#!/usr/bin/env bash
## Copyright (c) 2025 Buffer Punk and contributors

## Unified deployment entrypoint for the LogMachine central app.
## Supported commands:
##   ./install.sh install
##   ./install.sh uninstall
## Optional flags:
##   --venv <path>    Use an existing virtual environment instead of creating ./lenv
##   --domain <host>  Use a server domain without prompting during setup
##   --uninstall      Uninstall LogMachine services and nginx config
##   --force          Skip optional prompts and install unattended where possible

set -euo pipefail

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

user_can_sudo() {
  command_exists sudo || return 1
  case "${PREFIX:-}" in
  *com.termux*) return 1 ;;
  esac
  ! LANG= sudo -n -v 2>&1 | grep -q "may not run sudo"
}

resolve_script_dir() {
  local source_path=${BASH_SOURCE[0]:-}
  if [ -n "$source_path" ] && [ -f "$source_path" ]; then
    cd "$(dirname "$source_path")" && pwd
  else
    pwd
  fi
}

script_dir=$(resolve_script_dir)
workspace_root=$(cd "$script_dir" && pwd)

# check if dir is "central", if not, assume we're in a subdir and adjust workspace_root accordingly
if [ "$(basename "$workspace_root")" != "central" ]; then
  workspace_root=$(dirname "$workspace_root")
  cd "$workspace_root"
fi

selected_venv="$workspace_root/lenv"
custom_venv_provided="false"
server_domain=""
server_domain_provided="false"
force_mode="false"
declare -a positional_args=()
declare -a forward_args=()

source "$workspace_root/deployment/awesome.conf"

if ! user_can_sudo; then
  echo -e "${BRed}Error: You need sudo privileges to run this script.${Color_Off}"
  exit 1
fi

normalize_command() {
  local first=${1:-}
  local second=${2:-}

  case "${first,,}:${second,,}" in
    install:)
      echo install
      ;;
    uninstall:)
      echo uninstall
      ;;
    server:setup|server:setup\ *)
      echo server-setup
      ;;
    server-setup:|server_setup:)
      echo server-setup
      ;;
    setup:)
      echo server-setup
      ;;
    *)
      echo ""
      ;;
  esac
}

parse_cli_args() {
  while [ $# -gt 0 ]; do
    case "$1" in
      --venv)
        if [ $# -lt 2 ]; then
          echo -e "${BRed}Error: --venv requires a path argument.${Color_Off}"
          exit 1
        fi
        selected_venv="$2"
        custom_venv_provided="true"
        shift 2
        ;;
      --venv=*)
        selected_venv="${1#*=}"
        custom_venv_provided="true"
        shift
        ;;
      --domain)
        if [ $# -lt 2 ]; then
          echo -e "${BRed}Error: --domain requires a host argument.${Color_Off}"
          exit 1
        fi
        server_domain="$2"
        server_domain_provided="true"
        shift 2
        ;;
      --domain=*)
        server_domain="${1#*=}"
        server_domain_provided="true"
        shift
        ;;
      --admin)
        if [ $# -lt 2 ]; then
          echo -e "${BRed}Error: --admin requires a username argument.${Color_Off}"
          exit 1
        fi
        export BOOTSTRAP_ADMIN_USERNAME="$2"
        shift 2
        ;;
      --admin=*)
        export BOOTSTRAP_ADMIN_USERNAME="${1#*=}"
        shift
        ;;
      --force)
        force_mode="true"
        forward_args+=("$1")
        shift
        ;;
      --uninstall)
        positional_args=("uninstall")
        shift
        ;;
      *)
        positional_args+=("$1")
        forward_args+=("$1")
        shift
        ;;
    esac
  done

  if [ "$custom_venv_provided" = "true" ]; then
    case "$selected_venv" in
      /*) ;;
      *) selected_venv="$workspace_root/$selected_venv" ;;
    esac

    if [ ! -x "$selected_venv/bin/python3" ]; then
      echo -e "${BRed}Error: Provided venv is invalid: $selected_venv${Color_Off}"
      echo "Expected Python executable at: $selected_venv/bin/python3"
      exit 1
    fi
  fi
}

run_uninstall() {
  local answer="y"

  if [ "$force_mode" != "true" ]; then
    printf "${BRed}This will remove LogMachine systemd services and nginx config. Database and Redis data will be kept. Continue? (y/n) ${Color_Off}"
    read -r -p " " answer
    answer=${answer,,}
    if [[ "$answer" != "y" ]]; then
      echo -e "${BBlue}Uninstall cancelled.${Color_Off}"
      return 0
    fi
  fi

  echo -e "${BBlue}Stopping LogMachine services...${Color_Off}"
  sudo systemctl stop central_api central_client >/dev/null 2>&1 || true
  sudo systemctl disable central_api central_client >/dev/null 2>&1 || true

  echo -e "${BBlue}Removing systemd unit files...${Color_Off}"
  sudo rm -f /etc/systemd/system/central_api.service
  sudo rm -f /etc/systemd/system/central_client.service
  sudo systemctl daemon-reload

  echo -e "${BBlue}Removing nginx config...${Color_Off}"
  sudo rm -f /etc/nginx/conf.d/central.conf
  sudo service nginx restart >/dev/null 2>&1 || true

  echo -e "${BBlue}Removing deployment log directory...${Color_Off}"
  sudo rm -rf /var/log/central

  printf "${BGreen}\nLogMachine services were uninstalled successfully.\n${Color_Off}"
  printf "Removing scheduled database jobs... "
  conf_dir=$(dirname $(sudo -u postgres psql -tAc "SHOW config_file"))
  sudo rm "$conf_dir/conf.d/central.conf" >/dev/null 2>&1 || true
  sudo -u postgres psql -d postgres -v ON_ERROR_STOP=0 -c "DO \$\$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.schemata WHERE schema_name = 'cron') THEN DELETE FROM cron.job WHERE database = 'central' OR jobname IN ('daily-retention-cleanup', 'cleanup-cron-logs'); END IF; END \$\$;" >/dev/null 2>&1 || true
  sudo systemctl restart postgresql >/dev/null 2>&1 || true
  printf "Done.\n"
  printf "Dropping database... "
  sudo -u postgres dropdb --if-exists central >/dev/null 2>&1 || true
  sudo redis-cli -n 1 FLUSHDB >/dev/null 2>&1 || true
  printf "Done.\n"
}

setup_database_schema() {
  local schema_file="backend/schema.sql"

  echo -e "${BBlue}Configuring PostgreSQL database...${Color_Off}"
  sudo systemctl start postgresql >/dev/null 2>&1 || true

  if ! sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname = '$USER'" | grep -q 1; then
    sudo -u postgres createuser --createdb "$USER"
  fi

  if ! sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname = 'central'" | grep -q 1; then
    sudo -u postgres createdb -O "$USER" central
  fi

  # Add pg_cron to shared preload_libraries if not already present
  if ! sudo -u postgres psql -tAc "SHOW shared_preload_libraries" | grep -q "pg_cron"; then
    conf_dir=$(dirname $(sudo -u postgres psql -tAc "SHOW config_file"))
    echo -e "shared_preload_libraries = 'pg_cron'\ncron.database_name = 'central'" | sudo tee "$conf_dir/conf.d/central.conf" >/dev/null
    sudo systemctl restart postgresql >/dev/null 2>&1 || true
  fi

  if [ -f "$schema_file" ]; then
    echo -e "${BBlue}Applying database schema...${Color_Off}"
    # Add database permissions for the current user
    sudo -u postgres psql -d central -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO \"$USER\";"
    sudo -u postgres psql -d central -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO \"$USER\";"
    sudo -u postgres psql -d central -c "GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO \"$USER\";"
    # Dump schema
    sudo -u postgres psql -d central -v ON_ERROR_STOP=0 -f "$schema_file"
    # Ensure the app role owns objects created by the schema so it can manage indexes.
    sudo -u postgres psql -d central -v ON_ERROR_STOP=0 -c "ALTER TABLE IF EXISTS users OWNER TO \"$USER\";"
    sudo -u postgres psql -d central -v ON_ERROR_STOP=0 -c "ALTER TABLE IF EXISTS rooms OWNER TO \"$USER\";"
    sudo -u postgres psql -d central -v ON_ERROR_STOP=0 -c "ALTER TABLE IF EXISTS logs OWNER TO \"$USER\";"
    sudo -u postgres psql -d central -v ON_ERROR_STOP=0 -c "ALTER SEQUENCE IF EXISTS users_id_seq OWNER TO \"$USER\";"
    sudo -u postgres psql -d central -v ON_ERROR_STOP=0 -c "ALTER VIEW IF EXISTS room_log_stats OWNER TO \"$USER\";"
  else
    echo -e "${BRed}Warning: schema file not found at $schema_file. Skipping schema setup.${Color_Off}"
  fi
}

run_package_install() {
  source /etc/lsb-release

  sudo apt install curl git gnupg -y
  if ! which zsh >/dev/null 2>&1; then
    local answer="y"
    if ! [[ "${*:-}" =~ (^|[[:space:]])--force($|[[:space:]]) ]]; then
      printf "${Purple}Zsh is not installed. Do you want to install it? (y/n) ${Color_Off}"
      read -r -p " " answer
    fi
    answer=${answer,,}
    if [[ $answer == "y" ]]; then
      sudo apt-get install zsh -y
      sudo -k chsh -s "$(command -v zsh)" "$USER"
    else
      echo "zsh is required to run this script. Exiting..."
      exit 1
    fi
  fi

  if [ ! -d "$HOME/.oh-my-zsh" ]; then
    if [ "$force_mode" = "true" ]; then
      echo -e "${BBlue}Installing oh-my-zsh...${Color_Off}"
      sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" --unattended
    else
      printf "${BBlue}Oh My Zsh is not installed. It is not required, but you may like it. Do you want to install it? (y/n) ${Color_Off}"
      read -r -p " " answer
      answer=${answer,,}
      if [[ $answer = "y" ]]; then
          echo -e "${BBlue}Installing oh-my-zsh...${Color_Off} (You may need to rerun the script if oh-my-zsh changes your shell before the installation finishes)"
          sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" --unattended
      fi
    fi
  fi

  if command_exists node; then
    NODE_VERSION=$(node -v | sed 's/v//;s/\..*//')
    if [ "$NODE_VERSION" -lt 24 ]; then
      echo -e "${BBlue}Updating Node.js to the latest LTS version...${Color_Off}"
      curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -
      sudo apt-get install -y nodejs
    else
      echo -e "${BGreen}Node.js version $NODE_VERSION is already installed.${Color_Off}"
    fi
  else
    echo -e "${BBlue}Configuring Node.js...${Color_Off}"
    curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -
  fi

  sudo rm -f /usr/share/keyrings/redis-archive-keyring.gpg
  curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
  sudo chmod 644 /usr/share/keyrings/redis-archive-keyring.gpg
  echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list >/dev/null

  sudo apt-get update -y
  sudo apt install \
    nodejs python3-pip python3-venv python3-dev \
    build-essential redis postgresql postgresql-contrib postgresql-16-cron postgresql-16-pgvector \
    software-properties-common nginx certbot python3-certbot-nginx -y

  if apt-cache show postgresql-16-pgvector >/dev/null 2>&1; then
    sudo apt install postgresql-16-pgvector -y
  fi

  cd "$workspace_root"
  if [ "$custom_venv_provided" = "false" ] && [ ! -d "$selected_venv" ]; then
    python3 -m venv "$selected_venv"
  fi
  source "$selected_venv/bin/activate"

  pip3 install --upgrade pip
  pip3 install -r "$workspace_root/backend/requirements.txt"

  cd "$workspace_root/frontend"
  sudo npm install -g serve
  npm install --legacy-peer-deps

  printf "${BGreen}\nAll packages installed successfully.\n${Color_Off}"
}

run_server_setup() {
  cd "$workspace_root"

  if [ -z "$server_domain" ]; then
    read -r -p "Enter your server domain (e.g. example.com): " server_domain
    printf "\n"
  else
    printf "Using provided server domain: %s\n" "$server_domain"
  fi

  local_install="false"
  scheme="https://"
  frontend_base_url="/"
  frontend_api_url="$scheme$server_domain/api"
  case "$server_domain" in
    localhost|127.0.0.1|::1)
      local_install="true"
      scheme="http://"
      # frontend_base_url="/logmachine"
      frontend_api_url="$scheme$server_domain/api"
      ;;
  esac

  sudo mkdir -p /var/log/central
  sudo chown "$USER":www-data /var/log/central

  central_api=$(cat <<EOF
[Unit]
Description=API Client in FastAPI (Backend)
After=network.target nginx.service
Requires=nginx.service

[Service]
User=$USER
Group=www-data
WorkingDirectory=$workspace_root/backend
Environment=SERVER_DOMAIN=$scheme$server_domain
Environment=DATABASE_URL=postgresql:///central
ExecStart=$selected_venv/bin/python3 -m uvicorn app:sio_app --host 0.0.0.0 --port 5040 --workers 1 --log-level info
StandardOutput=append:/var/log/central/api.log
StandardError=append:/var/log/central/api-error.log

[Install]
WantedBy=multi-user.target
EOF
)

  central_frontend=$(cat <<EOF
[Unit]
Description=Central Client in Vue.js (Web App)
After=network.target central_api.service
Requires=central_api.service

[Service]
User=$USER
Group=www-data
WorkingDirectory=$workspace_root/frontend
ExecStart=npx serve -s dist -l 4050 -c 0
StandardOutput=append:/var/log/central/frontend.log
StandardError=append:/var/log/central/frontend-error.log

[Install]
WantedBy=multi-user.target
EOF
)

  central_nginx_config="
  server {
    listen 80;
    server_name $server_domain;
    location / {
      include proxy_params;
      proxy_pass http://0.0.0.0:4050;
    }
    location /api {
      include proxy_params;
      proxy_http_version 1.1;
      proxy_set_header Upgrade \$http_upgrade;
      proxy_set_header Connection \"upgrade\";
      proxy_pass http://0.0.0.0:5040;
    }
  }
  "

  cd "$workspace_root/frontend"
  VITE_BASE_URL="$frontend_base_url" VITE_API_URL="$frontend_api_url" npm run build
  cd "$workspace_root"

  sudo tee /etc/nginx/conf.d/central.conf >/dev/null <<< "$central_nginx_config"
  echo "$central_api" | sudo tee /etc/systemd/system/central_api.service >/dev/null
  echo "$central_frontend" | sudo tee /etc/systemd/system/central_client.service >/dev/null

  sudo systemctl daemon-reload
  setup_database_schema

  sudo systemctl enable postgresql
  sudo systemctl enable central_api
  sudo systemctl enable central_client
  sudo service nginx restart
  sudo service postgresql start
  sudo service central_api start
  sudo service central_client start

  # Wait for backend to be ready
  echo -e "${BBlue}Waiting for backend to initialize...${Color_Off}"
  sleep 5

  # Bootstrap first admin user
  echo -e "${BBlue}Creating bootstrap admin user...${Color_Off}"
  source "$selected_venv/bin/activate"
  cd "$workspace_root/backend"
  DATABASE_URL=postgresql:///central python3 bootstrap_admin.py ${BOOTSTRAP_ADMIN_USERNAME:-${USER}} || true
  deactivate

  if [ "$local_install" = "false" ]; then
    sudo certbot --nginx -d "$server_domain"
    sudo service nginx restart
  fi

  sudo systemctl status central_api central_client --no-pager

  printf "${BGreen}\nLogMachine Central has been successfully deployed on your server!\n"
  printf "${BPurple}Please make sure to check the logs for any errors.\n"
  printf "${Color_Off}App running at ${BGreen}%s%s\n\n${Color_Off}" "$scheme" "$server_domain$frontend_base_url"
}

main() {
  local mode
  parse_cli_args "$@"
  mode=$(normalize_command "${positional_args[0]:-}" "${positional_args[1]:-}")

  case "$mode" in
    uninstall)
      run_uninstall
      ;;
    server-setup)
      run_server_setup "${forward_args[@]}"
      ;;
    *)
      run_package_install "${forward_args[@]}"
      run_server_setup "${forward_args[@]}"
      ;;
  esac
}

main "$@"
