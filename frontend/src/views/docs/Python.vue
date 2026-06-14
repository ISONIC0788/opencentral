<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-8">
    <div class="prose dark:prose-invert max-w-none">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-6">Python SDK</h1>

      <p class="text-lg text-gray-600 dark:text-gray-400 mb-8">
        The LogMachine Python SDK provides seamless integration with Python applications,
        offering colored console output and real-time log forwarding to central servers.
      </p>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Installation</h2>

      <pre class="bg-gray-800 text-green-400 p-4 rounded-lg overflow-x-auto mb-6"><code>pip install logmachine</code></pre>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Basic Usage</h2>

      <pre class="bg-gray-800 text-green-400 p-4 rounded-lg overflow-x-auto mb-4"><code>from logmachine import LogMachine

# Create a logger (replaces standard logging)
logger = LogMachine("myapp", debug_level=1)

logger.info("Hello, world!")
logger.error("An error occurred!")
logger.success("Operation completed successfully!")
logger.debug("Debugging information here.")
logger.warning("This is a warning message.")</code></pre>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Central Logging</h2>

      <p class="text-gray-600 dark:text-gray-400 mb-4">
        Connect to a central LogMachine server for collaborative logging.
        Your logs will be visible to team members in real-time.
      </p>

      <pre class="bg-gray-800 text-green-400 p-4 rounded-lg overflow-x-auto mb-4"><code>from logmachine import LogMachine

# Connect to your central server
logger = LogMachine("myapp", debug_level=0, central={
    "url": "https://logmachine.org",
    "room": "team_alpha",
    "headers": {"Authorization": "Bearer token"}  # Optional
})

logger.info("This log is sent to the central server!")</code></pre>

      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">Using the Default Logger</h3>

      <pre class="bg-gray-800 text-green-400 p-4 rounded-lg overflow-x-auto mb-6"><code>from logmachine import default_logger

# Uses https://logmachine.org with auto-generated room
logger = default_logger()
logger.success("Connected to default central server!")</code></pre>

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
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>debug_level</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">int</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">0</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Console output level (0=all, 1=ERROR, 2=SUCCESS, etc.)</td>
            </tr>
            <tr class="bg-gray-50 dark:bg-gray-700">
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>log_file</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">str</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">"logs.log"</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">File to save all logs</td>
            </tr>
            <tr>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>error_file</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">str</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">"errors.log"</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">File to save error logs</td>
            </tr>
            <tr class="bg-gray-50 dark:bg-gray-700">
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>central</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">dict</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">None</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Central server configuration</td>
            </tr>
            <tr>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>verbose</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">bool</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">False</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Show all log levels in console</td>
            </tr>
          </tbody>
        </table>
      </div>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Central Configuration</h2>

      <div class="overflow-x-auto mb-6">
        <table class="min-w-full bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600">
          <thead>
            <tr class="bg-gray-50 dark:bg-gray-700">
              <th class="px-4 py-2 border border-gray-300 dark:border-gray-600 text-left text-gray-900 dark:text-white">Key</th>
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
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">API endpoint (default: /api/logs)</td>
            </tr>
            <tr class="bg-gray-50 dark:bg-gray-700">
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>headers</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">No</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Extra headers for authentication</td>
            </tr>
          </tbody>
        </table>
      </div>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Advanced Features</h2>

      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">Custom Log Levels</h3>

      <pre class="bg-gray-800 text-green-400 p-4 rounded-lg overflow-x-auto mb-4"><code>logger.new_level("CRITICAL_HACK", 60)
logger.new_level("DEPLOYMENT", 35, "\033[38;5;208m")  # Orange color

logger.critical_hack("Zero day vulnerability found!")
logger.deployment("Application deployed to production")</code></pre>

      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">JSON Export</h3>

      <pre class="bg-gray-800 text-green-400 p-4 rounded-lg overflow-x-auto mb-4"><code># Get logs as JSON objects
json_logs = logger.jsonifier()
for log_entry in json_logs:
    print(log_entry)  # Each entry is a JSON string</code></pre>

      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">Username Management</h3>

      <p class="text-gray-600 dark:text-gray-400 mb-4">
        Usernames are automatically resolved and cached in <code>~/.cl_username</code>.
        Override manually if needed:
      </p>

      <pre class="bg-gray-800 text-green-400 p-4 rounded-lg overflow-x-auto mb-6"><code>import os
os.environ['CL_USERNAME'] = 'my_custom_username'</code></pre>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Log Output Format</h2>

      <div class="bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg p-6 mb-6">
        <pre class="text-gray-800 dark:text-gray-200"><code>(username @ module) 🤌 CL Timing: [ 2024-01-15T10:30:45 ]
[ INFO ] Server started on port 8000
🏁</code></pre>
      </div>

      <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6">
        <h3 class="text-lg font-semibold text-blue-800 dark:text-blue-200 mb-2">📚 Resources</h3>
        <ul class="text-blue-700 dark:text-blue-300 space-y-1">
          <li><a href="https://github.com/logmachine/python" class="underline hover:no-underline">GitHub Repository</a></li>
          <li><a href="https://pypi.org/project/logmachine/" class="underline hover:no-underline">PyPI Package</a></li>
          <li><a href="https://logmachine.org" class="underline hover:no-underline">Log Machine</a></li>
        </ul>
      </div>
    </div>
  </div>
</template>