// src/components/results/ErrorState.tsx
import { Link } from 'react-router-dom';
import { Button } from '../ui/Button';

interface Props {
  error: string | null;
  trace?: string;
}

export function ErrorState({ error, trace }: Props) {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] gap-8 max-w-2xl mx-auto text-center">
      {/* Error icon */}
      <div className="w-24 h-24 rounded-full bg-[rgba(231,76,60,0.08)] border border-[rgba(231,76,60,0.3)] flex items-center justify-center shadow-[0_0_40px_rgba(231,76,60,0.12)]">
        <span className="material-symbols-outlined text-[#e74c3c] text-5xl" style={{ fontVariationSettings: "'FILL' 1" }}>
          error
        </span>
      </div>

      <div className="space-y-3">
        <div className="font-mono text-xs text-[#e74c3c] tracking-widest uppercase">
          Simulation Failed
        </div>
        <h2 className="font-['Space_Grotesk'] font-semibold text-2xl text-[#e2e0fc]">
          The Engine Returned an Error
        </h2>
        <p className="text-[#c8c4d3] text-sm leading-relaxed">
          {error || 'An unknown error occurred during simulation.'}
        </p>
      </div>

      {trace && (
        <div className="w-full text-left">
          <details className="group">
            <summary className="font-mono text-xs text-[#928f9d] cursor-pointer hover:text-[#c8c4d3] transition-colors flex items-center gap-1.5">
              <span className="material-symbols-outlined text-sm">bug_report</span>
              View stack trace
            </summary>
            <pre className="mt-3 p-4 bg-[#0c0c1f] border border-[#474552] rounded-xl text-[0.65rem] text-[#c8c4d3] font-mono overflow-auto max-h-48 leading-relaxed whitespace-pre-wrap">
              {trace}
            </pre>
          </details>
        </div>
      )}

      <div className="flex items-center gap-3">
        <Link to="/simulate">
          <Button variant="primary">
            <span className="material-symbols-outlined text-base">arrow_back</span>
            Back to Configure
          </Button>
        </Link>
        <Button variant="ghost" onClick={() => window.location.reload()}>
          <span className="material-symbols-outlined text-base">refresh</span>
          Retry
        </Button>
      </div>
    </div>
  );
}
