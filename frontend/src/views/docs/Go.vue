<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-8">
    <div class="prose dark:prose-invert max-w-none">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-6">Go SDK</h1>

      <p class="text-lg text-gray-600 dark:text-gray-400 mb-8">
        The LogMachine Go SDK is built on top of Go's standard <code>log/slog</code> library (Go 1.21+),
        providing colored terminal output, structured logging, and real-time log forwarding to central servers.
      </p>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Installation</h2>

      <pre class="bg-gray-800 text-green-400 p-4 rounded-lg overflow-x-auto mb-6"><code>go get github.com/logmachine/go</code></pre>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Basic Usage</h2>

      <pre class="bg-gray-800 text-green-400 p-4 rounded-lg overflow-x-auto mb-6"><code>package main

import (
    "log/slog"
    logmachine "github.com/logmachine/go"
)

func main() {
    logger, err := logmachine.New(logmachine.Options{
        LogFile:    "logs.log",
        ErrorFile:  "errors.log",
        DebugLevel: 0,
    })
    if err != nil {
        panic(err)
    }
    defer logger.Close()

    logger.Info("Hello, world!")
    logger.Error("An error occurred!")
    logger.Success("Operation completed successfully!")
    logger.Debug("Debugging information here.")
    logger.Warn("This is a warning message.")
}</code></pre>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Central Logging</h2>

      <p class="text-gray-600 dark:text-gray-400 mb-4">
        Connect to a central LogMachine server for collaborative logging.
        Your logs will be visible to team members in real-time.
      </p>

      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">HTTP Transport</h3>

      <pre class="bg-gray-800 text-green-400 p-4 rounded-lg overflow-x-auto mb-4"><code>logger, err := logmachine.New(logmachine.Options{
    LogFile:   "logs.log",
    ErrorFile: "errors.log",
    Central: &logmachine.CentralConfig{
        URL:      "https://logmachine.org",
        Room:     "team_alpha",
        Endpoint: "/api/logs",                              // optional, default: /api/logs
        Headers:  map[string]string{"Authorization": "Bearer token"},
    },
})</code></pre>

      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">Socket.IO Transport</h3>

      <pre class="bg-gray-800 text-green-400 p-4 rounded-lg overflow-x-auto mb-6"><code>logger, err := logmachine.New(logmachine.Options{
    LogFile:  "logs.log",
    ErrorFile: "errors.log",
    Central: &logmachine.CentralConfig{
        URL:          "https://logmachine.org",
        Room:         "team_alpha",
        SocketIO:     true,
        SocketIOPath: "/api/socket.io/",
    },
})</code></pre>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Configuration Options</h2>

      <div class="overflow-x-auto mb-6">
        <table class="min-w-full bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600">
          <thead>
            <tr class="bg-gray-50 dark:bg-gray-700">
              <th class="px-4 py-2 border border-gray-300 dark:border-gray-600 text-left text-gray-900 dark:text-white">Parameter</th>
              <th class="px-4 py-2 border border-gray-300 dark:border-gray-600 text-left text-gray-900 dark:text-white">Type</th>
              <th class="px-4 py-2 border border-gray-300 dark:border-gray-600 text-left text-gray-900 dark:text-white">Default</th>
              <th class="px-4 py-2 border border-gray-300 dark:border-gray-600 text-left text-gray-900 dark:text-white">Description</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>LogFile</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">string</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">"logs.log"</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">File to save all logs</td>
            </tr>
            <tr class="bg-gray-50 dark:bg-gray-700">
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>ErrorFile</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">string</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">"errors.log"</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">File to save error logs</td>
            </tr>
            <tr>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>DebugLevel</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">int</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">0</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Console output level (0=all, 1=ERROR, 2=SUCCESS, etc.)</td>
            </tr>
            <tr class="bg-gray-50 dark:bg-gray-700">
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>Central</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">*CentralConfig</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">nil</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Central server configuration</td>
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
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>URL</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Yes</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Central server base URL</td>
            </tr>
            <tr class="bg-gray-50 dark:bg-gray-700">
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>Room</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Yes</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Room/organization name</td>
            </tr>
            <tr>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>Endpoint</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">No</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">HTTP API endpoint (default: /api/logs)</td>
            </tr>
            <tr class="bg-gray-50 dark:bg-gray-700">
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>Headers</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">No</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Extra headers for authentication</td>
            </tr>
            <tr>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>SocketIO</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">No</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Use Socket.IO instead of HTTP (default: false)</td>
            </tr>
            <tr class="bg-gray-50 dark:bg-gray-700">
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>SocketIOPath</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">No</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Socket.IO path (default: /api/socket.io/)</td>
            </tr>
          </tbody>
        </table>
      </div>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Advanced Features</h2>

      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">Custom Log Levels</h3>

      <pre class="bg-gray-800 text-green-400 p-4 rounded-lg overflow-x-auto mb-4"><code>criticalHack := logger.NewLevel("CRITICAL_HACK", slog.Level(16))
deployment := logger.NewLevel("DEPLOYMENT", slog.Level(8))

criticalHack("Zero day vulnerability found!")
deployment("Application deployed to production")</code></pre>

      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">JSON Export</h3>

      <pre class="bg-gray-800 text-green-400 p-4 rounded-lg overflow-x-auto mb-4"><code>// Convert logs to JSON
entries, err := logger.Jsonifier()
if err != nil {
    panic(err)
}
for _, entry := range entries {
    fmt.Println(entry) // Each entry is a JSON string
}</code></pre>

      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">Parse Single Log Entry</h3>

      <pre class="bg-gray-800 text-green-400 p-4 rounded-lg overflow-x-auto mb-6"><code>// Parse a single log entry
entry := logger.ParseLog(rawLogText)
if entry != nil {
    fmt.Printf("User: %s, Level: %s, Message: %s\n",
        entry.User, entry.Level, entry.Message)
}</code></pre>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Log Output Format</h2>

      <div class="bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg p-6 mb-6">
        <pre class="text-gray-800 dark:text-gray-200"><code>(username @ myapp) 🤌 CL Timing: [ 2024-01-15T10:30:45+00:00 ]
[ INFO ] Server started on port 8000
🏁</code></pre>
      </div>

      <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6">
        <h3 class="text-lg font-semibold text-blue-800 dark:text-blue-200 mb-2">📚 Resources</h3>
        <ul class="text-blue-700 dark:text-blue-300 space-y-1">
          <li><a href="https://github.com/logmachine/go" class="underline hover:no-underline">GitHub Repository</a></li>
          <li><a href="https://pkg.go.dev/github.com/logmachine/go" class="underline hover:no-underline">Go Package Documentation</a></li>
          <li><a href="https://logmachine.org" class="underline hover:no-underline">Log Machine</a></li>
        </ul>
      </div>
    </div>
  </div>
</template>