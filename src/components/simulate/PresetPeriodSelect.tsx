// src/components/simulate/PresetPeriodSelect.tsx
import type { PresetPeriod } from '../../hooks/useDemandForm';

interface Props {
  value: PresetPeriod;
  onChange: (period: PresetPeriod) => void;
}

const PERIODS: { value: PresetPeriod; label: string }[] = [
  { value: '',             label: 'Full 24-Hour Day' },
  { value: 'morning_rush', label: 'Morning Rush' },
  { value: 'mid_morning',  label: 'Mid-Morning' },
  { value: 'afternoon',    label: 'Afternoon' },
  { value: 'evening_rush', label: 'Evening Rush' },
  { value: 'evening',      label: 'Evening' },
  { value: 'night',        label: 'Night' },
];

export function PresetPeriodSelect({ value, onChange }: Props) {
  return (
    <div className="space-y-2">
      <label className="block font-mono text-xs text-[#928f9d] tracking-widest uppercase">
        Traffic Period
      </label>
      <div className="relative">
        <select
          value={value}
          onChange={(e) => onChange(e.target.value as PresetPeriod)}
          className="w-full appearance-none bg-[#1a1a2e] border border-[#474552] text-[#e2e0fc] rounded-lg px-4 py-2.5 pr-10 font-mono text-sm focus:outline-none focus:border-[#a29bfe] focus:ring-[3px] focus:ring-[rgba(162,155,254,0.2)] transition-all cursor-pointer"
        >
          {PERIODS.map((p) => (
            <option key={p.value} value={p.value} className="bg-[#1e1e32]">
              {p.label}
            </option>
          ))}
        </select>
        <span className="material-symbols-outlined absolute right-3 top-1/2 -translate-y-1/2 text-[#928f9d] pointer-events-none text-lg">
          expand_more
        </span>
      </div>
      <p className="font-mono text-[0.65rem] text-[#474552]">
        Omitting period runs the full 24-hour simulation cycle
      </p>
    </div>
  );
}
