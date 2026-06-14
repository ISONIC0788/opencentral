<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-8">
    <div class="prose dark:prose-invert max-w-none">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-6">Rust SDK</h1>

      <p class="text-lg text-gray-600 dark:text-gray-400 mb-8">
        The LogMachine Rust SDK installs a global logger that captures logs from your entire Rust application,
        providing colored terminal output and real-time log forwarding to central servers.
      </p>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Installation</h2>

      <pre class="bg-gray-800 text-green-400 p-4 rounded-lg overflow-x-auto mb-6"><code>cargo add logmachine</code></pre>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Basic Usage</h2>

      <pre class="bg-gray-800 text-green-400 p-4 rounded-lg overflow-x-auto mb-6"><code>use logmachine::{init_global_logger, success, LogMachineOptions};

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

      <pre class="bg-gray-800 text-green-400 p-4 rounded-lg overflow-x-auto mb-6"><code>use std::collections::HashMap;

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
        <table class="min-w-full bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600">
          <thead>
            <tr class="bg-gray-50 dark:bg-gray-700">
              <th class="px-4 py-2 border border-gray-300 dark:border-gray-600 text-left text-gray-900 dark:text-white">Field</th>
              <th class="px-4 py-2 border border-gray-300 dark:border-gray-600 text-left text-gray-900 dark:text-white">Type</th>
              <th class="px-4 py-2 border border-gray-300 dark:border-gray-600 text-left text-gray-900 dark:text-white">Default</th>
              <th class="px-4 py-2 border border-gray-300 dark:border-gray-600 text-left text-gray-900 dark:text-white">Description</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>log_file</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">String</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">"logs.log"</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">File to save all logs</td>
            </tr>
            <tr class="bg-gray-50 dark:bg-gray-700">
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>error_file</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">String</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">"errors.log"</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">File to save error logs</td>
            </tr>
            <tr>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>debug_level</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">u8</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">0</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Console output level (0=all, 1=ERROR, 2=SUCCESS, etc.)</td>
            </tr>
            <tr class="bg-gray-50 dark:bg-gray-700">
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>verbose</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">bool</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">false</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Show all log levels in console</td>
            </tr>
            <tr>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>central</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Option&lt;CentralConfig&gt;</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">None</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Central server configuration</td>
            </tr>
            <tr class="bg-gray-50 dark:bg-gray-700">
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>attached</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">bool</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">false</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Whether logger is already attached</td>
            </tr>
          </tbody>
        </table>
      </div>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Central Configuration</h2>

      <div class="overflow-x-auto mb-6">
        <table class="min-w-full bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600">
          <thead>
            <tr class="bg-gray-50 dark:bg-gray-700">
              <th class="px-4 py-2 border border-gray-300 dark:border-gray-600 text-left text-gray-900 dark:text-white">Field</th>
              <th class="px-4 py-2 border border-gray-300 dark:border-gray-600 text-left text-gray-900 dark:text-white">Required</th>
              <th class="px-4 py-2 border border-gray-300 dark:border-gray-600 text-left text-gray-900 dark:text-white">Description</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>url</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Yes</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Central server base URL</td>
            </tr>
            <tr class="bg-gray-50 dark:bg-gray-700">
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>room</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Yes</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Room/organization name</td>
            </tr>
            <tr>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>endpoint</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">No</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">HTTP API endpoint (default: /api/logs)</td>
            </tr>
            <tr class="bg-gray-50 dark:bg-gray-700">
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>headers</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">No</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Extra headers for authentication</td>
            </tr>
            <tr>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>socketio</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">No</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Use Socket.IO instead of HTTP (default: false)</td>
            </tr>
            <tr class="bg-gray-50 dark:bg-gray-700">
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>socketio_path</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">No</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Socket.IO path (default: /api/socket.io/)</td>
            </tr>
          </tbody>
        </table>
      </div>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Advanced Features</h2>

      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">Success Logging</h3>

      <pre class="bg-gray-800 text-green-400 p-4 rounded-lg overflow-x-auto mb-4"><code>use logmachine::success;

success("Operation completed successfully!");</code></pre>

      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">JSON Export</h3>

      <pre class="bg-gray-800 text-green-400 p-4 rounded-lg overflow-x-auto mb-4"><code>use logmachine::jsonifier;

// Get logs as JSON strings
let json_logs = jsonifier("logs.log")?;
for log_entry in json_logs {
    println!("{}", log_entry); // Each entry is a JSON string
}</code></pre>

      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">Parse Single Log Entry</h3>

      <pre class="bg-gray-800 text-green-400 p-4 rounded-lg overflow-x-auto mb-6"><code>use logmachine::parse_log;

// Parse a single log entry
if let Some(entry) = parse_log(raw_log_text) {
    println!("User: {}, Level: {}, Message: {}",
        entry.user, entry.level, entry.message);
}</code></pre>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Log Output Format</h2>

      <div class="bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg p-6 mb-6">
        <pre class="text-gray-800 dark:text-gray-200"><code>(username @ crate_name) 🤌 CL Timing: [ 2024-01-15T10:30:45+00:00 ]
[ INFO ] Server started on port 8000
🏁</code></pre>
      </div>

      <div class="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-6 mb-6">
        <h3 class="text-lg font-semibold text-yellow-800 dark:text-yellow-200 mb-2">⚠️ Important Notes</h3>
        <ul class="text-yellow-700 dark:text-yellow-300 space-y-1">
          <li>The Rust SDK installs a global logger that captures all logs from your application</li>
          <li>Debug level filtering only affects console output, not file writes</li>
          <li>All logs are written to files regardless of debug level</li>
          <li>Username resolution works the same as other SDKs</li>
        </ul>
      </div>

      <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6">
        <h3 class="text-lg font-semibold text-blue-800 dark:text-blue-200 mb-2">📚 Resources</h3>
        <ul class="text-blue-700 dark:text-blue-300 space-y-1">
          <li><a href="https://github.com/logmachine/rust" class="underline hover:no-underline">GitHub Repository</a></li>
          <li><a href="https://crates.io/crates/logmachine" class="underline hover:no-underline">Crates.io Package</a></li>
          <li><a href="https://docs.rs/logmachine" class="underline hover:no-underline">API Documentation</a></li>
          <li><a href="https://logmachine.org" class="underline hover:no-underline">Log Machine</a></li>
        </ul>
      </div>
    </div>
  </div>
</template>