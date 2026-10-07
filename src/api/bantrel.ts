// src/api/bantrel.ts
// Single module for all API calls — nothing else in the app constructs fetch calls.

import type { JobStatus, SimulateRequest } from '../types/simulation';

const getBaseUrl = (): string => {
  const url = import.meta.env.VITE_API_BASE_URL as string | undefined;
  if (!url) {
    // Fall back to local /api path which will be proxied by Vercel
    return '/api';
  }
  return url.replace(/\/$/, '');
};

/**
 * POST /simulate — Submit a new simulation job.
 * Returns { job_id: string }
 */
export async function postSimulate(
  req: SimulateRequest,
  signal?: AbortSignal,
): Promise<{ job_id: string }> {
  const res = await fetch(`${getBaseUrl()}/simulate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(req),
    signal,
  });

  if (!res.ok) {
    const text = await res.text().catch(() => res.statusText);
    throw new Error(`POST /simulate failed (${res.status}): ${text}`);
  }

  return res.json() as Promise<{ job_id: string }>;
}

/**
 * GET /simulate/{jobId} — Poll for job status.
 */
export async function getSimulationJob(
  jobId: string,
  signal?: AbortSignal,
): Promise<JobStatus> {
  const res = await fetch(`${getBaseUrl()}/simulate/${encodeURIComponent(jobId)}`, {
    signal,
  });

  if (!res.ok) {
    const text = await res.text().catch(() => res.statusText);
    throw new Error(`GET /simulate/${jobId} failed (${res.status}): ${text}`);
  }

  return res.json() as Promise<JobStatus>;
}

/**
 * GET /health — Check if the backend engine is ready.
 * Returns { status: "ok", network_built: boolean, checkpoint_found: boolean }
 */
export async function getHealth(
  signal?: AbortSignal,
): Promise<{ status: string; network_built: boolean; checkpoint_found: boolean }> {
  const res = await fetch(`${getBaseUrl()}/health`, { signal });
  if (!res.ok) throw new Error(`GET /health failed (${res.status})`);
  return res.json() as Promise<{ status: string; network_built: boolean; checkpoint_found: boolean }>;
}
