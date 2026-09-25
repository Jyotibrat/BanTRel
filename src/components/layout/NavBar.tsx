// src/components/layout/NavBar.tsx
import { useEffect, useRef, useState } from 'react';
import { Link, NavLink } from 'react-router-dom';
import { getHealth } from '../../api/bantrel';

type EngineStatus = 'checking' | 'ready' | 'degraded' | 'offline';

function useEngineStatus(): EngineStatus {
  const [status, setStatus] = useState<EngineStatus>('checking');
  const abortRef = useRef<AbortController | null>(null);

  useEffect(() => {
    let cancelled = false;

    const check = async () => {
      abortRef.current = new AbortController();
      try {
        const health = await getHealth(abortRef.current.signal);
        if (cancelled) return;
        if (health.status === 'ok' && health.network_built && health.checkpoint_found) {
          setStatus('ready');
        } else {
          // Backend is up but SUMO network or checkpoint is missing
          setStatus('degraded');
        }
      } catch (err) {
        if ((err as Error).name === 'AbortError' || cancelled) return;
        setStatus('offline');
      }
    };

    void check();
    return () => {
      cancelled = true;
      abortRef.current?.abort();
    };
  }, []);

  return status;
}

const ENGINE_LABEL: Record<EngineStatus, string> = {
  checking: 'Engine: Checking…',
  ready: 'Engine: Ready',
  degraded: 'Engine: Degraded',
  offline: 'Engine: Offline',
};

const ENGINE_DOT: Record<EngineStatus, string> = {
  checking: 'bg-[#f39c12] animate-pulse',
  ready: 'bg-[#4ae183] animate-pulse',
  degraded: 'bg-[#f39c12]',
  offline: 'bg-[#e74c3c]',
};

export function NavBar() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const engineStatus = useEngineStatus();

  const linkClass = ({ isActive }: { isActive: boolean }) =>
    isActive
      ? 'text-[#c5c0ff] border-b-2 border-[#c5c0ff] font-medium font-mono text-xs h-full flex items-center px-1 tracking-wider'
      : 'text-[#c8c4d3] border-b-2 border-transparent font-mono text-xs hover:text-[#e2e0fc] transition-colors duration-150 h-full flex items-center px-1 tracking-wider';

  return (
    <header className="sticky top-0 z-50 h-16 bg-[rgba(26,26,46,0.85)] backdrop-blur-[12px] border-b border-[#474552] shadow-sm">
      <div className="flex items-center justify-between w-full h-full px-6 max-w-7xl mx-auto">

        {/* Brand */}
        <Link to="/" className="flex items-center gap-2.5 group">
          <div className="w-8 h-8 rounded-lg bg-[#28283d] border border-[#474552] flex items-center justify-center relative overflow-hidden group-hover:border-[#a29bfe] transition-colors duration-150">
            <span
              className="material-symbols-outlined text-[#a29bfe] text-xl"
              style={{ fontVariationSettings: "'FILL' 1" }}
            >
              traffic
            </span>
            <span className="absolute top-1 right-1 w-1.5 h-1.5 rounded-full bg-[#4ae183]" />
          </div>
          <div className="flex items-baseline gap-1.5">
            <span className="font-['Space_Grotesk'] font-bold text-[#e2e0fc] tracking-tight text-lg">
              BanTRel
            </span>
            <span className="font-mono text-[0.65rem] text-[#c5c0ff] px-1.5 py-0.5 rounded bg-[#28283d] border border-[#474552]">
              v1.0-rl
            </span>
          </div>
        </Link>

        {/* Desktop nav */}
        <nav className="hidden md:flex items-center gap-8 h-16">
          <NavLink to="/" end className={linkClass}>Home</NavLink>
          <NavLink to="/simulate" className={linkClass}>Simulate</NavLink>
          <NavLink to="/about" className={linkClass}>About</NavLink>
        </nav>

        {/* Right cluster */}
        <div className="flex items-center gap-3">
          {/* Real engine status — driven by GET /health */}
          <div className="hidden sm:flex items-center gap-2 px-2.5 py-1 rounded-full bg-[#1e1e32] border border-[#474552] font-mono text-[0.65rem] text-[#c8c4d3]">
            <span className={`w-2 h-2 rounded-full ${ENGINE_DOT[engineStatus]}`} />
            <span>{ENGINE_LABEL[engineStatus]}</span>
          </div>
          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            title="Source Code on GitHub"
            className="p-2 rounded-lg text-[#c8c4d3] hover:text-[#e2e0fc] bg-[#28283d]/60 border border-[#474552] hover:border-[#a29bfe] transition-all duration-150 flex items-center justify-center"
          >
            <span className="material-symbols-outlined text-lg">code</span>
          </a>
          <Link
            to="/simulate"
            className="bg-[#a29bfe] text-[#2a1f7e] hover:bg-[#c5c0ff] font-['JetBrains_Mono'] font-semibold text-xs px-4 py-2 rounded-lg flex items-center gap-1.5 transition-all duration-150 active:scale-[0.98] shadow-[0_0_12px_rgba(162,155,254,0.25)]"
          >
            <span className="material-symbols-outlined text-base">smart_toy</span>
            <span>Launch Sim</span>
          </Link>

          {/* Mobile hamburger */}
          <button
            className="md:hidden p-2 rounded-lg text-[#c8c4d3] hover:text-[#e2e0fc] hover:bg-[#28283d] transition-colors"
            onClick={() => setMobileOpen((o) => !o)}
            aria-label="Toggle navigation"
          >
            <span className="material-symbols-outlined">
              {mobileOpen ? 'close' : 'menu'}
            </span>
          </button>
        </div>
      </div>

      {/* Mobile nav panel */}
      {mobileOpen && (
        <div className="md:hidden bg-[#1a1a2e] border-t border-[#474552] px-6 py-4 flex flex-col gap-4">
          <NavLink to="/" end className={({ isActive }) => isActive ? 'text-[#c5c0ff] font-mono text-sm' : 'text-[#c8c4d3] font-mono text-sm hover:text-[#e2e0fc]'} onClick={() => setMobileOpen(false)}>Home</NavLink>
          <NavLink to="/simulate" className={({ isActive }) => isActive ? 'text-[#c5c0ff] font-mono text-sm' : 'text-[#c8c4d3] font-mono text-sm hover:text-[#e2e0fc]'} onClick={() => setMobileOpen(false)}>Simulate</NavLink>
          <NavLink to="/about" className={({ isActive }) => isActive ? 'text-[#c5c0ff] font-mono text-sm' : 'text-[#c8c4d3] font-mono text-sm hover:text-[#e2e0fc]'} onClick={() => setMobileOpen(false)}>About</NavLink>
        </div>
      )}
    </header>
  );
}
