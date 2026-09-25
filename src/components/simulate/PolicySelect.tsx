// src/components/simulate/PolicySelect.tsx
import type { PolicyType } from '../../hooks/useDemandForm';

interface Props {
  value: PolicyType;
  onChange: (policy: PolicyType) => void;
}

const OPTIONS: { value: PolicyType; label: string; sublabel: string; icon: string }[] = [
  { value: 'ppo',         label: 'PPO Agent',           sublabel: 'ppo',         icon: 'smart_toy' },
  { value: 'fixed_cycle', label: 'Fixed-Cycle Baseline', sublabel: 'fixed_cycle', icon: 'timer' },
  { value: 'both',        label: 'Compare Both',        sublabel: 'default',     icon: 'compare' },
];

export function PolicySelect({ value, onChange }: Props) {
  return (
    <div className="space-y-2">
      <label className="block font-mono text-xs text-[#928f9d] tracking-widest uppercase">
        Dispatch Policy
      </label>
      <div className="grid grid-cols-3 gap-2 p-1 bg-[#111125] rounded-xl border border-[#474552]">
        {OPTIONS.map((opt) => {
          const active = value === opt.value;
          return (
            <button
              key={opt.value}
              type="button"
              onClick={() => onChange(opt.value)}
              className={`flex flex-col items-center gap-1 py-3 px-2 rounded-lg text-center transition-all duration-150 ${
                active
                  ? 'bg-[#28283d] shadow-sm border border-[#a29bfe]/40'
                  : 'hover:bg-[#1e1e32] border border-transparent'
              }`}
            >
              <span
                className={`material-symbols-outlined text-xl ${active ? 'text-[#c5c0ff]' : 'text-[#928f9d]'}`}
              >
                {opt.icon}
              </span>
              <span className={`font-['Space_Grotesk'] font-semibold text-xs leading-tight ${active ? 'text-[#e2e0fc]' : 'text-[#c8c4d3]'}`}>
                {opt.label}
              </span>
              <span className={`font-mono text-[0.6rem] ${active ? 'text-[#c5c0ff]' : 'text-[#474552]'}`}>
                {opt.sublabel}
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
