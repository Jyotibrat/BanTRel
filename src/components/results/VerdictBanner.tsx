// src/components/results/VerdictBanner.tsx
import type { SimulationResult } from '../../types/simulation';

interface Props {
  result: SimulationResult;
}

const VERDICT_CONFIG = {
  ppo: {
    label: 'PPO Agent Wins',
    sublabel: 'Reinforcement learning outperforms the fixed-cycle baseline',
    icon: 'smart_toy',
    bg: 'bg-[rgba(46,204,113,0.08)] border-[rgba(46,204,113,0.3)]',
    iconColor: 'text-[#2ecc71]',
    textColor: 'text-[#2ecc71]',
    glow: 'shadow-[0_0_40px_rgba(46,204,113,0.12)]',
  },
  fixed_cycle: {
    label: 'Fixed-Cycle Baseline Wins',
    sublabel: 'Traditional signal timing outperforms the RL agent this run',
    icon: 'timer',
    bg: 'bg-[rgba(231,76,60,0.08)] border-[rgba(231,76,60,0.3)]',
    iconColor: 'text-[#e74c3c]',
    textColor: 'text-[#e74c3c]',
    glow: 'shadow-[0_0_40px_rgba(231,76,60,0.12)]',
  },
  draw: {
    label: 'Statistical Draw',
    sublabel: 'Both policies performed comparably across all metrics',
    icon: 'balance',
    bg: 'bg-[rgba(243,156,18,0.08)] border-[rgba(243,156,18,0.3)]',
    iconColor: 'text-[#f39c12]',
    textColor: 'text-[#f39c12]',
    glow: 'shadow-[0_0_40px_rgba(243,156,18,0.12)]',
  },
};

export function VerdictBanner({ result }: Props) {
  if (!result.comparison) return null;

  const { overall, wins_ppo, wins_fixed_cycle, ties } = result.comparison;
  const cfg = VERDICT_CONFIG[overall];

  return (
    <div className={`rounded-2xl border p-6 ${cfg.bg} ${cfg.glow}`}>
      <div className="flex flex-col sm:flex-row items-center gap-6">
        {/* Icon */}
        <div className={`w-16 h-16 rounded-2xl border flex items-center justify-center flex-shrink-0 ${cfg.bg}`}>
          <span
            className={`material-symbols-outlined text-4xl ${cfg.iconColor}`}
            style={{ fontVariationSettings: "'FILL' 1" }}
          >
            {cfg.icon}
          </span>
        </div>

        {/* Text */}
        <div className="flex-1 text-center sm:text-left">
          <p className={`font-mono text-xs tracking-widest uppercase mb-1 ${cfg.textColor}`}>
            Overall Verdict
          </p>
          <h2 className={`font-['Space_Grotesk'] font-bold text-2xl ${cfg.textColor}`}>
            {cfg.label}
          </h2>
          <p className="text-[#c8c4d3] text-sm mt-1">{cfg.sublabel}</p>
        </div>

        {/* Win counter chips */}
        <div className="flex items-center gap-3 flex-shrink-0">
          <div className="text-center">
            <div className="font-mono font-bold text-2xl text-[#2ecc71] tabular">{wins_ppo}</div>
            <div className="font-mono text-[0.6rem] text-[#928f9d] tracking-wider">PPO Wins</div>
          </div>
          <div className="w-px h-8 bg-[#474552]" />
          <div className="text-center">
            <div className="font-mono font-bold text-2xl text-[#e74c3c] tabular">{wins_fixed_cycle}</div>
            <div className="font-mono text-[0.6rem] text-[#928f9d] tracking-wider">FC Wins</div>
          </div>
          <div className="w-px h-8 bg-[#474552]" />
          <div className="text-center">
            <div className="font-mono font-bold text-2xl text-[#f39c12] tabular">{ties}</div>
            <div className="font-mono text-[0.6rem] text-[#928f9d] tracking-wider">Ties</div>
          </div>
        </div>
      </div>
    </div>
  );
}
