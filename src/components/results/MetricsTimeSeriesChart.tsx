// src/components/results/MetricsTimeSeriesChart.tsx
import { useState } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import type { SimulationResult } from '../../types/simulation';
import { METRIC_KEYS, METRIC_LABELS } from '../../types/simulation';
import type { MetricKey } from '../../types/simulation';

interface Props {
  result: SimulationResult;
}

function buildChartData(
  result: SimulationResult,
  metricKey: MetricKey,
): Array<{ step: number; ppo?: number; fixed_cycle?: number }> {
  const ppoSeries = result.ppo?.timeseries[metricKey];
  const fcSeries = result.fixed_cycle?.timeseries[metricKey];

  const len = Math.max(ppoSeries?.length ?? 0, fcSeries?.length ?? 0);
  if (len === 0) return [];

  return Array.from({ length: len }, (_, i) => ({
    step: i + 1,
    ...(ppoSeries ? { ppo: ppoSeries[i] } : {}),
    ...(fcSeries ? { fixed_cycle: fcSeries[i] } : {}),
  }));
}

const CUSTOM_TOOLTIP_STYLE = {
  backgroundColor: '#2b2b48',
  border: '1px solid rgba(162, 155, 254, 0.3)',
  borderRadius: '0.5rem',
  boxShadow: '0 16px 36px -6px rgba(0, 0, 0, 0.75)',
  color: '#e2e0fc',
  fontFamily: 'JetBrains Mono, monospace',
  fontSize: '0.75rem',
};

export function MetricsTimeSeriesChart({ result }: Props) {
  // Only show metric keys that have data
  const availableKeys = METRIC_KEYS.filter(
    (k) =>
      (result.ppo?.timeseries[k]?.length ?? 0) > 0 ||
      (result.fixed_cycle?.timeseries[k]?.length ?? 0) > 0,
  );

  const [activeKey, setActiveKey] = useState<MetricKey>(availableKeys[0] ?? 'throughput');

  if (availableKeys.length === 0) return null;

  const data = buildChartData(result, activeKey);
  const hasPpo = !!result.ppo?.timeseries[activeKey];
  const hasFc = !!result.fixed_cycle?.timeseries[activeKey];

  return (
    <div className="rounded-xl border border-[#474552] overflow-hidden">
      <div className="px-4 py-3 bg-[#1e1e32] border-b border-[#474552] flex items-center justify-between gap-3 flex-wrap">
        <h3 className="font-['Space_Grotesk'] font-semibold text-sm text-[#e2e0fc]">
          Time-Series Telemetry
        </h3>
        <div className="flex items-center gap-4 font-mono text-xs text-[#928f9d]">
          {hasPpo && (
            <span className="flex items-center gap-1.5">
              <span className="w-6 h-0.5 rounded bg-[#a29bfe] inline-block" />
              PPO Agent
            </span>
          )}
          {hasFc && (
            <span className="flex items-center gap-1.5">
              <span className="w-6 h-0.5 rounded bg-[#928f9d] inline-block" />
              Fixed-Cycle
            </span>
          )}
        </div>
      </div>

      {/* Metric selector tabs */}
      <div className="flex gap-1 p-2 bg-[#111125] border-b border-[#474552] overflow-x-auto">
        {availableKeys.map((key) => (
          <button
            key={key}
            onClick={() => setActiveKey(key)}
            className={`flex-shrink-0 px-3 py-1.5 rounded-lg font-mono text-[0.65rem] tracking-wider uppercase transition-all duration-150 ${
              activeKey === key
                ? 'bg-[rgba(162,155,254,0.15)] text-[#c5c0ff] border border-[rgba(162,155,254,0.3)]'
                : 'text-[#928f9d] hover:text-[#c8c4d3] hover:bg-[#1e1e32] border border-transparent'
            }`}
          >
            {METRIC_LABELS[key]}
          </button>
        ))}
      </div>

      {/* Chart */}
      <div className="p-4 bg-[#0c0c1f]">
        <ResponsiveContainer width="100%" height={280}>
          <LineChart data={data} margin={{ top: 8, right: 16, left: 0, bottom: 8 }}>
            <CartesianGrid
              strokeDasharray="4 4"
              stroke="#2e2e4f"
              vertical={false}
            />
            <XAxis
              dataKey="step"
              tick={{ fill: '#928f9d', fontFamily: 'JetBrains Mono', fontSize: 10 }}
              axisLine={{ stroke: '#474552' }}
              tickLine={false}
              label={{ value: 'Simulation Step', fill: '#474552', fontSize: 10, fontFamily: 'JetBrains Mono', position: 'insideBottom', offset: -2 }}
            />
            <YAxis
              tick={{ fill: '#928f9d', fontFamily: 'JetBrains Mono', fontSize: 10 }}
              axisLine={false}
              tickLine={false}
              width={48}
            />
            <RechartsTooltip
              contentStyle={CUSTOM_TOOLTIP_STYLE}
              labelStyle={{ color: '#c5c0ff', marginBottom: 4 }}
              formatter={(value) => [
                typeof value === 'number' ? value.toFixed(3) : value,
                undefined,
              ]}
            />
            <Legend wrapperStyle={{ display: 'none' }} />
            {hasPpo && (
              <Line
                type="monotone"
                dataKey="ppo"
                name="PPO Agent"
                stroke="#a29bfe"
                strokeWidth={2}
                dot={false}
                activeDot={{ r: 4, fill: '#a29bfe', strokeWidth: 0 }}
              />
            )}
            {hasFc && (
              <Line
                type="monotone"
                dataKey="fixed_cycle"
                name="Fixed-Cycle"
                stroke="#928f9d"
                strokeWidth={2}
                dot={false}
                strokeDasharray="5 3"
                activeDot={{ r: 4, fill: '#928f9d', strokeWidth: 0 }}
              />
            )}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
