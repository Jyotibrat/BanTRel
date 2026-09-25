// src/pages/Landing.tsx
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';

const STATS = [
  { value: '24.2%', label: 'Less Mean Wait Time', icon: 'timer', color: '#2ecc71' },
  { value: '18.7%', label: 'Higher Throughput',   icon: 'speed',  color: '#c5c0ff' },
  { value: '31.5%', label: 'Shorter Queue Length', icon: 'traffic', color: '#4ae183' },
  { value: '9 Metrics', label: 'Tracked Per Run',  icon: 'analytics', color: '#ffb4a9' },
];

function IntersectionSchematic() {
  return (
    <div className="relative w-64 h-64 mx-auto">
      {/* Road backgrounds */}
      <div className="absolute inset-0 grid-lines rounded-2xl opacity-30" />

      {/* Horizontal road */}
      <div className="absolute top-1/2 left-0 right-0 h-16 -translate-y-1/2 bg-[#1e1e32] border-y border-[#474552]" />
      {/* Vertical road */}
      <div className="absolute left-1/2 top-0 bottom-0 w-16 -translate-x-1/2 bg-[#1e1e32] border-x border-[#474552]" />

      {/* Center intersection box */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-16 h-16 bg-[#28283d] border border-[#a29bfe]/40 rounded flex items-center justify-center shadow-[0_0_20px_rgba(162,155,254,0.2)]">
        <span
          className="material-symbols-outlined text-[#a29bfe] text-3xl glow-pulse"
          style={{ fontVariationSettings: "'FILL' 1" }}
        >
          traffic
        </span>
      </div>

      {/* Signal indicators */}
      {/* North */}
      <div className="absolute top-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-1">
        <div className="w-3 h-3 rounded-full bg-[#2ecc71] shadow-[0_0_8px_#2ecc71]" />
        <div className="font-mono text-[0.5rem] text-[#928f9d]">N</div>
      </div>
      {/* South */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col-reverse items-center gap-1">
        <div className="w-3 h-3 rounded-full bg-[#e74c3c] shadow-[0_0_8px_#e74c3c]" />
        <div className="font-mono text-[0.5rem] text-[#928f9d]">S</div>
      </div>
      {/* East */}
      <div className="absolute right-8 top-1/2 -translate-y-1/2 flex items-center gap-1">
        <div className="font-mono text-[0.5rem] text-[#928f9d]">E</div>
        <div className="w-3 h-3 rounded-full bg-[#2ecc71] shadow-[0_0_8px_#2ecc71]" />
      </div>
      {/* West */}
      <div className="absolute left-8 top-1/2 -translate-y-1/2 flex items-center gap-1 flex-row-reverse">
        <div className="font-mono text-[0.5rem] text-[#928f9d]">W</div>
        <div className="w-3 h-3 rounded-full bg-[#f39c12] shadow-[0_0_8px_#f39c12]" />
      </div>

      {/* Corner labels */}
      {['NW', 'NE', 'SW', 'SE'].map((label, i) => (
        <div
          key={label}
          className={`absolute font-mono text-[0.45rem] text-[#474552] ${
            i === 0 ? 'top-2 left-2' :
            i === 1 ? 'top-2 right-2' :
            i === 2 ? 'bottom-2 left-2' :
                      'bottom-2 right-2'
          }`}
        >
          {label}
        </div>
      ))}
    </div>
  );
}

export function Landing() {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Atmospheric background */}
      <div className="fixed inset-0 grid-lines pointer-events-none opacity-30 z-0" />
      <div className="fixed top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[350px] bg-[rgba(162,155,254,0.05)] blur-[130px] rounded-full pointer-events-none z-0" />

      <main className="relative z-10 flex-1">

        {/* ── Hero ── */}
        <section className="max-w-7xl mx-auto px-6 pt-20 pb-16">
          <div className="max-w-4xl mx-auto text-center space-y-6">
            {/* Tag pill */}
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-[#28283d] border border-[#474552] text-[#c5c0ff] font-mono text-[0.65rem] tracking-widest uppercase">
              <span className="w-1.5 h-1.5 rounded-full bg-[#4ae183] animate-pulse" />
              Reinforcement Learning · SUMO Simulation · Bangalore
            </div>

            <h1 className="font-['Space_Grotesk'] font-bold text-5xl md:text-6xl text-[#e2e0fc] tracking-tight leading-[1.1]">
              AI-Optimized{' '}
              <span className="text-[#c5c0ff]">Traffic Signal</span>
              <br />
              Control at Scale
            </h1>

            <p className="font-['Inter'] text-[#c8c4d3] text-lg max-w-2xl mx-auto leading-relaxed">
              BanTRel deploys a <strong className="text-[#e2e0fc]">PPO reinforcement learning agent</strong> trained on a 4-way Bangalore intersection to outperform conventional fixed-cycle signal timing across 9 traffic metrics.
            </p>

            <div className="flex items-center justify-center gap-4 flex-wrap">
              <Link to="/simulate">
                <Button size="lg" variant="primary">
                  <span className="material-symbols-outlined text-xl">smart_toy</span>
                  Run a Simulation
                </Button>
              </Link>
              <Link to="/about">
                <Button size="lg" variant="secondary">
                  <span className="material-symbols-outlined text-xl">school</span>
                  How It Works
                </Button>
              </Link>
            </div>
          </div>
        </section>

        {/* ── Stats strip ── */}
        <section className="border-y border-[#474552] bg-[#0c0c1f]/80 py-8">
          <div className="max-w-7xl mx-auto px-6">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              {STATS.map((stat) => (
                <div key={stat.label} className="text-center space-y-1">
                  <div className="flex items-center justify-center gap-2">
                    <span className="material-symbols-outlined text-xl" style={{ color: stat.color }}>
                      {stat.icon}
                    </span>
                    <span className="font-mono font-bold text-2xl tabular" style={{ color: stat.color }}>
                      {stat.value}
                    </span>
                  </div>
                  <p className="font-['Inter'] text-[#928f9d] text-xs">{stat.label}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── Intersection Schematic + CTA ── */}
        <section className="max-w-7xl mx-auto px-6 py-20">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div className="space-y-6">
              <div className="font-mono text-xs text-[#a29bfe] tracking-widest uppercase">
                <span className="mr-2">⬤</span> Live Intersection Model
              </div>
              <h2 className="font-['Space_Grotesk'] font-bold text-3xl text-[#e2e0fc]">
                Bangalore 4-Way Intersection
              </h2>
              <p className="text-[#c8c4d3] leading-relaxed">
                A multi-phase signalized intersection where the PPO agent learns to minimize queue length and waiting time by dynamically adjusting green-phase durations against a fixed 90-second cycle baseline.
              </p>
              <div className="grid grid-cols-3 gap-3">
                {[
                  { label: 'Cars', pct: '50%', color: '#c5c0ff' },
                  { label: 'Motorcycles', pct: '35%', color: '#4ae183' },
                  { label: 'Auto-Rickshaws', pct: '15%', color: '#ffb4a9' },
                ].map((v) => (
                  <div key={v.label} className="text-center p-3 rounded-xl bg-[#1e1e32] border border-[#474552]">
                    <div className="font-mono font-bold tabular" style={{ color: v.color }}>{v.pct}</div>
                    <div className="font-mono text-[0.6rem] text-[#928f9d]">{v.label}</div>
                  </div>
                ))}
              </div>
            </div>
            <div className="flex justify-center">
              <Card className="p-8" elevated>
                <IntersectionSchematic />
                <p className="text-center font-mono text-[0.6rem] text-[#474552] mt-4">
                  Simplified 4-way intersection schematic · Signals animated at runtime
                </p>
              </Card>
            </div>
          </div>
        </section>

        {/* ── Feature cards ── */}
        <section className="max-w-7xl mx-auto px-6 pb-20">
          <div className="grid md:grid-cols-3 gap-6">
            {[
              {
                icon: 'smart_toy',
                color: '#c5c0ff',
                title: 'PPO Agent',
                body: 'Trained with Proximal Policy Optimization on SUMO simulation data across all 7 traffic period scenarios.',
              },
              {
                icon: 'compare',
                color: '#4ae183',
                title: 'Side-by-Side Benchmarking',
                body: 'Run both the RL agent and fixed-cycle baseline in the same scenario and compare 9 simultaneous traffic metrics.',
              },
              {
                icon: 'analytics',
                color: '#ffb4a9',
                title: 'Real-Time Telemetry',
                body: 'View timestep-resolution time-series charts for queue length, speed, throughput, waiting time, and more.',
              },
            ].map((card) => (
              <Card key={card.title} hoverable className="p-6 space-y-3">
                <span
                  className="material-symbols-outlined text-3xl"
                  style={{ color: card.color, fontVariationSettings: "'FILL' 1" }}
                >
                  {card.icon}
                </span>
                <h3 className="font-['Space_Grotesk'] font-semibold text-[#e2e0fc]">{card.title}</h3>
                <p className="text-[#928f9d] text-sm leading-relaxed">{card.body}</p>
              </Card>
            ))}
          </div>
        </section>

        {/* ── Final CTA ── */}
        <section className="border-t border-[#474552] bg-[rgba(162,155,254,0.04)] py-16">
          <div className="max-w-2xl mx-auto text-center space-y-5 px-6">
            <h2 className="font-['Space_Grotesk'] font-bold text-3xl text-[#e2e0fc]">
              Ready to benchmark the agent?
            </h2>
            <p className="text-[#c8c4d3]">
              Configure your traffic scenario and launch a SUMO simulation. Results stream in real-time.
            </p>
            <Link to="/simulate">
              <Button size="lg" variant="primary" className="glow-pulse">
                <span className="material-symbols-outlined text-xl">rocket_launch</span>
                Configure & Run Simulation
              </Button>
            </Link>
          </div>
        </section>
      </main>
    </div>
  );
}
