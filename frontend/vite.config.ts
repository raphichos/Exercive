/**
 * Vite configuration: the dev server, the React and Tailwind plugins, and the API proxy.
 *
 * The Tailwind plugin runs at build time: it scans our files for class names and writes
 * plain CSS for the ones it finds. No Tailwind code reaches the browser.
 *
 * The proxy forwards every request starting with `/api` to the FastAPI server. The browser
 * only ever talks to the frontend's own origin, so the login cookie added in Phase 2 counts
 * as a same-site cookie and browsers like Safari don't block it.
 */
import tailwindcss from '@tailwindcss/vite';
import react from '@vitejs/plugin-react';
import { defineConfig, loadEnv } from 'vite';

export default defineConfig(({ mode }) => {
  // Read frontend/.env* files. The empty prefix also exposes variables without VITE_,
  // which is safe here because this file runs in Node and never reaches the browser.
  const env = loadEnv(mode, process.cwd(), '');
  const apiTarget = env.API_PROXY_TARGET ?? 'http://localhost:8000';

  return {
    plugins: [react(), tailwindcss()],
    server: {
      port: 5173,
      proxy: {
        '/api': { target: apiTarget, changeOrigin: true },
      },
    },
  };
});
