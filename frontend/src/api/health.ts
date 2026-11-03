/**
 * Client for the backend's health endpoint.
 *
 * Every file in `src/api/` wraps one group of backend endpoints, so components never
 * build URLs or parse responses themselves.
 */

/** Response body of `GET /api/health`; mirrors `HealthResponse` in backend/app/schemas/health.py. */
export interface HealthResponse {
  status: 'ok';
  environment: string;
}

/**
 * Ask the backend whether it is running.
 *
 * The URL is relative (`/api/...`), so the request goes to the frontend's own origin and
 * the Vite proxy forwards it to FastAPI.
 *
 * @throws Error if the server answers with a non-2xx status.
 */
export async function fetchHealth(): Promise<HealthResponse> {
  const response = await fetch('/api/health');
  if (!response.ok) {
    throw new Error(`Health check failed with status ${response.status}`);
  }
  return (await response.json()) as HealthResponse;
}
