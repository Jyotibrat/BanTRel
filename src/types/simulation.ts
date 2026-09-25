// src/types/simulation.ts
// Verbatim from API contract (Step 5 of prompt)

export interface SimulateRequest {
  mode: 'preset' | 'custom';
  policy: 'ppo' | 'fixed_cycle' | 'both';
  period?: 'night' | 'morning_rush' | 'mid_morning' | 'afternoon' | 'evening_rush' | 'evening';
  total_vehicles?: number;
  car_pct?: number;
  motorcycle_pct?: number;
  autorickshaw_pct?: number;
  n_runs?: number;
  deterministic?: boolean;
  seed?: number;
}

export interface MetricSummary {
  label: string;
  unit: string;
  higher_is_better: boolean;
  value: number;
}

export interface PolicyResult {
  summary: Record<string, MetricSummary>;
  timeseries: Record<string, number[]>;
}

export interface ComparisonRow {
  key: string;
  label: string;
  unit: string;
  ppo: number;
  fixed_cycle: number;
  delta: number;
  outcome: 'ppo' | 'fixed_cycle' | 'tie';
}

export interface SimulationResult {
  policy_requested: 'ppo' | 'fixed_cycle' | 'both';
  n_runs: number;
  ppo?: PolicyResult;
  fixed_cycle?: PolicyResult;
  comparison?: {
    rows: ComparisonRow[];
    wins_ppo: number;
    wins_fixed_cycle: number;
    ties: number;
    overall: 'ppo' | 'fixed_cycle' | 'draw';
  };
}

export type JobStatus =
  | { status: 'queued' | 'running' }
  | { status: 'error'; error: string; trace?: string }
  | { status: 'done'; result: SimulationResult };

export const METRIC_KEYS = [
  'system_total_stopped',
  'system_total_waiting_time',
  'system_mean_waiting_time',
  'system_mean_speed',
  'avg_waiting_time',
  'avg_travel_time',
  'queue_length',
  'throughput',
  'delay',
] as const;

export type MetricKey = (typeof METRIC_KEYS)[number];

export const METRIC_LABELS: Record<MetricKey, string> = {
  system_total_stopped: 'Total Stopped',
  system_total_waiting_time: 'Total Wait Time',
  system_mean_waiting_time: 'Mean Wait Time',
  system_mean_speed: 'Mean Speed',
  avg_waiting_time: 'Avg Wait Time',
  avg_travel_time: 'Avg Travel Time',
  queue_length: 'Queue Length',
  throughput: 'Throughput',
  delay: 'Delay',
};
