// src/components/ui/Slider.tsx
// Reusable slider with label and value display.
// Uses the custom range thumb defined in index.css (Stitch spec).

interface SliderProps {
  label: string;
  value: number;
  min?: number;
  max?: number;
  step?: number;
  onChange: (value: number) => void;
  unit?: string;
  accentColor?: string;
  className?: string;
  id?: string;
}

export function Slider({
  label,
  value,
  min = 0,
  max = 100,
  step = 1,
  onChange,
  unit = '',
  accentColor = '#c5c0ff',
  className = '',
  id,
}: SliderProps) {
  const pct = ((value - min) / (max - min)) * 100;

  return (
    <div className={`space-y-2 ${className}`}>
      {/* Label row */}
      <div className="flex items-center justify-between">
        <label
          htmlFor={id}
          className="font-mono text-xs text-[#c8c4d3]"
        >
          {label}
        </label>
        <span
          className="font-mono font-semibold text-sm tabular"
          style={{ color: accentColor }}
        >
          {value}{unit}
        </span>
      </div>

      {/* Track wrapper — shows filled portion via background gradient */}
      <div className="relative">
        <input
          id={id}
          type="range"
          min={min}
          max={max}
          step={step}
          value={value}
          onChange={(e) => onChange(Number(e.target.value))}
          className="w-full"
          style={{
            // Progressive fill behind the thumb using a CSS gradient
            background: `linear-gradient(to right, ${accentColor} 0%, ${accentColor} ${pct}%, #1a1a2e ${pct}%, #1a1a2e 100%)`,
          }}
        />
      </div>

      {/* Min / max labels */}
      <div className="flex justify-between font-mono text-[0.6rem] text-[#474552]">
        <span>{min}{unit}</span>
        <span>{max}{unit}</span>
      </div>
    </div>
  );
}
