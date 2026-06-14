#!/usr/bin/env python3
"""
Bootstrap script to create the first admin user during installation.
Usage: python3 bootstrap_admin.py [username]

If no username is provided, the current system user is used.
"""

import sys
import os
import time
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from db import DB


def _bootstrap_database_url():
    os.environ.setdefault("DATABASE_URL", "postgresql:///central")

def bootstrap_admin(username=None):
    """Create the first admin user if none exists."""
    if username is None:
        username = os.getenv("USER") or "admin"

    _bootstrap_database_url()

    db = None
    last_error = None
    for _ in range(10):
        try:
            db = DB()
            break
        except Exception as e:
            last_error = e
            time.sleep(1)

    if db is None:
        print(f"✗ Could not connect to PostgreSQL after retries: {last_error}")
        return False

    # # Check if admins already exist
    # try:
    #     admin_count = db.count_admins()
    #     if admin_count > 0:
    #         print(f"✓ Admin user(s) already exist ({admin_count}). Skipping bootstrap.")
    #         return True
    # except Exception as e:
    #     print(f"✗ Could not inspect admin users: {e}")
    #     return False

    try:
        # Create local admin user
        user = db.create_local_admin_user(username)
        print(f"✓ Bootstrap admin user created: {username}")
        print(f"  Type: {user.get('type')}")
        return True
    except ValueError as e:
        print(f"✗ Error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    username = sys.argv[1] if len(sys.argv) > 1 else None
    success = bootstrap_admin(username)
    sys.exit(0 if success else 1)
