<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-8">
    <div class="prose dark:prose-invert max-w-none">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-6">PHP SDK</h1>

      <p class="text-lg text-gray-600 dark:text-gray-400 mb-8">
        The LogMachine PHP SDK provides structured logging for PHP applications,
        with colored console output, JSON formatting, and optional log forwarding to central servers.
      </p>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Installation</h2>

      <pre class="bg-gray-800 text-green-400 p-4 rounded-lg overflow-x-auto mb-6"><code>composer require bufferpunk/logmachine</code></pre>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Basic Usage</h2>

      <pre class="bg-gray-800 text-green-400 p-4 rounded-lg overflow-x-auto mb-6"><code>&lt;?php

require __DIR__ . '/vendor/autoload.php';

use Bufferpunk\Logmachine\LogMachine;

// Load config (example: config/logmachine.php)
$config = require __DIR__ . '/config/logmachine.php';

// Create logger instance
$logger = LogMachine::create($config);

// Log messages
$logger-&gt;debug('Debug message');
$logger-&gt;info('User logged in', ['user' =&gt; 'jdoe']);
$logger-&gt;warning('API rate limit approaching');
$logger-&gt;error('Database connection failed', ['host' =&gt; 'localhost']);
$logger-&gt;success('Operation completed successfully!');

?&gt;</code></pre>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Configuration</h2>

      <p class="text-gray-600 dark:text-gray-400 mb-4">
        Create a configuration file (e.g., <code>config/logmachine.php</code>) with your settings:
      </p>

      <pre class="bg-gray-800 text-green-400 p-4 rounded-lg overflow-x-auto mb-6"><code>&lt;?php

return [

    'log_file' =&gt; __DIR__ . '/logs/all_logs.log',
    'error_file' =&gt; __DIR__ . '/logs/error_logs.log',
    'transport_error_file' =&gt; __DIR__ . '/logs/transport-error.log',

    /*
    |--------------------------------------------------------------------------
    | Local Logger Settings
    |--------------------------------------------------------------------------
    */
    'local' =&gt; [
        'color' =&gt; true,
        'emoji' =&gt; true,
    ],

    /*
    |--------------------------------------------------------------------------
    | Central Logging Settings
    |--------------------------------------------------------------------------
    */
    'central' =&gt; [
        'http_enabled'    =&gt; false,
        'url'             =&gt; 'https://logmachine.org',
        'room'            =&gt; null,
        'headers'         =&gt; [
            // 'Authorization' =&gt; 'Bearer YOUR_TOKEN_HERE',
        ],
        'timeout'         =&gt; 30,
        'connect_timeout' =&gt; 10,
        'verify_ssl'      =&gt; true,
        'user_agent'      =&gt; 'LogMachine-Client/1.0',
    ],

];</code></pre>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Central Logging</h2>

      <p class="text-gray-600 dark:text-gray-400 mb-4">
        Enable central logging to forward logs to a LogMachine server for collaborative debugging.
      </p>

      <pre class="bg-gray-800 text-green-400 p-4 rounded-lg overflow-x-auto mb-6"><code>'central' =&gt; [
    'http_enabled'    =&gt; true,
    'url'             =&gt; 'https://logmachine.org',
    'room'            =&gt; 'my_app_room',
    'user'            =&gt; 'your_username',      // optional
    'module'          =&gt; 'backend_api',        // optional
    'headers'         =&gt; [
        'Authorization' =&gt; 'Bearer YOUR_TOKEN_HERE',
    ],
],</code></pre>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Configuration Options</h2>

      <div class="overflow-x-auto mb-6">
        <table class="min-w-full bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600">
          <thead>
            <tr class="bg-gray-50 dark:bg-gray-700">
              <th class="px-4 py-2 border border-gray-300 dark:border-gray-600 text-left text-gray-900 dark:text-white">Option</th>
              <th class="px-4 py-2 border border-gray-300 dark:border-gray-600 text-left text-gray-900 dark:text-white">Type</th>
              <th class="px-4 py-2 border border-gray-300 dark:border-gray-600 text-left text-gray-900 dark:text-white">Default</th>
              <th class="px-4 py-2 border border-gray-300 dark:border-gray-600 text-left text-gray-900 dark:text-white">Description</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>channel</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">string</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">"logmachine"</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Logger channel name</td>
            </tr>
            <tr class="bg-gray-50 dark:bg-gray-700">
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>level</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">int</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">DEBUG</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Minimum log level to output</td>
            </tr>
            <tr>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>log_file</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">string</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">null</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Path to general log file</td>
            </tr>
            <tr class="bg-gray-50 dark:bg-gray-700">
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>error_file</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">string</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">null</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Path to error-only log file</td>
            </tr>
            <tr>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>transport_error_file</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">string</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">null</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Path for transport error logs</td>
            </tr>
            <tr class="bg-gray-50 dark:bg-gray-700">
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>http_retries</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">int</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">2</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Retries for failed HTTP requests</td>
            </tr>
            <tr>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>http_retry_delay</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">int</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">1</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Delay between HTTP retries (seconds)</td>
            </tr>
            <tr class="bg-gray-50 dark:bg-gray-700">
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>central</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">array</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">null</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Remote log forwarding config</td>
            </tr>
          </tbody>
        </table>
      </div>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Log Levels</h2>

      <div class="overflow-x-auto mb-6">
        <table class="min-w-full bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600">
          <thead>
            <tr class="bg-gray-50 dark:bg-gray-700">
              <th class="px-4 py-2 border border-gray-300 dark:border-gray-600 text-left text-gray-900 dark:text-white">Level</th>
              <th class="px-4 py-2 border border-gray-300 dark:border-gray-600 text-left text-gray-900 dark:text-white">Description</th>
              <th class="px-4 py-2 border border-gray-300 dark:border-gray-600 text-left text-gray-900 dark:text-white">Method</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>DEBUG</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Detailed debug information</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>$logger-&gt;debug()</code></td>
            </tr>
            <tr class="bg-gray-50 dark:bg-gray-700">
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>INFO</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">General application events</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>$logger-&gt;info()</code></td>
            </tr>
            <tr>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>NOTICE</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Normal but significant conditions</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>$logger-&gt;notice()</code></td>
            </tr>
            <tr class="bg-gray-50 dark:bg-gray-700">
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>WARNING</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Warnings that require attention</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>$logger-&gt;warning()</code></td>
            </tr>
            <tr>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>ERROR</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Runtime errors</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>$logger-&gt;error()</code></td>
            </tr>
            <tr class="bg-gray-50 dark:bg-gray-700">
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>CRITICAL</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Critical conditions</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>$logger-&gt;critical()</code></td>
            </tr>
            <tr>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>ALERT</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Immediate action required</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>$logger-&gt;alert()</code></td>
            </tr>
            <tr class="bg-gray-50 dark:bg-gray-700">
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>EMERGENCY</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">System unusable</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>$logger-&gt;emergency()</code></td>
            </tr>
            <tr>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>SUCCESS</code></td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600">Successful operations</td>
              <td class="px-4 py-2 border border-gray-300 dark:border-gray-600"><code>$logger-&gt;success()</code></td>
            </tr>
          </tbody>
        </table>
      </div>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Log Output Format</h2>

      <div class="bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg p-6 mb-6">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">CLI Output (with colors and emojis)</h3>
        <pre class="text-gray-800 dark:text-gray-200"><code>[2024-01-15T10:30:45 UTC] [DEBUG] Debug message
[2024-01-15T10:30:46 UTC] [INFO]  User logged in  {"user":"jdoe"}
[2024-01-15T10:30:47 UTC] [WARNING] API rate limit approaching
[2024-01-15T10:30:48 UTC] [ERROR]   Database connection failed  {"host":"localhost"}</code></pre>
      </div>

      <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6">
        <h3 class="text-lg font-semibold text-blue-800 dark:text-blue-200 mb-2">📚 Resources</h3>
        <ul class="text-blue-700 dark:text-blue-300 space-y-1">
          <li><a href="https://github.com/logmachine/php" class="underline hover:no-underline">GitHub Repository</a></li>
          <li><a href="https://packagist.org/packages/bufferpunk/logmachine" class="underline hover:no-underline">Packagist Package</a></li>
          <li><a href="https://logmachine.org" class="underline hover:no-underline">Log Machine</a></li>
        </ul>
      </div>
    </div>
  </div>
</template>
