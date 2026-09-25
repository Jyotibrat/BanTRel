// src/components/simulate/CustomDemandForm.tsx
import type { DemandFormState } from '../../hooks/useDemandForm';

interface Props {
  state: Pick<DemandFormState, 'total_vehicles' | 'car_pct' | 'motorcycle_pct' | 'autorickshaw_pct'>;
  setField: <K extends keyof DemandFormState>(key: K, value: DemandFormState[K]) => void;
  pctError?: string;
}

interface SliderRowProps {
  label: string;
  icon: string;
  value: number;
  onChange: (v: number) => void;
  color: string;
}

function SliderRow({ label, icon, value, onChange, color }: SliderRowProps) {
  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="material-symbols-outlined text-base" style={{ color }}>{icon}</span>
          <span className="font-mono text-xs text-[#c8c4d3]">{label}</span>
        </div>
        <span className="font-mono text-sm font-semibold tabular" style={{ color }}>
          {value}%
        </span>
      </div>
      <input
        type="range"
        min={0}
        max={100}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className="w-full"
      />
    </div>
  );
}

export function CustomDemandForm({ state, setField, pctError }: Props) {
  const sum = state.car_pct + state.motorcycle_pct + state.autorickshaw_pct;

  return (
    <div className="space-y-5">
      {/* Total vehicles */}
      <div className="space-y-2">
        <label className="block font-mono text-xs text-[#928f9d] tracking-widest uppercase">
          Total Vehicles
        </label>
        <div className="relative">
          <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-[#928f9d] text-lg pointer-events-none">
            directions_car
          </span>
          <input
            type="number"
            min={100}
            max={100000}
            value={state.total_vehicles}
            onChange={(e) => setField('total_vehicles', Number(e.target.value))}
            className="w-full bg-[#1a1a2e] border border-[#474552] text-[#e2e0fc] rounded-lg pl-10 pr-4 py-2.5 font-mono text-sm focus:outline-none focus:border-[#a29bfe] focus:ring-[3px] focus:ring-[rgba(162,155,254,0.2)] transition-all tabular"
          />
        </div>
      </div>

      {/* Modal split sliders */}
      <div className="space-y-4 p-4 bg-[#111125] rounded-xl border border-[#474552]">
        <div className="flex items-center justify-between mb-1">
          <span className="font-mono text-xs text-[#928f9d] tracking-widest uppercase">Modal Split</span>
          <span
            className={`font-mono text-xs font-bold tabular px-2 py-0.5 rounded ${
              sum === 100
                ? 'bg-[rgba(46,204,113,0.12)] text-[#2ecc71]'
                : 'bg-[rgba(231,76,60,0.12)] text-[#e74c3c]'
            }`}
          >
            {sum}% / 100%
          </span>
        </div>

        <SliderRow
          label="Cars"
          icon="directions_car"
          value={state.car_pct}
          onChange={(v) => setField('car_pct', v)}
          color="#c5c0ff"
        />
        <SliderRow
          label="Motorcycles"
          icon="two_wheeler"
          value={state.motorcycle_pct}
          onChange={(v) => setField('motorcycle_pct', v)}
          color="#4ae183"
        />
        <SliderRow
          label="Auto-Rickshaws"
          icon="local_taxi"
          value={state.autorickshaw_pct}
          onChange={(v) => setField('autorickshaw_pct', v)}
          color="#ffb4a9"
        />

        {pctError && (
          <div className="flex items-center gap-2 p-3 rounded-lg bg-[rgba(231,76,60,0.08)] border border-[rgba(231,76,60,0.3)]">
            <span className="material-symbols-outlined text-[#e74c3c] text-base">error</span>
            <p className="font-mono text-xs text-[#e74c3c]">{pctError}</p>
          </div>
        )}
      </div>
    </div>
  );
}
