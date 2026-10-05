// src/components/results/LoadingState.tsx
export function LoadingState() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] gap-8">
      {/* Animated intersection schematic */}
      <div className="relative w-32 h-32">
        <div className="absolute inset-0 rounded-full border-2 border-[#474552] animate-ping opacity-20" />
        <div className="absolute inset-4 rounded-full border-2 border-[#a29bfe]/40 animate-ping opacity-40" style={{ animationDelay: '0.3s' }} />
        <div className="w-full h-full rounded-full border-2 border-[#474552] flex items-center justify-center bg-[#1e1e32] shadow-[0_0_40px_rgba(162,155,254,0.15)]">
          <span
            className="material-symbols-outlined text-[#a29bfe] text-5xl animate-spin"
            style={{ animationDuration: '3s', fontVariationSettings: "'FILL' 1" }}
          >
            traffic
          </span>
        </div>
      </div>

      {/* Status text */}
      <div className="text-center space-y-2 w-full max-w-[450px] mx-auto px-4">
        <div className="flex items-center justify-center gap-2 font-mono text-xs text-[#a29bfe] tracking-widest uppercase">
          <span className="w-1.5 h-1.5 rounded-full bg-[#a29bfe] animate-pulse" />
          <span>Simulation Running</span>
          <span className="w-1.5 h-1.5 rounded-full bg-[#a29bfe] animate-pulse" />
        </div>
        <h2 className="font-['Space_Grotesk'] font-semibold text-2xl text-[#e2e0fc]">
          SUMO Engine Processing…
        </h2>
        <p className="font-['Inter'] text-[#c8c4d3] text-sm w-full mx-auto">
          The PPO agent and fixed-cycle baseline are running their simulation passes. This typically takes 1–5 minutes.
        </p>
      </div>

      {/* Skeleton metric cards */}
      <div className="grid grid-cols-3 gap-3 w-full max-w-2xl">
        {[...Array(9)].map((_, i) => (
          <div key={i} className="skeleton h-16 rounded-xl" style={{ animationDelay: `${i * 0.1}s` }} />
        ))}
      </div>

      <p className="font-mono text-[0.65rem] text-[#474552]">
        Polling every 1.75s · Do not close this tab
      </p>
    </div>
  );
}
