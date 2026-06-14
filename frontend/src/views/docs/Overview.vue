<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-8">
    <div class="prose dark:prose-invert max-w-none">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-6">LogMachine Documentation</h1>

      <p class="text-lg text-gray-600 dark:text-gray-400 mb-8">
        Welcome to LogMachine, a collaborative logging system designed for distributed developers.
        This documentation will help you get started with setting up and using LogMachine across different programming languages.
      </p>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div class="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 p-6 rounded-lg border border-blue-200 dark:border-blue-800">
          <h3 class="text-xl font-semibold text-blue-900 dark:text-blue-100 mb-3">Quick Start</h3>
          <p class="text-blue-800 dark:text-blue-200 mb-4">
            Get up and running with LogMachine in minutes. Choose your language and start logging collaboratively.
          </p>
          <a
            href="https://logmachine.org/docs/setup"
            class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Setup Guide →
          </a>
        </div>

        <div class="bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 p-6 rounded-lg border border-green-200 dark:border-green-800">
          <h3 class="text-xl font-semibold text-green-900 dark:text-green-100 mb-3">SDKs</h3>
          <p class="text-green-800 dark:text-green-200 mb-4">
            LogMachine supports multiple programming languages. Find your SDK below.
          </p>
          <div class="flex flex-wrap gap-2">
            <router-link to="/docs/python" class="px-3 py-1 bg-green-100 dark:bg-green-800 text-green-800 dark:text-green-200 rounded text-sm hover:bg-green-200 dark:hover:bg-green-700 transition-colors">Python</router-link>
            <router-link to="/docs/javascript" class="px-3 py-1 bg-green-100 dark:bg-green-800 text-green-800 dark:text-green-200 rounded text-sm hover:bg-green-200 dark:hover:bg-green-700 transition-colors">JavaScript</router-link>
            <router-link to="/docs/go" class="px-3 py-1 bg-green-100 dark:bg-green-800 text-green-800 dark:text-green-200 rounded text-sm hover:bg-green-200 dark:hover:bg-green-700 transition-colors">Go</router-link>
            <router-link to="/docs/rust" class="px-3 py-1 bg-green-100 dark:bg-green-800 text-green-800 dark:text-green-200 rounded text-sm hover:bg-green-200 dark:hover:bg-green-700 transition-colors">Rust</router-link>
            <router-link to="/docs/php" class="px-3 py-1 bg-green-100 dark:bg-green-800 text-green-800 dark:text-green-200 rounded text-sm hover:bg-green-200 dark:hover:bg-green-700 transition-colors">PHP</router-link>
          </div>
        </div>
      </div>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">What is LogMachine?</h2>

      <p class="text-gray-600 dark:text-gray-400 mb-6">
        LogMachine is a powerful logging platform that enables teams to collaborate on debugging and monitoring.
        Unlike traditional logging systems that store logs locally, LogMachine centralizes logs in real-time,
        allowing team members to see each other's logs instantly.
      </p>

      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">Key Features</h3>

      <ul class="list-disc list-inside text-gray-600 dark:text-gray-400 space-y-2 mb-6">
        <li><strong>Real-time Collaboration:</strong> See team members' logs as they happen</li>
        <li><strong>Multi-language Support:</strong> SDKs for Python, JavaScript, Go, Rust, and PHP</li>
        <li><strong>Centralized Storage:</strong> All logs in one place with powerful search and filtering</li>
        <li><strong>Beautiful Interface:</strong> Color-coded logs with user identification</li>
        <li><strong>Flexible Transport:</strong> HTTP and WebSocket support for different environments</li>
        <li><strong>Privacy Controls:</strong> Room-based organization for different projects</li>
      </ul>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Getting Started</h2>

      <ol class="list-decimal list-inside text-gray-600 dark:text-gray-400 space-y-3 mb-6">
        <li><strong>Setup a Central Server:</strong> Deploy or use the hosted LogMachine server</li>
        <li><strong>Choose Your SDK:</strong> Install the LogMachine SDK for your programming language</li>
        <li><strong>Configure Logging:</strong> Point your application to the central server</li>
        <li><strong>Start Logging:</strong> Use familiar logging methods with collaborative features</li>
        <li><strong>Monitor & Debug:</strong> View logs in real-time with your team</li>
      </ol>

      <p class="text-gray-600 dark:text-gray-400 mb-8">
        See the dedicated <router-link to="/docs/viewing-logs" class="text-blue-600 dark:text-blue-400 underline">Viewing Logs</router-link> page for CLI, web UI, and file-based viewing options.
      </p>

      <div class="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-6">
        <h3 class="text-lg font-semibold text-yellow-800 dark:text-yellow-200 mb-2">💡 Pro Tip</h3>
        <p class="text-yellow-700 dark:text-yellow-300">
          Start with the default hosted server at <code class="bg-yellow-100 dark:bg-yellow-800 px-2 py-1 rounded">https://logmachine.org</code>
          to try LogMachine without setting up your own infrastructure.
        </p>
      </div>
    </div>
  </div>
</template>
