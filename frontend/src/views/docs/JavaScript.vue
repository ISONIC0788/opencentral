<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-8">
    <div class="prose dark:prose-invert max-w-none">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-6">JavaScript SDK</h1>

      <p class="text-lg text-gray-600 dark:text-gray-400 mb-8">
        The LogMachine JavaScript SDK works in both Node.js and browser environments,
        providing colored console output and real-time log forwarding to central servers.
      </p>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Installation</h2>

      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">Node.js</h3>

      <pre class="bg-gray-800 text-green-400 p-4 rounded-lg overflow-x-auto mb-4"><code>npm install @bufferpunk/logmachine</code></pre>

      <pre class="bg-gray-800 text-green-400 p-4 rounded-lg overflow-x-auto mb-6"><code>import { LogMachine, defaultLogger } from '@bufferpunk/logmachine';</code></pre>

      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">Browser</h3>

      <pre class="bg-gray-800 text-yellow-400 p-4 rounded-lg overflow-x-auto mb-6"><code>&lt;script src="https://cdn.socket.io/4.7.5/socket.io.min.js"&gt;&lt;/script&gt;
&lt;script src="browsers.umd.js"&gt;&lt;/script&gt;</code></pre>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Basic Usage</h2>

      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">Node.js</h3>

      <pre class="bg-gray-800 text-green-400 p-4 rounded-lg overflow-x-auto mb-4"><code>import { LogMachine } from '@bufferpunk/logmachine';

const logger = new LogMachine('myapp', { debug_level: 0 });

logger.info('Hello, world!');
logger.error('An error occurred!');
logger.success('Operation completed successfully!');
logger.debug('Debugging information here.');
logger.warning('This is a warning message.');</code></pre>

      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">Browser</h3>

      <pre class="bg-gray-800 text-yellow-400 p-4 rounded-lg overflow-x-auto mb-6"><code>&lt;script&gt;
  // Use the default logger
  defaultLogger.info('Hello from the browser');

  // Or create your own instance
  const lm = new LogMachine('my_logger', {
    debug_level: 0,
    central: {
      url: 'https://logmachine.org',
      room: 'public',
    },
  });

  lm.success('All green!', window.location.pathname);
  lm.error('Something went wrong', window.location.pathname);
&lt;/script&gt;</code></pre>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Central Logging</h2>

      <p class="text-gray-600 dark:text-gray-400 mb-4">
        Connect to a central LogMachine server for collaborative logging.
        Your logs will be visible to team members in real-time.
      </p>

      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">Using Default Logger</h3>

      <pre class="bg-gray-800 text-green-400 p-4 rounded-lg overflow-x-auto mb-4"><code>import { defaultLogger } from '@bufferpunk/logmachine';

const logger = defaultLogger;
logger.info('This log is sent to the LogMachine central server!');</code></pre>

      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">Custom Configuration</h3>

      <pre class="bg-gray-800 text-green-400 p-4 rounded-lg overflow-x-auto mb-6"><code>const logger = new LogMachine('with_central', {
  debug_level: 0,
  central: {
    url: 'https://your-server.com',      // Base server URL
    room: 'team_alpha',                   // Your organization or room
    endpoint: '/api/logs',                // Optional, defaults to /api/logs
    headers: { 'Authorization': 'Bearer token' },
    socketio: true,                       // Use Socket.IO instead of HTTP
    socketio_path: '/api/socket.io/',     // Optional
    withCredentials: false,               // Optional CORS
  },
});

logger.success('Central logging is working!');</code></pre>

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
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">number</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">0</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Console output level (0=all, 1=ERROR, 2=SUCCESS, etc.)</td>
            </tr>
            <tr class="bg-gray-50 dark:bg-gray-700">
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>log_file</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">string</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">"logs.log"</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">File to save all logs (Node.js only)</td>
            </tr>
            <tr>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>error_file</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">string</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">"errors.log"</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">File to save error logs (Node.js only)</td>
            </tr>
            <tr class="bg-gray-50 dark:bg-gray-700">
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>central</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">object</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">null</td>
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

      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">Custom Log Levels</h3>

      <pre class="bg-gray-800 text-green-400 p-4 rounded-lg overflow-x-auto mb-4"><code>logger.addLevel('CRITICAL_HACK', 60, '#ff00ff');
logger.addLevel('DEPLOYMENT', 35, '#ff8800');

logger.critical_hack('Zero day vulnerability found!');
logger.deployment('Application deployed to production');</code></pre>

      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">JSON Export</h3>

      <pre class="bg-gray-800 text-green-400 p-4 rounded-lg overflow-x-auto mb-4"><code>// Get logs as JSON objects (Node.js only)
const jsonLogs = logger.jsonifier();
jsonLogs.forEach(logEntry => {
  console.log(logEntry); // Each entry is a JSON string
});</code></pre>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Log Output Format</h2>

      <div class="bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg p-6 mb-6">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">Console Output (with colors)</h3>
        <pre class="text-gray-800 dark:text-gray-200"><code>(username @ myapp) 🤌 CL Timing: [ 2024-01-15T10:30:45.123Z ]
[ INFO ] Server started on port 8000
🏁</code></pre>
      </div>

      <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6">
        <h3 class="text-lg font-semibold text-blue-800 dark:text-blue-200 mb-2">📚 Resources</h3>
        <ul class="text-blue-700 dark:text-blue-300 space-y-1">
          <li><a href="https://github.com/logmachine/js" class="underline hover:no-underline">GitHub Repository</a></li>
          <li><a href="https://www.npmjs.com/package/@bufferpunk/logmachine" class="underline hover:no-underline">NPM Package</a></li>
          <li><a href="https://logmachine.org" class="underline hover:no-underline">Log Machine</a></li>
        </ul>
      </div>
    </div>
  </div>
</template>