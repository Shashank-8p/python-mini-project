/**
 * playground-worker.js  –  Pyodide Web Worker
 *
 * Runs on a dedicated thread so the main UI thread is NEVER blocked.
 * Terminating this worker (via worker.terminate()) is the stop mechanism:
 * it kills execution instantly, even inside an infinite loop.
 *
 * Message protocol (main → worker)
 * ─────────────────────────────────
 *  { type: 'run', code: '<python source>' }
 *
 * Message protocol (worker → main)
 * ─────────────────────────────────
 *  { type: 'ready'                           }  – Pyodide loaded OK
 *  { type: 'load-error', message: '...'      }  – Pyodide failed to load
 *  { type: 'done',  stdout: '...', stderr: '...' }  – run finished cleanly
 *  { type: 'error', message: '...'           }  – Python raised an exception
 */

'use strict';

var PYODIDE_VERSION = '0.26.2';
var PYODIDE_CDN     = 'https://cdn.jsdelivr.net/pyodide/v' + PYODIDE_VERSION + '/full/';

importScripts(PYODIDE_CDN + 'pyodide.js');

var pyodide = null;   // set once loadPyodide() resolves

/* ── Boot Pyodide as soon as the worker starts ── */
async function init() {
    try {
        pyodide = await loadPyodide({ indexURL: PYODIDE_CDN });

        /* Wire stdout / stderr to StringIO buffers */
        pyodide.runPython(
            'import sys, io\n' +
            'sys.stdout = io.StringIO()\n' +
            'sys.stderr = io.StringIO()\n'
        );

        self.postMessage({ type: 'ready' });

    } catch (err) {
        self.postMessage({
            type    : 'load-error',
            message : err.message || String(err)
        });
    }
}

/* ── Handle run requests from the main thread ── */
self.onmessage = async function (e) {
    if (e.data.type !== 'run') return;

    /* Clear buffers before each execution */
    try {
        pyodide.runPython(
            'try:\n' +
            '    sys.stdout.seek(0); sys.stdout.truncate(0)\n' +
            '    sys.stderr.seek(0); sys.stderr.truncate(0)\n' +
            'except Exception:\n' +
            '    import io\n' +
            '    sys.stdout = io.StringIO()\n' +
            '    sys.stderr = io.StringIO()\n'
        );
    } catch (_) { /* swallow — output will still be captured */ }

    try {
        await pyodide.runPythonAsync(e.data.code);

        var stdout = pyodide.runPython('sys.stdout.getvalue()');
        var stderr = pyodide.runPython('sys.stderr.getvalue()');

        self.postMessage({ type: 'done', stdout: stdout, stderr: stderr });

    } catch (err) {
        /* Pyodide wraps Python tracebacks in the JS error message */
        self.postMessage({ type: 'error', message: err.message || String(err) });
    }
};

init();