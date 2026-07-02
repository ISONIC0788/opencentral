<template>
  <div class="bg-[#ffffff] dark:bg-[#000000] border border-neutral-200/80 dark:border-neutral-800/80 rounded-md p-8 shadow-none">
    <div class="prose dark:prose-invert max-w-none">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-6">PHP SDK</h1>

      <p class="text-lg text-gray-600 dark:text-gray-400 mb-8">
        The LogMachine PHP SDK provides structured logging for PHP applications,
        with colored console output, JSON formatting, and optional log forwarding to central servers.
      </p>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Installation</h2>

      <pre class="bg-neutral-50 border border-neutral-200/60 text-neutral-800 dark:bg-neutral-900 dark:border-neutral-800/60 dark:text-neutral-200 p-4 rounded-md text-sm overflow-x-auto font-mono mb-6"><code>composer require bufferpunk/logmachine</code></pre>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Basic Usage</h2>

      <pre class="bg-neutral-50 border border-neutral-200/60 text-neutral-800 dark:bg-neutral-900 dark:border-neutral-800/60 dark:text-neutral-200 p-4 rounded-md text-sm overflow-x-auto font-mono mb-6"><code>&lt;?php

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

      <pre class="bg-neutral-50 border border-neutral-200/60 text-neutral-800 dark:bg-neutral-900 dark:border-neutral-800/60 dark:text-neutral-200 p-4 rounded-md text-sm overflow-x-auto font-mono mb-6"><code>&lt;?php

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
        'color' => true,
        'emoji' => true,
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

      <pre class="bg-neutral-50 border border-neutral-200/60 text-neutral-800 dark:bg-neutral-900 dark:border-neutral-800/60 dark:text-neutral-200 p-4 rounded-md text-sm overflow-x-auto font-mono mb-6"><code>'central' =&gt; [
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
        <table class="min-w-full bg-transparent border border-neutral-200 dark:border-neutral-800 text-sm">
          <thead>
            <tr>
              <th class="bg-neutral-100 dark:bg-neutral-900 px-4 py-2 border border-neutral-200 dark:border-neutral-800 font-semibold text-[#171717] dark:text-[#ffffff] text-left">Option</th>
              <th class="bg-neutral-100 dark:bg-neutral-900 px-4 py-2 border border-neutral-200 dark:border-neutral-800 font-semibold text-[#171717] dark:text-[#ffffff] text-left">Type</th>
              <th class="bg-neutral-100 dark:bg-neutral-900 px-4 py-2 border border-neutral-200 dark:border-neutral-800 font-semibold text-[#171717] dark:text-[#ffffff] text-left">Default</th>
              <th class="bg-neutral-100 dark:bg-neutral-900 px-4 py-2 border border-neutral-200 dark:border-neutral-800 font-semibold text-[#171717] dark:text-[#ffffff] text-left">Description</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>channel</code></td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">string</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">"logmachine"</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">Logger channel name</td>
            </tr>
            <tr class="bg-neutral-50/50 dark:bg-neutral-900/40">
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>level</code></td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">int</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">DEBUG</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">Minimum log level to output</td>
            </tr>
            <tr>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>log_file</code></td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">string</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">null</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">Path to general log file</td>
            </tr>
            <tr class="bg-neutral-50/50 dark:bg-neutral-900/40">
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>error_file</code></td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">string</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">null</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">Path to error-only log file</td>
            </tr>
            <tr>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>transport_error_file</code></td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">string</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">null</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">Path for transport error logs</td>
            </tr>
            <tr class="bg-neutral-50/50 dark:bg-neutral-900/40">
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>http_retries</code></td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">int</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">2</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">Retries for failed HTTP requests</td>
            </tr>
            <tr>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>http_retry_delay</code></td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">int</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">1</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">Delay between HTTP retries (seconds)</td>
            </tr>
            <tr class="bg-neutral-50/50 dark:bg-neutral-900/40">
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>central</code></td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">array</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">null</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">Remote log forwarding config</td>
            </tr>
          </tbody>
        </table>
      </div>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Log Levels</h2>

      <div class="overflow-x-auto mb-6">
        <table class="min-w-full bg-transparent border border-neutral-200 dark:border-neutral-800 text-sm">
          <thead>
            <tr>
              <th class="bg-neutral-100 dark:bg-neutral-900 px-4 py-2 border border-neutral-200 dark:border-neutral-800 font-semibold text-[#171717] dark:text-[#ffffff] text-left">Level</th>
              <th class="bg-neutral-100 dark:bg-neutral-900 px-4 py-2 border border-neutral-200 dark:border-neutral-800 font-semibold text-[#171717] dark:text-[#ffffff] text-left">Description</th>
              <th class="bg-neutral-100 dark:bg-neutral-900 px-4 py-2 border border-neutral-200 dark:border-neutral-800 font-semibold text-[#171717] dark:text-[#ffffff] text-left">Method</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>DEBUG</code></td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">Detailed debug information</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>$logger-&gt;debug()</code></td>
            </tr>
            <tr class="bg-neutral-50/50 dark:bg-neutral-900/40">
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>INFO</code></td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">General application events</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>$logger-&gt;info()</code></td>
            </tr>
            <tr>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>NOTICE</code></td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">Normal but significant conditions</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>$logger-&gt;notice()</code></td>
            </tr>
            <tr class="bg-neutral-50/50 dark:bg-neutral-900/40">
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>WARNING</code></td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">Warnings that require attention</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>$logger-&gt;warning()</code></td>
            </tr>
            <tr>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>ERROR</code></td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">Runtime errors</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>$logger-&gt;error()</code></td>
            </tr>
            <tr class="bg-neutral-50/50 dark:bg-neutral-900/40">
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>CRITICAL</code></td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">Critical conditions</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>$logger-&gt;critical()</code></td>
            </tr>
            <tr>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>ALERT</code></td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">Immediate action required</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>$logger-&gt;alert()</code></td>
            </tr>
            <tr class="bg-neutral-50/50 dark:bg-neutral-900/40">
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>EMERGENCY</code></td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">System unusable</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>$logger-&gt;emergency()</code></td>
            </tr>
            <tr>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>SUCCESS</code></td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400">Successful operations</td>
              <td class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400"><code>$logger-&gt;success()</code></td>
            </tr>
          </tbody>
        </table>
      </div>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Log Output Format</h2>

      <div class="bg-neutral-50/40 dark:bg-neutral-900/20 border border-neutral-200 dark:border-neutral-800 rounded-md p-6 mb-6">
        <h3 class="text-lg font-semibold text-[#171717] dark:text-[#ffffff] mb-3">CLI Output (with colors and emojis)</h3>
        <pre class="text-gray-800 dark:text-gray-200"><code>[2024-01-15T10:30:45 UTC] [DEBUG] Debug message
[2024-01-15T10:30:46 UTC] [INFO]  User logged in  {"user":"jdoe"}
[2024-01-15T10:30:47 UTC] [WARNING] API rate limit approaching
[2024-01-15T10:30:48 UTC] [ERROR]   Database connection failed  {"host":"localhost"}</code></pre>
      </div>

      <div class="bg-neutral-50/80 dark:bg-neutral-900/30 border border-neutral-200 dark:border-neutral-800 rounded-md p-6">
        <h3 class="text-lg font-semibold text-[#171717] dark:text-[#ffffff] mb-2">📚 Resources</h3>
        <ul class="space-y-1">
          <li><a href="https://github.com/logmachine/php" class="text-neutral-800 dark:text-neutral-200 hover:text-black hover:dark:text-white underline">GitHub Repository</a></li>
          <li><a href="https://packagist.org/packages/bufferpunk/logmachine" class="text-neutral-800 dark:text-neutral-200 hover:text-black hover:dark:text-white underline">Packagist Package</a></li>
          <li><a href="https://logmachine.org" class="text-neutral-800 dark:text-neutral-200 hover:text-black hover:dark:text-white underline">Log Machine</a></li>
        </ul>
      </div>
    </div>
  </div>
</template>
