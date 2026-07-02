<template>
  <div class="bg-[#ffffff] dark:bg-[#000000] border border-neutral-200/80 dark:border-neutral-800/80 rounded-md p-8 shadow-none">
    <div class="prose dark:prose-invert max-w-none">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-6">Rust SDK</h1>

      <p class="text-lg text-gray-600 dark:text-gray-400 mb-8">
        The LogMachine Rust SDK installs a global logger that captures logs from your entire Rust application,
        providing colored terminal output and real-time log forwarding to central servers.
      </p>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Installation</h2>

      <pre class="bg-neutral-50 border border-neutral-200/60 text-neutral-800 dark:bg-neutral-900 dark:border-neutral-800/60 dark:text-neutral-200 p-4 rounded-md text-sm overflow-x-auto font-mono mb-6"><code>cargo add logmachine</code></pre>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Basic Usage</h2>

      <pre class="bg-neutral-50 border border-neutral-200/60 text-neutral-800 dark:bg-neutral-900 dark:border-neutral-800/60 dark:text-neutral-200 p-4 rounded-md text-sm overflow-x-auto font-mono mb-6"><code>use logmachine::{init_global_logger, success, LogMachineOptions};

fn main() -> Result&lt;(), Box&lt;dyn std::error::Error&gt;&gt; {
    init_global_logger(LogMachineOptions {
        debug_level: 0,
        ..Default::default()
    })?;

    log::info!("Hello from info");
    log::warn!("Hello from warn");
    log::error!("Hello from error");
    success("Hello from success");
    Ok(())
}</code></pre>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Central Logging</h2>

      <p class="text-gray-600 dark:text-gray-400 mb-4">
        Connect to a central LogMachine server for collaborative logging.
        Your logs will be visible to team members in real-time.
      </p>

      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">HTTP Transport</h3>

      <pre class="bg-neutral-50 border border-neutral-200/60 text-neutral-800 dark:bg-neutral-900 dark:border-neutral-800/60 dark:text-neutral-200 p-4 rounded-md text-sm overflow-x-auto font-mono mb-6"><code>use std::collections::HashMap;

init_global_logger(LogMachineOptions {
    central: Some(CentralConfig {
        url: "https://logmachine.org".to_string(),
        room: "public".to_string(),
        endpoint: "/api/logs".to_string(),
        headers: HashMap::new(),
        socketio: false,
        socketio_path: "/api/socket.io/".to_string(),
    }),
    ..Default::default()
})?;</code></pre>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Configuration Options</h2>

      <div class="overflow-x-auto mb-6">
        <table class="min-w-full bg-transparent border border-neutral-200 dark:border-neutral-800 text-sm">
          <thead>
            <tr>
              <th class="bg-neutral-100 dark:bg-neutral-900 px-4 py-2 border border-neutral-200 dark:border-neutral-800 font-semibold text-[#171717] dark:text-[#ffffff] text-left">Field</th>
              <th class="bg-neutral-100 dark:bg-neutral-900 px-4 py-2 border border-neutral-200 dark:border-neutral-800 font-semibold text-[#171717] dark:text-[#ffffff] text-left">Type</th>
              <th class="bg-neutral-100 dark:bg-neutral-900 px-4 py-2 border border-neutral-200 dark:border-neutral-800 font-semibold text-[#171717] dark:text-[#ffffff] text-left">Default</th>
              <th class="bg-neutral-100 dark:bg-neutral-900 px-4 py-2 border border-neutral-200 dark:border-neutral-800 font-semibold text-[#171717] dark:text-[#ffffff] text-left">Description</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>log_file</code></td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">String</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">"logs.log"</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">File to save all logs</td>
            </tr>
            <tr class="bg-neutral-50/50 dark:bg-neutral-900/40">
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>error_file</code></td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">String</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">"errors.log"</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">File to save error logs</td>
            </tr>
            <tr>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>debug_level</code></td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">u8</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">0</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">Console output level (0=all, 1=ERROR, 2=SUCCESS, etc.)</td>
            </tr>
            <tr class="bg-neutral-50/50 dark:bg-neutral-900/40">
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>verbose</code></td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">bool</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">false</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">Show all log levels in console</td>
            </tr>
            <tr>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>central</code></td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">Option&lt;CentralConfig&gt;</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">None</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">Central server configuration</td>
            </tr>
            <tr class="bg-neutral-50/50 dark:bg-neutral-900/40">
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>attached</code></td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">bool</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">false</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">Whether logger is already attached</td>
            </tr>
          </tbody>
        </table>
      </div>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Central Configuration</h2>

      <div class="overflow-x-auto mb-6">
        <table class="min-w-full bg-transparent border border-neutral-200 dark:border-neutral-800 text-sm">
          <thead>
            <tr>
              <th class="bg-neutral-100 dark:bg-neutral-900 px-4 py-2 border border-neutral-200 dark:border-neutral-800 font-semibold text-[#171717] dark:text-[#ffffff] text-left">Field</th>
              <th class="bg-neutral-100 dark:bg-neutral-900 px-4 py-2 border border-neutral-200 dark:border-neutral-800 font-semibold text-[#171717] dark:text-[#ffffff] text-left">Required</th>
              <th class="bg-neutral-100 dark:bg-neutral-900 px-4 py-2 border border-neutral-200 dark:border-neutral-800 font-semibold text-[#171717] dark:text-[#ffffff] text-left">Description</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>url</code></td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">Yes</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">Central server base URL</td>
            </tr>
            <tr class="bg-neutral-50/50 dark:bg-neutral-900/40">
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>room</code></td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">Yes</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">Room/organization name</td>
            </tr>
            <tr>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>endpoint</code></td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">No</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">HTTP API endpoint (default: /api/logs)</td>
            </tr>
            <tr class="bg-neutral-50/50 dark:bg-neutral-900/40">
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>headers</code></td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">No</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">Extra headers for authentication</td>
            </tr>
            <tr>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>socketio</code></td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">No</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">Use Socket.IO instead of HTTP (default: false)</td>
            </tr>
            <tr class="bg-neutral-50/50 dark:bg-neutral-900/40">
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>socketio_path</code></td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">No</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">Socket.IO path (default: /api/socket.io/)</td>
            </tr>
          </tbody>
        </table>
      </div>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Advanced Features</h2>

      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">Success Logging</h3>

      <pre class="bg-neutral-50 border border-neutral-200/60 text-neutral-800 dark:bg-neutral-900 dark:border-neutral-800/60 dark:text-neutral-200 p-4 rounded-md text-sm overflow-x-auto font-mono mb-6"><code>use logmachine::success;

success("Operation completed successfully!");</code></pre>

      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">JSON Export</h3>

      <pre class="bg-neutral-50 border border-neutral-200/60 text-neutral-800 dark:bg-neutral-900 dark:border-neutral-800/60 dark:text-neutral-200 p-4 rounded-md text-sm overflow-x-auto font-mono mb-6"><code>use logmachine::jsonifier;

// Get logs as JSON strings
let json_logs = jsonifier("logs.log")?;
for log_entry in json_logs {
    println!("{}", log_entry); // Each entry is a JSON string
}</code></pre>

      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">Parse Single Log Entry</h3>

      <pre class="bg-neutral-50 border border-neutral-200/60 text-neutral-800 dark:bg-neutral-900 dark:border-neutral-800/60 dark:text-neutral-200 p-4 rounded-md text-sm overflow-x-auto font-mono mb-6"><code>use logmachine::parse_log;

// Parse a single log entry
if let Some(entry) = parse_log(raw_log_text) {
    println!("User: {}, Level: {}, Message: {}",
        entry.user, entry.level, entry.message);
}</code></pre>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Log Output Format</h2>

      <div class="bg-neutral-50/40 dark:bg-neutral-900/20 border border-neutral-200 dark:border-neutral-800 rounded-md p-6 mb-6">
        <pre class="text-gray-800 dark:text-gray-200"><code>(username @ crate_name) 🤌 CL Timing: [ 2024-01-15T10:30:45+00:00 ]
[ INFO ] Server started on port 8000
🏁</code></pre>
      </div>

      <div class="bg-neutral-50 dark:bg-neutral-900/40 border border-neutral-200 dark:border-neutral-800 rounded-md p-6 mb-6">
        <h3 class="text-lg font-semibold text-[#171717] dark:text-[#ffffff] mb-2">⚠️ Important Notes</h3>
        <ul class="text-neutral-600 dark:text-neutral-400 space-y-1">
          <li>The Rust SDK installs a global logger that captures all logs from your application</li>
          <li>Debug level filtering only affects console output, not file writes</li>
          <li>All logs are written to files regardless of debug level</li>
          <li>Username resolution works the same as other SDKs</li>
        </ul>
      </div>

      <div class="bg-neutral-50/80 dark:bg-neutral-900/30 border border-neutral-200 dark:border-neutral-800 rounded-md p-6">
        <h3 class="text-lg font-semibold text-[#171717] dark:text-[#ffffff] mb-2">📚 Resources</h3>
        <ul class="space-y-1">
          <li><a href="https://github.com/logmachine/rust" class="text-neutral-800 dark:text-neutral-200 hover:text-black hover:dark:text-white underline">GitHub Repository</a></li>
          <li><a href="https://crates.io/crates/logmachine" class="text-neutral-800 dark:text-neutral-200 hover:text-black hover:dark:text-white underline">Crates.io Package</a></li>
          <li><a href="https://docs.rs/logmachine" class="text-neutral-800 dark:text-neutral-200 hover:text-black hover:dark:text-white underline">API Documentation</a></li>
          <li><a href="https://logmachine.org" class="text-neutral-800 dark:text-neutral-200 hover:text-black hover:dark:text-white underline">Log Machine</a></li>
        </ul>
      </div>
    </div>
  </div>
</template>