// src/pages/NotFound.tsx
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/Button';

export function NotFound() {
  return (
    <main className="min-h-[80vh] flex flex-col items-center justify-center px-6 text-center relative">
      {/* Background glow */}
      <div className="absolute inset-0 grid-lines pointer-events-none opacity-20" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-[rgba(231,76,60,0.05)] blur-[80px] rounded-full pointer-events-none" />

      <div className="relative z-10 space-y-6 max-w-md">
        {/* 404 number */}
        <div className="font-['Space_Grotesk'] font-bold text-[8rem] leading-none text-transparent bg-clip-text bg-gradient-to-b from-[#474552] to-[#1e1e32] select-none">
          404
        </div>

        {/* Signal icon */}
        <div className="flex justify-center">
          <div className="w-20 h-20 rounded-2xl bg-[rgba(231,76,60,0.08)] border border-[rgba(231,76,60,0.25)] flex items-center justify-center">
            <span
              className="material-symbols-outlined text-[#e74c3c] text-5xl"
              style={{ fontVariationSettings: "'FILL' 1" }}
            >
              traffic
            </span>
          </div>
        </div>

        <div className="space-y-2">
          <h1 className="font-['Space_Grotesk'] font-bold text-2xl text-[#e2e0fc]">
            Signal Not Found
          </h1>
          <p className="text-[#928f9d] text-sm leading-relaxed">
            This intersection doesn't exist in the BanTRel network. The route you're looking for may have been removed or the URL is incorrect.
          </p>
        </div>

        <div className="flex items-center justify-center gap-3 flex-wrap">
          <Link to="/">
            <Button variant="primary">
              <span className="material-symbols-outlined text-base">home</span>
              Back to Home
            </Button>
          </Link>
          <Link to="/simulate">
            <Button variant="secondary">
              <span className="material-symbols-outlined text-base">smart_toy</span>
              Run a Simulation
            </Button>
          </Link>
        </div>

        <p className="font-mono text-[0.6rem] text-[#474552]">
          Error 404 · Route not found in BanTRel navigation graph
        </p>
      </div>
    </main>
  );
}
