/**
 * Root component. For now it only shows whether the frontend can reach the backend;
 * routing and real pages replace this in later phases.
 */
import { useEffect, useState } from 'react';

import { fetchHealth } from './api/health';

/** The three states of a request: still waiting, succeeded, or failed. */
type ApiStatus =
  { kind: 'loading' } | { kind: 'ok'; environment: string } | { kind: 'error'; message: string };

/** Render the app name and the result of one call to `GET /api/health`. */
export default function App() {
  const [apiStatus, setApiStatus] = useState<ApiStatus>({ kind: 'loading' });

  useEffect(() => {
    // StrictMode runs effects twice in development; this flag stops the first,
    // discarded run from updating state after React has thrown it away.
    let ignore = false;
    fetchHealth()
      .then((health) => {
        if (!ignore) setApiStatus({ kind: 'ok', environment: health.environment });
      })
      .catch((error: unknown) => {
        if (!ignore) setApiStatus({ kind: 'error', message: String(error) });
      });
    return () => {
      ignore = true;
    };
  }, []);

  return (
    <main className="mx-auto flex min-h-dvh max-w-xl flex-col justify-center px-6 py-16">
      <p className="text-xs tracking-[0.2em] text-muted uppercase">Workout planner</p>
      <h1 className="mt-3 text-5xl font-medium">Exercive</h1>
      <hr className="my-8 border-line" />

      {/* aria-live: screen readers announce the text when the status changes. */}
      <section aria-live="polite" className="rounded-sm border border-line bg-surface p-5">
        <h2 className="font-sans text-xs tracking-[0.2em] text-muted uppercase">API status</h2>
        {apiStatus.kind === 'loading' && <p className="mt-2 text-muted">Checking the API…</p>}
        {apiStatus.kind === 'ok' && (
          <p className="mt-2 flex items-center gap-2">
            <span aria-hidden="true" className="size-2 rounded-full bg-accent" />
            Connected ({apiStatus.environment})
          </p>
        )}
        {apiStatus.kind === 'error' && (
          <p className="mt-2 rounded-sm bg-danger px-3 py-2">
            API unreachable: {apiStatus.message}
          </p>
        )}
      </section>
    </main>
  );
}
