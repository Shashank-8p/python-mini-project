/**
 * playground.js  –  Python Playground powered by Pyodide
 *
 * Architecture
 * ─────────────────────────────────────────────────────────────────
 *  • Pyodide runs inside a Web Worker (playground-worker.js)
 *    so the main thread / UI is NEVER blocked.
 *
 *  • Stop works by calling worker.terminate(), which kills the
 *    worker thread instantly — even during an infinite loop.
 *    A fresh worker is then spawned automatically so the user
 *    can run again without a page reload. Pyodide reloads (~8 MB).
 *
 *  • window.PYODIDE      – lightweight status object (ready / loading)
 *  • window.playgroundAPI – consumed by main.js for tab show/hide
 *
 * Zero conflicts with the modal system or existing project scripts.
 */
(function () {
    'use strict';

    /* ================================================================
       1.  LIGHTWEIGHT STATUS OBJECT
       Kept on window so external scripts can check readiness.
       The actual Pyodide instance now lives in the worker thread.
    ================================================================ */
    window.PYODIDE = {
        ready  : false,   // true once the worker signals 'ready'
        loading: false    // true while the worker is booting
    };

    /* ================================================================
       2.  CONSTANTS
    ================================================================ */
    var WORKER_SCRIPT = 'js/playground-worker.js';

    /* ================================================================
       3.  EXAMPLE CODE SNIPPETS
    ================================================================ */
    var EXAMPLES = [
        /* 0 – Hello World */
        '# \uD83D\uDC4B Hello, Python Playground!\n' +
        'name = "World"\n' +
        'greeting = f"Hello, {name}!"\n' +
        'print(greeting)\n\n' +
        'for i in range(1, 6):\n' +
        '    print("  " + "\u2B50" * i)',

        /* 1 – Fibonacci */
        '# \uD83D\uDD22 Fibonacci Sequence\n' +
        'def fibonacci(n):\n' +
        '    a, b = 0, 1\n' +
        '    result = []\n' +
        '    for _ in range(n):\n' +
        '        result.append(a)\n' +
        '        a, b = b, a + b\n' +
        '    return result\n\n' +
        'fibs = fibonacci(15)\n' +
        'print("Fibonacci (first 15):", fibs)\n' +
        'print("Sum:", sum(fibs))',

        /* 2 – Sieve of Eratosthenes */
        '# \uD83D\uDD0D Sieve of Eratosthenes\n' +
        'def sieve(limit):\n' +
        '    is_prime = [True] * (limit + 1)\n' +
        '    is_prime[0] = is_prime[1] = False\n' +
        '    for i in range(2, int(limit ** 0.5) + 1):\n' +
        '        if is_prime[i]:\n' +
        '            for j in range(i * i, limit + 1, i):\n' +
        '                is_prime[j] = False\n' +
        '    return [n for n in range(2, limit + 1) if is_prime[n]]\n\n' +
        'primes = sieve(50)\n' +
        'print(f"Primes up to 50 ({len(primes)} found):")\n' +
        'print(primes)',

        /* 3 – Statistics (stdlib) */
        '# \uD83D\uDCCA Basic Statistics (stdlib only)\n' +
        'import statistics\n\n' +
        'data = [23, 45, 12, 67, 34, 89, 56, 11, 78, 42]\n' +
        'print(f"Data   : {sorted(data)}")\n' +
        'print(f"Mean   : {statistics.mean(data):.2f}")\n' +
        'print(f"Median : {statistics.median(data)}")\n' +
        'print(f"Stdev  : {statistics.stdev(data):.2f}")\n' +
        'print(f"Min/Max: {min(data)} / {max(data)}")',

        /* 4 – Recursion */
        '# \uD83D\uDD04 Recursion: Factorial\n' +
        'def factorial(n):\n' +
        '    if n <= 1:\n' +
        '        return 1\n' +
        '    return n * factorial(n - 1)\n\n' +
        'for n in range(1, 11):\n' +
        '    print(f"  {n:2d}! = {factorial(n):10,}")',

        /* 5 – List comprehensions */
        '# \uD83E\uDDE9 List Comprehensions\n' +
        'words = ["banana", "apple", "cherry", "date", "elderberry", "fig"]\n\n' +
        'by_length = sorted(words, key=len)\n' +
        'print("Sorted by length:")\n' +
        'for w in by_length:\n' +
        '    bar = chr(9608) * len(w)\n' +
        '    print(f"  {bar}  {w} ({len(w)})")\n\n' +
        'palindromes = [w for w in words if w == w[::-1]]\n' +
        'print("\\nPalindromes:", palindromes or "none found")'
    ];

    var exampleIdx = 0;

    /* ================================================================
       4.  DOM REFERENCES
    ================================================================ */
    function $id(id) { return document.getElementById(id); }

    var playgroundSection = $id('playgroundSection');
    var runBtn            = $id('runCode');
    var stopBtn           = $id('stopCode');        // ← NEW
    var editor            = $id('pythonEditor');
    var consoleEl         = $id('consoleOutput');
    var statusDot         = $id('statusDot');
    var statusText        = $id('statusText');
    var clearConsoleBtn   = $id('clearConsole');
    var clearEditorBtn    = $id('clearEditor');
    var loadExampleBtn    = $id('loadExample');

    /* Guard – abort gracefully if playground HTML is absent */
    if (!playgroundSection || !runBtn || !stopBtn || !editor || !consoleEl) {
        console.warn('[playground.js] Required DOM elements not found — playground disabled.');
        return;
    }

    /* ================================================================
       5.  UI HELPER FUNCTIONS
    ================================================================ */

    /**
     * Update the status badge.
     * @param {'idle'|'loading'|'ready'|'error'} state
     * @param {string} label
     */
    function setStatus(state, label) {
        if (statusDot)  statusDot.className    = 'status-dot ' + state;
        if (statusText) statusText.textContent = label;
    }

    /** Reset the console to its initial placeholder state. */
    function resetConsole() {
        consoleEl.innerHTML =
            '<span class="pg-placeholder">' +
            '&gt;&gt;&gt; Console output will appear here\u2026' +
            '</span>';
    }

    /**
     * Append a line to the console.
     * @param {string} text
     * @param {'out'|'err'|'info'} type
     */
    function printLine(text, type) {
        var ph = consoleEl.querySelector('.pg-placeholder');
        if (ph) ph.remove();

        var colorMap = {
            out  : '#c9d1d9',
            err  : '#ff7b72',
            info : '#79c0ff'
        };
        var span          = document.createElement('span');
        span.style.color      = colorMap[type] || colorMap.out;
        span.style.display    = 'block';
        span.style.whiteSpace = 'pre-wrap';
        span.style.wordBreak  = 'break-word';
        span.textContent      = text;

        consoleEl.appendChild(span);
        consoleEl.scrollTop = consoleEl.scrollHeight;
    }

    /**
     * Switch the toolbar between Run-mode and Running-mode.
     * Run mode  : Run button enabled, Stop button disabled.
     * Running   : Stop button enabled, Run button disabled.
     * @param {boolean} running
     */
    function setRunning(running) {
        runBtn.disabled = running;

        
        stopBtn.disabled = !running;
        stopBtn.style.opacity = running ? '1' : '0.5';
        stopBtn.style.cursor = running ? 'pointer' : 'not-allowed';
        
}

    /* ================================================================
       6.  WEB WORKER MANAGEMENT
       A new worker is created lazily on the first playground visit,
       and re-created automatically after a stop.
    ================================================================ */

    var worker = null;   // the current live worker (null if not yet started)

    /**
     * Spawn a fresh Pyodide worker.
     * Safe to call multiple times — always replaces the old worker reference.
     */
    function spawnWorker() {
        /* Tear down any existing worker before creating a replacement */
        if (worker) {
            worker.onmessage = null;
            worker.onerror   = null;
            /* Don't call terminate() here — spawnWorker() after a stop
               is called AFTER terminate() already ran in stopExecution(). */
        }

        window.PYODIDE.ready   = false;
        window.PYODIDE.loading = true;

        setStatus('loading', 'Downloading Pyodide\u2026');
        printLine(
            '\u23F3 Loading Python runtime (first load ~8 MB). ' +
            'This may take a moment on slow connections\u2026',
            'info'
        );

        runBtn.disabled = true;   /* re-enabled once worker signals 'ready' */

        worker = new Worker(WORKER_SCRIPT);

        worker.onmessage = function (e) {
            switch (e.data.type) {

                /* ── Pyodide finished loading in the worker ── */
                case 'ready':
                    window.PYODIDE.ready   = true;
                    window.PYODIDE.loading = false;
                    setStatus('ready', 'Pyodide Ready \u2713');
                    printLine(
                        '\u2705 Python is ready \u2014 write some code and press Run Code!',
                        'info'
                    );
                    runBtn.disabled = false;
                    break;

                /* ── Pyodide failed to load ── */
                case 'load-error':
                    window.PYODIDE.loading = false;
                    setStatus('error', 'Load failed \u2717');
                    printLine('\u274C Pyodide failed to load: ' + e.data.message, 'err');
                    break;

                /* ── Python ran and finished cleanly ── */
                case 'done':
                    if (e.data.stdout) printLine(e.data.stdout.trimEnd(), 'out');
                    if (e.data.stderr) printLine(e.data.stderr.trimEnd(), 'err');
                    if (!e.data.stdout && !e.data.stderr) printLine('(no output)', 'info');
                    setRunning(false);
                    break;

                /* ── Python raised an exception ── */
                case 'error':
                    printLine(e.data.message, 'err');
                    setRunning(false);
                    break;
            }
        };

        worker.onerror = function (err) {
            /* Catches worker-level JS errors (not Python exceptions) */
            window.PYODIDE.loading = false;
            setStatus('error', 'Worker error \u2717');
            printLine('\u274C Worker error: ' + (err.message || String(err)), 'err');
            setRunning(false);
        };
    }

    /**
     * Terminate the running worker and spin up a fresh one.
     * Called by the Stop button.
     */
    function stopExecution() {
        if (worker) {
            worker.onmessage = null;   // silence any in-flight messages
            worker.onerror   = null;
            worker.terminate();
            worker = null;
        }

        setRunning(false);
        setStatus('loading', 'Reloading Python\u2026');
        printLine(
            '\u26D4 Execution stopped. Reloading Python runtime\u2026',
            'info'
        );

        /*
         * Small delay before spawning the replacement worker.
         * Gives the browser time to fully clean up the terminated worker
         * before we allocate a new one, avoiding occasional stalls.
         */
        setTimeout(spawnWorker, 150);
    }

    /* ================================================================
       7.  RUN CODE
    ================================================================ */

    function runCode() {
        var code = editor.value;
        if (!code.trim()) {
            printLine('\u2139 Nothing to run \u2014 write some Python first!', 'info');
            return;
        }

        if (!window.PYODIDE.ready) {
            printLine('\u23F3 Python runtime is still loading \u2014 please wait\u2026', 'info');
            return;
        }

        setRunning(true);
        printLine('>>> Running\u2026', 'info');
        worker.postMessage({ type: 'run', code: code });
    }

    /* ================================================================
       8.  PUBLIC API
       Called by main.js when the user switches tabs.
    ================================================================ */

    window.playgroundAPI = {
        /**
         * Show the playground and boot the worker on the first visit.
         */
        activate: function () {
            playgroundSection.style.display = 'block';
            if (!window.PYODIDE.ready && !window.PYODIDE.loading) {
                spawnWorker();
            }
        },

        /** Hide the playground section. */
        deactivate: function () {
            playgroundSection.style.display = 'none';
        }
    };

    /* ================================================================
       9.  EVENT WIRING
    ================================================================ */

    /* Run button */
    runBtn.addEventListener('click', runCode);

    /* Stop button */
    stopBtn.addEventListener('click', stopExecution);
    

    /* Editor keyboard shortcuts */
    editor.addEventListener('keydown', function (e) {

        /* Ctrl/Cmd + Enter → run */
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            runCode();
            return;
        }

        /* Enter → new line preserving indent, extra indent after colon */
        if (e.key === 'Enter') {
            e.preventDefault();
            var start       = editor.selectionStart;
            var value       = editor.value;
            var lineStart   = value.lastIndexOf('\n', start - 1) + 1;
            var currentLine = value.substring(lineStart, start);
            var indentMatch = currentLine.match(/^\s*/);
            var indent      = indentMatch ? indentMatch[0] : '';
            if (currentLine.trimEnd().endsWith(':')) {
                indent += '    ';
            }
            var insertion = '\n' + indent;
            editor.value =
                value.substring(0, start) +
                insertion +
                value.substring(editor.selectionEnd);
            editor.selectionStart = editor.selectionEnd = start + insertion.length;
            return;
        }

        /* Tab → insert 4 spaces (no focus change) */
        if (e.key === 'Tab') {
            e.preventDefault();
            var start  = editor.selectionStart;
            var end    = editor.selectionEnd;
            var spaces = '    ';
            editor.value =
                editor.value.substring(0, start) +
                spaces +
                editor.value.substring(end);
            editor.selectionStart = editor.selectionEnd = start + spaces.length;
        }
    });

    /* Clear console */
    if (clearConsoleBtn) {
        clearConsoleBtn.addEventListener('click', resetConsole);
    }

    /* Clear editor */
    if (clearEditorBtn) {
        clearEditorBtn.addEventListener('click', function () {
            editor.value = '';
            editor.focus();
        });
    }

    /* Cycle through built-in example snippets */
    if (loadExampleBtn) {
        loadExampleBtn.addEventListener('click', function () {
            editor.value = EXAMPLES[exampleIdx % EXAMPLES.length];
            exampleIdx++;
            editor.focus();
        });
    }

    /* ================================================================
       10.  BOOT  –  set initial state
    ================================================================ */

    playgroundSection.style.display = 'none';   /* hidden until tab click */
    runBtn.disabled                 = true;       /* enabled after worker ready */
    setRunning(false);
    resetConsole();
    setStatus('idle', 'Open the tab to load Python');

}());