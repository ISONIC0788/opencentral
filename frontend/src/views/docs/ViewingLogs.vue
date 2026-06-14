<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-8">
    <div class="prose dark:prose-invert max-w-none">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-6">Viewing Logs</h1>

      <p class="text-lg text-gray-600 dark:text-gray-400 mb-8">
        LogMachine logs can be viewed in three ways depending on your workflow.
        Use the CLI for quick inspection, the web UI for collaboration, or an ANSI-aware file viewer if you prefer reading from files.
      </p>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div class="bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg p-5">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">1. CLI output</h2>
          <p class="text-gray-600 dark:text-gray-400 mb-3">
            Use standard terminal commands to inspect your log file directly.
          </p>
          <pre class="bg-gray-800 text-green-400 p-3 rounded-md text-sm overflow-x-auto"><code>tail -f logs.log
cat logs.log
less -R logs.log</code></pre>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-3">
            `less -R` is useful when you want to preserve ANSI colors in the terminal.
          </p>
        </div>

        <div class="bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg p-5">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">2. Web UI</h2>
          <p class="text-gray-600 dark:text-gray-400 mb-3">
            Open the central app, join a room, and watch logs stream in live.
          </p>
          <p class="text-sm text-gray-500 dark:text-gray-400">
            Best for team debugging, filtering, and collaborative triage.
          </p>
          <div class="mt-4">
            <router-link to="/docs/setup" class="text-blue-600 dark:text-blue-400 underline text-sm">
              See central server setup →
            </router-link>
          </div>
        </div>

        <div class="bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg p-5">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">3. In file</h2>
          <p class="text-gray-600 dark:text-gray-400 mb-3">
            If you prefer viewing logs in files, install an ANSI viewer extension or plugin for your IDE.
          </p>
          <p class="text-sm text-gray-500 dark:text-gray-400">
            This keeps colors readable while avoiding raw escape codes.
          </p>
        </div>
      </div>

      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Recommended ANSI Viewers</h2>

      <div class="space-y-4 mb-8">
        <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-5">
          <h3 class="text-lg font-semibold text-blue-900 dark:text-blue-100 mb-2">VS Code</h3>
          <p class="text-blue-800 dark:text-blue-200 mb-2">
            <a href="https://marketplace.visualstudio.com/items?itemName=eric-blanquer.ansi-automatic-clean-viewer" class="underline">ANSI Automatic Clean Viewer</a>
          </p>
          <p class="text-sm text-blue-800 dark:text-blue-200">
            Automatically hides ANSI escape codes, preserves colors, and handles large files smoothly.
          </p>
        </div>

        <div class="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-5">
          <h3 class="text-lg font-semibold text-green-900 dark:text-green-100 mb-2">Vim / Neovim</h3>
          <p class="text-green-800 dark:text-green-200 mb-2">
            <strong>AnsiEsc.vim</strong> for ANSI-aware viewing inside Vim, or <strong>nvimpager</strong> for quick terminal-based viewing.
          </p>
          <p class="text-sm text-green-800 dark:text-green-200">
            Good choice if you already work inside terminal editors and want logs to render with color.
          </p>
        </div>

        <div class="bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-800 rounded-lg p-5">
          <h3 class="text-lg font-semibold text-purple-900 dark:text-purple-100 mb-2">Emacs</h3>
          <p class="text-purple-800 dark:text-purple-200 mb-2">
            Use the built-in <strong>ansi-color</strong> package.
          </p>
          <p class="text-sm text-purple-800 dark:text-purple-200">
            It applies ANSI colors directly in buffers and is a reliable built-in option.
          </p>
        </div>

        <div class="bg-orange-50 dark:bg-orange-900/20 border border-orange-200 dark:border-orange-800 rounded-lg p-5">
          <h3 class="text-lg font-semibold text-orange-900 dark:text-orange-100 mb-2">JetBrains IDEs</h3>
          <p class="text-orange-800 dark:text-orange-200 mb-2">
            Use the built-in ANSI support in the Run/Debug console or terminal output.
          </p>
          <p class="text-sm text-orange-800 dark:text-orange-200">
            Built-in support is usually enough for viewing colored log output without extra plugins.
          </p>
        </div>
      </div>

      <div class="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-6">
        <h3 class="text-lg font-semibold text-yellow-800 dark:text-yellow-200 mb-2">Tip</h3>
        <p class="text-yellow-700 dark:text-yellow-300">
          If you are working from the terminal, <code>tail -f</code> is the fastest way to watch live logs, while <code>less -R</code> is better when you need to scroll through colored history.
        </p>
      </div>
    </div>
  </div>
</template>