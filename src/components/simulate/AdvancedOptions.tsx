// src/components/simulate/AdvancedOptions.tsx
import { useState } from 'react';
import { Tooltip } from '../ui/Tooltip';
import type { DemandFormState } from '../../hooks/useDemandForm';

interface Props {
  state: Pick<DemandFormState, 'n_runs' | 'deterministic' | 'seed'>;
  setField: <K extends keyof DemandFormState>(key: K, value: DemandFormState[K]) => void;
  nRunsError?: string;
}

export function AdvancedOptions({ state, setField, nRunsError }: Props) {
  const [open, setOpen] = useState(false);

  return (
    <div className="border border-[#474552] rounded-xl overflow-hidden">
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        className="w-full flex items-center justify-between px-4 py-3 bg-[#1e1e32] hover:bg-[#28283d] transition-colors"
      >
        <div className="flex items-center gap-2">
          <span className="material-symbols-outlined text-[#928f9d] text-base">settings_suggest</span>
          <span className="font-mono text-xs text-[#c8c4d3] tracking-wider uppercase">Advanced Options</span>
        </div>
        <span
          className={`material-symbols-outlined text-[#928f9d] transition-transform duration-200 ${open ? 'rotate-180' : ''}`}
        >
          expand_more
        </span>
      </button>

      {open && (
        <div className="px-4 py-4 bg-[#111125] space-y-5 border-t border-[#474552]">

          {/* n_runs */}
          <div className="space-y-2">
            <label className="block font-mono text-xs text-[#928f9d] tracking-widest uppercase">
              Number of Runs
            </label>
            <div className="flex items-center gap-3">
              {[1, 2, 3].map((n) => (
                <button
                  key={n}
                  type="button"
                  onClick={() => setField('n_runs', n)}
                  className={`w-10 h-10 rounded-lg font-mono font-semibold text-sm transition-all duration-150 ${
                    state.n_runs === n
                      ? 'bg-[#a29bfe] text-[#2a1f7e] shadow-[0_0_10px_rgba(162,155,254,0.4)]'
                      : 'bg-[#1e1e32] border border-[#474552] text-[#c8c4d3] hover:border-[#a29bfe]'
                  }`}
                >
                  {n}
                </button>
              ))}
              <p className="font-mono text-[0.65rem] text-[#474552] ml-1">
                Averaged across runs for statistical robustness
              </p>
            </div>
            {nRunsError && (
              <p className="font-mono text-xs text-[#e74c3c]">{nRunsError}</p>
            )}
          </div>

          {/* deterministic toggle */}
          <div className="flex items-center justify-between gap-4">
            <div className="flex items-center gap-2">
              <span className="font-mono text-xs text-[#c8c4d3]">Deterministic Mode</span>
              <Tooltip content="When ON, the PPO agent uses greedy action selection — fully reproducible. When OFF (default), actions are sampled stochastically, matching the paper's evaluation protocol but producing different results each run.">
                <span className="material-symbols-outlined text-[#928f9d] text-base cursor-help">
                  help_outline
                </span>
              </Tooltip>
            </div>
            <button
              type="button"
              role="switch"
              aria-checked={state.deterministic}
              onClick={() => setField('deterministic', !state.deterministic)}
              className={`relative w-11 h-6 rounded-full border transition-all duration-200 ${
                state.deterministic
                  ? 'bg-[#a29bfe] border-[#a29bfe]'
                  : 'bg-[#1e1e32] border-[#474552]'
              }`}
            >
              <span
                className={`absolute top-0.5 left-0.5 w-5 h-5 rounded-full bg-white shadow transition-transform duration-200 ${
                  state.deterministic ? 'translate-x-5' : 'translate-x-0'
                }`}
              />
            </button>
          </div>

          {/* seed */}
          <div className="space-y-2">
            <label className="block font-mono text-xs text-[#928f9d] tracking-widest uppercase">
              Random Seed <span className="text-[#474552]">(optional)</span>
            </label>
            <input
              type="number"
              placeholder="e.g. 42"
              value={state.seed}
              onChange={(e) => setField('seed', e.target.value)}
              className="w-full bg-[#1a1a2e] border border-[#474552] text-[#e2e0fc] rounded-lg px-4 py-2.5 font-mono text-sm placeholder:text-[#474552] focus:outline-none focus:border-[#a29bfe] focus:ring-[3px] focus:ring-[rgba(162,155,254,0.2)] transition-all tabular"
            />
          </div>
        </div>
      )}
    </div>
  );
}
