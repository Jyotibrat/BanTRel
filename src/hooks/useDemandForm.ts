// src/hooks/useDemandForm.ts
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { postSimulate } from '../api/bantrel';
import type { SimulateRequest } from '../types/simulation';

export type DemandMode = 'preset' | 'custom';
export type PolicyType = 'ppo' | 'fixed_cycle' | 'both';
export type PresetPeriod =
  | ''
  | 'night'
  | 'morning_rush'
  | 'mid_morning'
  | 'afternoon'
  | 'evening_rush'
  | 'evening';

export interface DemandFormState {
  mode: DemandMode;
  period: PresetPeriod;
  total_vehicles: number;
  car_pct: number;
  motorcycle_pct: number;
  autorickshaw_pct: number;
  policy: PolicyType;
  n_runs: number;
  deterministic: boolean;
  seed: string;
}

export interface DemandFormErrors {
  pct_sum?: string;
  n_runs?: string;
}

const DEFAULT_STATE: DemandFormState = {
  mode: 'preset',
  period: 'morning_rush',
  total_vehicles: 16400,
  car_pct: 50,
  motorcycle_pct: 35,
  autorickshaw_pct: 15,
  policy: 'both',
  n_runs: 1,
  deterministic: false,
  seed: '',
};

export function useDemandForm() {
  const navigate = useNavigate();
  const [formState, setFormState] = useState<DemandFormState>(DEFAULT_STATE);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  const setField = <K extends keyof DemandFormState>(
    key: K,
    value: DemandFormState[K],
  ) => {
    setFormState((prev) => ({ ...prev, [key]: value }));
  };

  // Validation
  const errors: DemandFormErrors = {};

  if (formState.mode === 'custom') {
    const sum = formState.car_pct + formState.motorcycle_pct + formState.autorickshaw_pct;
    if (sum !== 100) {
      errors.pct_sum = `Percentages must sum to 100 (currently ${sum})`;
    }
  }

  if (formState.n_runs < 1 || formState.n_runs > 3) {
    errors.n_runs = 'Number of runs must be between 1 and 3';
  }

  const isValid = Object.keys(errors).length === 0;

  const submit = async () => {
    if (!isValid || isSubmitting) return;

    setIsSubmitting(true);
    setSubmitError(null);

    const req: SimulateRequest = {
      mode: formState.mode,
      policy: formState.policy,
      n_runs: formState.n_runs,
      deterministic: formState.deterministic,
    };

    if (formState.mode === 'preset') {
      if (formState.period) {
        req.period = formState.period as Exclude<PresetPeriod, ''>;
      }
      // period omitted for full 24-hour day (empty string)
    } else {
      req.total_vehicles = formState.total_vehicles;
      req.car_pct = formState.car_pct;
      req.motorcycle_pct = formState.motorcycle_pct;
      req.autorickshaw_pct = formState.autorickshaw_pct;
    }

    if (formState.seed.trim() !== '') {
      const seedNum = parseInt(formState.seed, 10);
      if (!isNaN(seedNum)) req.seed = seedNum;
    }

    try {
      const { job_id } = await postSimulate(req);
      navigate(`/simulate/${job_id}`);
    } catch (err) {
      setSubmitError((err as Error).message);
      setIsSubmitting(false);
    }
  };

  return {
    formState,
    setField,
    isValid,
    errors,
    submit,
    isSubmitting,
    submitError,
  };
}
