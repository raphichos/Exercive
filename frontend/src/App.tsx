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
    <main>
      <h1>Exercive</h1>
      {apiStatus.kind === 'loading' && <p>Checking the API…</p>}
      {apiStatus.kind === 'ok' && <p>API: ok ({apiStatus.environment})</p>}
      {apiStatus.kind === 'error' && <p>API unreachable: {apiStatus.message}</p>}
    </main>
  );
}
