// src/components/simulate/DemandModeToggle.tsx
import type { DemandMode } from '../../hooks/useDemandForm';

interface Props {
  value: DemandMode;
  onChange: (mode: DemandMode) => void;
}

const OPTIONS: { value: DemandMode; label: string; icon: string; desc: string }[] = [
  { value: 'preset', label: 'Preset Scenario', icon: 'schedule', desc: 'Select from predefined traffic periods' },
  { value: 'custom', label: 'Custom Demand',   icon: 'tune',     desc: 'Configure vehicles and modal split' },
];

export function DemandModeToggle({ value, onChange }: Props) {
  return (
    <div className="grid grid-cols-2 gap-3">
      {OPTIONS.map((opt) => {
        const active = value === opt.value;
        return (
          <button
            key={opt.value}
            type="button"
            onClick={() => onChange(opt.value)}
            className={`flex flex-col gap-1.5 p-4 rounded-xl border text-left transition-all duration-150 ${
              active
                ? 'bg-[rgba(162,155,254,0.12)] border-[#a29bfe] shadow-[0_0_0_1px_rgba(162,155,254,0.3)]'
                : 'bg-[#1e1e32] border-[#474552] hover:border-[#a29bfe] hover:bg-[rgba(162,155,254,0.06)]'
            }`}
          >
            <div className="flex items-center gap-2">
              <span
                className={`material-symbols-outlined text-xl ${active ? 'text-[#c5c0ff]' : 'text-[#928f9d]'}`}
              >
                {opt.icon}
              </span>
              <span
                className={`font-['Space_Grotesk'] font-semibold text-sm ${active ? 'text-[#e2e0fc]' : 'text-[#c8c4d3]'}`}
              >
                {opt.label}
              </span>
              {active && (
                <span className="ml-auto w-2 h-2 rounded-full bg-[#a29bfe] shadow-[0_0_6px_rgba(162,155,254,0.7)]" />
              )}
            </div>
            <p className="font-mono text-[0.7rem] text-[#928f9d] leading-relaxed">{opt.desc}</p>
          </button>
        );
      })}
    </div>
  );
}
