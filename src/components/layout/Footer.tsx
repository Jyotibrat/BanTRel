// src/components/layout/Footer.tsx
import { Link } from 'react-router-dom';

export function Footer() {
  return (
    <footer className="border-t border-[#474552] bg-[#0c0c1f] mt-auto">
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6">

          {/* Brand */}
          <div className="flex items-center gap-2">
            <span className="font-['Space_Grotesk'] font-bold text-[#e2e0fc] text-base tracking-tight">
              BanTRel
            </span>
            <span className="font-mono text-[0.6rem] text-[#928f9d]">
              PPO Traffic Optimization
            </span>
          </div>

          {/* Links */}
          <nav className="flex items-center gap-6 font-mono text-xs text-[#928f9d]">
            <Link to="/" className="hover:text-[#c5c0ff] transition-colors">Home</Link>
            <Link to="/simulate" className="hover:text-[#c5c0ff] transition-colors">Simulate</Link>
            <Link to="/about" className="hover:text-[#c5c0ff] transition-colors">About</Link>
            <a
              href="https://github.com"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1 hover:text-[#c5c0ff] transition-colors"
            >
              <span className="material-symbols-outlined text-base">code</span>
              GitHub
            </a>
            <a
              href="https://huggingface.co"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1 hover:text-[#c5c0ff] transition-colors"
            >
              <span className="material-symbols-outlined text-base">hub</span>
              HuggingFace
            </a>
          </nav>

          {/* Copyright */}
          <p className="font-mono text-[0.6rem] text-[#474552]">
            SUMO-based RL · PPO Agent · Bangalore Intersection
          </p>
        </div>
      </div>
    </footer>
  );
}
