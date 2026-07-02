<template>
  <div class="bg-[#ffffff] dark:bg-[#000000] border border-neutral-200/80 dark:border-neutral-800/80 rounded-md p-8 shadow-none">
    <div class="prose dark:prose-invert max-w-none">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-6">LogMachine Documentation</h1>

      <p class="text-lg text-gray-600 dark:text-gray-400 mb-8">
        Welcome to LogMachine, a collaborative logging system designed for distributed developers.
        This documentation will help you get started with setting up and using LogMachine across different programming languages.
      </p>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div class="bg-[#ffffff] dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800 p-6 rounded-md">
          <h3 class="text-xl font-semibold text-[#171717] dark:text-[#ffffff] mb-3">Quick Start</h3>
          <p class="text-[#171717] dark:text-[#ffffff] mb-4">
            Get up and running with LogMachine in minutes. Choose your language and start logging collaboratively.
          </p>
          <a
            href="https://logmachine.org/docs/setup"
            class="inline-flex items-center px-4 py-2 bg-[#171717] text-[#ffffff] dark:bg-[#ffffff] dark:text-[#000000] hover:bg-neutral-800 dark:hover:bg-neutral-100 rounded-md text-sm font-medium transition-colors"
          >
            Setup Guide →
          </a>
        </div>

        <div class="bg-[#ffffff] dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800 p-6 rounded-md">
          <h3 class="text-xl font-semibold text-[#171717] dark:text-[#ffffff] mb-3">SDKs</h3>
          <p class="text-[#171717] dark:text-[#ffffff] mb-4">
            LogMachine supports multiple programming languages. Find your SDK below.
          </p>
          <div class="flex flex-wrap gap-2">
            <router-link to="/docs/python" class="px-3 py-1 bg-neutral-100 hover:bg-neutral-200/80 dark:bg-neutral-900 dark:hover:bg-neutral-800 text-[#171717] dark:text-[#ffffff] rounded-md text-sm font-medium transition-colors border border-neutral-200/50 dark:border-neutral-700/50">Python</router-link>
            <router-link to="/docs/javascript" class="px-3 py-1 bg-neutral-100 hover:bg-neutral-200/80 dark:bg-neutral-900 dark:hover:bg-neutral-800 text-[#171717] dark:text-[#ffffff] rounded-md text-sm font-medium transition-colors border border-neutral-200/50 dark:border-neutral-700/50">JavaScript</router-link>
            <router-link to="/docs/go" class="px-3 py-1 bg-neutral-100 hover:bg-neutral-200/80 dark:bg-neutral-900 dark:hover:bg-neutral-800 text-[#171717] dark:text-[#ffffff] rounded-md text-sm font-medium transition-colors border border-neutral-200/50 dark:border-neutral-700/50">Go</router-link>
            <router-link to="/docs/rust" class="px-3 py-1 bg-neutral-100 hover:bg-neutral-200/80 dark:bg-neutral-900 dark:hover:bg-neutral-800 text-[#171717] dark:text-[#ffffff] rounded-md text-sm font-medium transition-colors border border-neutral-200/50 dark:border-neutral-700/50">Rust</router-link>
            <router-link to="/docs/php" class="px-3 py-1 bg-neutral-100 hover:bg-neutral-200/80 dark:bg-neutral-900 dark:hover:bg-neutral-800 text-[#171717] dark:text-[#ffffff] rounded-md text-sm font-medium transition-colors border border-neutral-200/50 dark:border-neutral-700/50">PHP</router-link>
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

      <div class="bg-neutral-50 dark:bg-neutral-900/40 border border-neutral-200 dark:border-neutral-800 rounded-md p-6">
        <h3 class="text-lg font-semibold text-[#171717] dark:text-[#ffffff] mb-2">💡 Pro Tip</h3>
        <p class="text-neutral-600 dark:text-neutral-300">
          Start with the default hosted server at <code class="bg-neutral-100 dark:bg-neutral-800 text-neutral-800 dark:text-neutral-200 rounded-md px-2 py-1">https://logmachine.org</code>
          to try LogMachine without setting up your own infrastructure.
        </p>
      </div>
    </div>
  </div>
</template>
