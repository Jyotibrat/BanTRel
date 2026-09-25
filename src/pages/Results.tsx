// src/pages/Results.tsx
import { useParams, Link } from 'react-router-dom';
import { useSimulationJob } from '../hooks/useSimulationJob';
import { LoadingState } from '../components/results/LoadingState';
import { ErrorState } from '../components/results/ErrorState';
import { VerdictBanner } from '../components/results/VerdictBanner';
import { MetricsSummaryTable } from '../components/results/MetricsSummaryTable';
import { MetricsTimeSeriesChart } from '../components/results/MetricsTimeSeriesChart';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';

function SinglePolicyMetrics({ result }: { result: import('../types/simulation').SimulationResult }) {
  const policyData = result.ppo ?? result.fixed_cycle;
  const policyLabel = result.ppo ? 'PPO Agent' : 'Fixed-Cycle Baseline';
  if (!policyData) return null;

  return (
    <div className="space-y-4">
      <h3 className="font-['Space_Grotesk'] font-semibold text-[#e2e0fc]">
        {policyLabel} — Summary Metrics
      </h3>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
        {Object.entries(policyData.summary).map(([key, metric]) => (
          <div
            key={key}
            className="p-4 rounded-xl bg-[#1e1e32] border border-[#474552] space-y-1"
          >
            <p className="font-mono text-[0.6rem] text-[#928f9d] uppercase tracking-wider">
              {metric.label}
            </p>
            <p className="font-mono font-bold text-xl text-[#e2e0fc] tabular">
              {metric.value.toFixed(2)}
              <span className="text-xs text-[#474552] ml-1">{metric.unit}</span>
            </p>
            <Badge variant={metric.higher_is_better ? 'success' : 'default'} pill={false}>
              {metric.higher_is_better ? '↑ Higher = Better' : '↓ Lower = Better'}
            </Badge>
          </div>
        ))}
      </div>
    </div>
  );
}

export function Results() {
  const { jobId } = useParams<{ jobId: string }>();
  const { status, result, error, trace, isLoading } = useSimulationJob(jobId);

  // Loading / initial state — show loader while jobId exists and status hasn't settled
  if (jobId && (isLoading || status === null || status === 'queued' || status === 'running')) {
    return (
      <main className="max-w-5xl mx-auto px-4 sm:px-6 py-10">
        <LoadingState />
      </main>
    );
  }

  // Error state
  if (status === 'error') {
    return (
      <main className="max-w-5xl mx-auto px-4 sm:px-6 py-10">
        <ErrorState error={error} trace={trace} />
      </main>
    );
  }

  // Done state
  if (status === 'done' && result) {
    const hasBoth = !!result.comparison;

    return (
      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-8 space-y-6">

        {/* Header */}
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-4 border-b border-[#474552]/40">
          <div className="space-y-1.5">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="inline-flex items-center gap-1.5 font-mono text-[0.65rem] px-2.5 py-1 rounded-full bg-[#28283d] border border-[#474552] text-[#e2e0fc]">
                <span className="w-2 h-2 rounded-full bg-[#4ae183]" />
                JOB #{jobId?.substring(0, 8).toUpperCase()} · COMPLETED
              </span>
            </div>
            <h1 className="font-['Space_Grotesk'] font-bold text-2xl md:text-3xl text-[#e2e0fc] tracking-tight">
              Simulation Results
            </h1>
            <p className="font-['Inter'] text-[#c8c4d3] text-sm">
              {result.policy_requested === 'both'
                ? `Comparative run — PPO Agent vs Fixed-Cycle Baseline · ${result.n_runs} run${result.n_runs > 1 ? 's' : ''}`
                : `Single policy run — ${result.policy_requested === 'ppo' ? 'PPO Agent' : 'Fixed-Cycle Baseline'} · ${result.n_runs} run${result.n_runs > 1 ? 's' : ''}`}
            </p>
          </div>

          <div className="flex items-center gap-2 self-start lg:self-center">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => navigator.clipboard.writeText(window.location.href)}
            >
              <span className="material-symbols-outlined text-base text-[#c5c0ff]">link</span>
              Share Results
            </Button>
            <Link to="/simulate">
              <Button variant="secondary" size="sm">
                <span className="material-symbols-outlined text-base">add</span>
                New Simulation
              </Button>
            </Link>
          </div>
        </div>

        {/* Verdict banner (only for "both" policy) */}
        {hasBoth && <VerdictBanner result={result} />}

        {/* Comparison table (only for "both") */}
        {hasBoth && result.comparison && (
          <MetricsSummaryTable rows={result.comparison.rows} />
        )}

        {/* Single policy metrics (if not comparison) */}
        {!hasBoth && <SinglePolicyMetrics result={result} />}

        {/* Time series chart */}
        <MetricsTimeSeriesChart result={result} />

        {/* Back CTA */}
        <div className="pt-4 border-t border-[#474552]/40 flex justify-center">
          <Link to="/simulate">
            <Button variant="primary">
              <span className="material-symbols-outlined text-base">add</span>
              Run Another Simulation
            </Button>
          </Link>
        </div>
      </main>
    );
  }

  // Fallback (no jobId, etc.)
  return (
    <main className="max-w-5xl mx-auto px-4 sm:px-6 py-20 text-center">
      <p className="text-[#928f9d] font-mono text-sm">No job ID provided.</p>
      <Link to="/simulate" className="mt-4 inline-block">
        <Button variant="primary">Configure a Simulation</Button>
      </Link>
    </main>
  );
}
