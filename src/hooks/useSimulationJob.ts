// src/hooks/useSimulationJob.ts
import { useEffect, useRef, useState } from 'react';
import { getSimulationJob } from '../api/bantrel';
import type { JobStatus, SimulationResult } from '../types/simulation';

const POLL_INTERVAL_MS = 1750; // 1.5–2 seconds

interface UseSimulationJobResult {
  status: JobStatus['status'] | null;
  result: SimulationResult | null;
  error: string | null;
  trace: string | undefined;
  isLoading: boolean;
}

export function useSimulationJob(jobId: string | undefined): UseSimulationJobResult {
  const [status, setStatus] = useState<JobStatus['status'] | null>(null);
  const [result, setResult] = useState<SimulationResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [trace, setTrace] = useState<string | undefined>(undefined);
  const [isLoading, setIsLoading] = useState(true);

  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const abortRef = useRef<AbortController | null>(null);

  useEffect(() => {
    if (!jobId) {
      setIsLoading(false);
      return;
    }

    const poll = async () => {
      abortRef.current = new AbortController();
      try {
        const data = await getSimulationJob(jobId, abortRef.current.signal);
        setStatus(data.status);

        if (data.status === 'done') {
          setResult(data.result);
          setIsLoading(false);
          clearInterval(intervalRef.current!);
        } else if (data.status === 'error') {
          setError(data.error);
          setTrace(data.trace);
          setIsLoading(false);
          clearInterval(intervalRef.current!);
        }
        // status 'queued' | 'running' — keep polling
      } catch (err) {
        if ((err as Error).name === 'AbortError') return;
        setError((err as Error).message);
        setIsLoading(false);
        clearInterval(intervalRef.current!);
      }
    };

    // Immediate first poll
    void poll();
    intervalRef.current = setInterval(() => void poll(), POLL_INTERVAL_MS);

    return () => {
      clearInterval(intervalRef.current!);
      abortRef.current?.abort();
    };
  }, [jobId]);

  return { status, result, error, trace, isLoading };
}
