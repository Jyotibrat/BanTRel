// src/components/results/MetricsSummaryTable.tsx
import type { ComparisonRow } from '../../types/simulation';
import { Badge } from '../ui/Badge';

interface Props {
  rows: ComparisonRow[];
}

function DeltaCell({ row }: { row: ComparisonRow }) {
  const sign = row.delta > 0 ? '+' : '';
  const variant = row.outcome === 'ppo' ? 'ppo' : row.outcome === 'fixed_cycle' ? 'fixed_cycle' : 'tie';

  return (
    <Badge variant={variant} pill={false}>
      {sign}{row.delta.toFixed(2)} {row.unit}
    </Badge>
  );
}

function OutcomeCell({ outcome }: { outcome: ComparisonRow['outcome'] }) {
  if (outcome === 'ppo') {
    return (
      <span className="flex items-center gap-1 text-[#2ecc71] font-mono text-xs">
        <span className="material-symbols-outlined text-sm" style={{ fontVariationSettings: "'FILL' 1" }}>smart_toy</span>
        PPO
      </span>
    );
  }
  if (outcome === 'fixed_cycle') {
    return (
      <span className="flex items-center gap-1 text-[#e74c3c] font-mono text-xs">
        <span className="material-symbols-outlined text-sm" style={{ fontVariationSettings: "'FILL' 1" }}>timer</span>
        Fixed
      </span>
    );
  }
  return (
    <span className="flex items-center gap-1 text-[#f39c12] font-mono text-xs">
      <span className="material-symbols-outlined text-sm">balance</span>
      Tie
    </span>
  );
}

export function MetricsSummaryTable({ rows }: Props) {
  return (
    <div className="rounded-xl border border-[#474552] overflow-hidden">
      <div className="px-4 py-3 bg-[#1e1e32] border-b border-[#474552]">
        <h3 className="font-['Space_Grotesk'] font-semibold text-sm text-[#e2e0fc]">
          Metrics Comparison Table
        </h3>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-[#111125] border-b border-[#474552]">
              {['Metric', 'PPO Agent', 'Fixed-Cycle', 'Δ Delta', 'Winner'].map((h) => (
                <th
                  key={h}
                  className="px-4 py-3 text-left font-mono text-[0.65rem] tracking-widest uppercase text-[#928f9d]"
                >
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, i) => (
              <tr
                key={row.key}
                className={`border-b border-[#474552]/50 transition-colors hover:bg-[#1e1e32] ${
                  i % 2 === 0 ? 'bg-[#111125]' : 'bg-[#0c0c1f]'
                }`}
              >
                <td className="px-4 py-3">
                  <span className="font-['Inter'] text-[#c8c4d3] text-sm">{row.label}</span>
                  <br />
                  <span className="font-mono text-[0.6rem] text-[#474552]">{row.key}</span>
                </td>
                <td className="px-4 py-3 font-mono font-semibold text-[#e2e0fc] tabular">
                  {row.ppo.toFixed(2)}
                  <span className="text-[#474552] text-xs ml-1">{row.unit}</span>
                </td>
                <td className="px-4 py-3 font-mono font-semibold text-[#e2e0fc] tabular">
                  {row.fixed_cycle.toFixed(2)}
                  <span className="text-[#474552] text-xs ml-1">{row.unit}</span>
                </td>
                <td className="px-4 py-3">
                  <DeltaCell row={row} />
                </td>
                <td className="px-4 py-3">
                  <OutcomeCell outcome={row.outcome} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
