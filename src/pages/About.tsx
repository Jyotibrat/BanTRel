// src/pages/About.tsx
import { Card } from '../components/ui/Card';
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/Button';

const RL_SECTIONS = [
  {
    icon: 'visibility',
    color: '#c5c0ff',
    title: 'State Space',
    items: [
      'Per-lane queue lengths (vehicles waiting)',
      'Per-phase elapsed green time',
      'Current active signal phase (one-hot encoded)',
      'Time-of-day normalized to [0, 1]',
      'Vehicle density per approach arm',
    ],
    body: 'The agent observes a 28-dimensional state vector capturing the instantaneous traffic situation at all 4 arms of the intersection.',
  },
  {
    icon: 'star',
    color: '#4ae183',
    title: 'Reward Function',
    items: [
      'Negative total waiting time per step',
      'Penalty for excessive queue overflow',
      'Bonus for throughput above rolling baseline',
      'Phase-change penalty to prevent thrashing',
    ],
    body: 'The reward is shaped to minimize aggregate cumulative delay while penalizing frequent unnecessary phase switches that cause confusion at the physical intersection.',
  },
  {
    icon: 'psychology',
    color: '#ffb4a9',
    title: 'PPO Architecture',
    items: [
      'Actor: 3-layer MLP [256, 128, 64] + tanh activation',
      'Critic: Shared trunk + separate value head',
      'Clip ratio ε = 0.2',
      'Entropy coefficient: 0.01',
      'Learning rate: 3×10⁻⁴ with linear decay',
    ],
    body: 'Proximal Policy Optimization with clipping prevents excessively large policy updates, providing stable convergence across diverse traffic distributions.',
  },
  {
    icon: 'tune',
    color: '#a29bfe',
    title: 'Training Hyperparameters',
    items: [
      '5M total environment steps',
      'Rollout buffer: 2048 steps',
      'Mini-batch size: 64',
      'GAE λ = 0.95, γ = 0.99',
      '10 PPO epochs per rollout batch',
    ],
    body: 'Training ran on a single NVIDIA T4 GPU via Colab Pro for approximately 4 hours. Evaluation uses deterministic greedy action selection.',
  },
];

const METRIC_DESCRIPTIONS = [
  { key: 'system_total_stopped',       label: 'Total Stopped',          desc: 'Sum of all stopped vehicles across all lanes at each timestep' },
  { key: 'system_total_waiting_time',  label: 'Total Waiting Time',     desc: 'Accumulated seconds all vehicles spent waiting (speed < 0.1 m/s)' },
  { key: 'system_mean_waiting_time',   label: 'Mean Waiting Time',      desc: 'Average per-vehicle time spent stationary at red phases' },
  { key: 'system_mean_speed',          label: 'Mean Speed',             desc: 'Average speed across all vehicles in the network (m/s)' },
  { key: 'avg_waiting_time',           label: 'Avg Wait Time',          desc: 'Mean waiting time per vehicle at intersection entry' },
  { key: 'avg_travel_time',            label: 'Avg Travel Time',        desc: 'Mean end-to-end time from entry to exit of the intersection' },
  { key: 'queue_length',               label: 'Queue Length',           desc: 'Mean number of vehicles queued per approach arm' },
  { key: 'throughput',                 label: 'Throughput',             desc: 'Vehicles exiting the intersection per simulation step' },
  { key: 'delay',                      label: 'Delay',                  desc: 'Additional travel time above free-flow speed per vehicle' },
];

export function About() {
  return (
    <div className="min-h-screen relative">
      <div className="fixed inset-0 grid-lines pointer-events-none opacity-20 z-0" />

      <main className="relative z-10 max-w-5xl mx-auto px-4 sm:px-6 py-10 md:py-14 space-y-14">

        {/* Header */}
        <div className="space-y-4">
          <div className="font-mono text-xs text-[#c5c0ff] tracking-widest uppercase">
            <span className="mr-2">⬤</span> How It Works
          </div>
          <h1 className="font-['Space_Grotesk'] font-bold text-4xl md:text-5xl text-[#e2e0fc] tracking-tight">
            Reinforcement Learning<br />for Traffic Control
          </h1>
          <p className="text-[#c8c4d3] text-lg leading-relaxed max-w-3xl">
            BanTRel trains a PPO agent in a <strong className="text-[#e2e0fc]">SUMO (Simulation of Urban MObility)</strong> environment to learn an optimal traffic signal policy at a 4-way Bangalore intersection — without hard-coded rules.
          </p>
        </div>

        {/* RL Sections */}
        <div className="grid md:grid-cols-2 gap-6">
          {RL_SECTIONS.map((section) => (
            <Card key={section.title} className="p-6 space-y-4">
              <div className="flex items-center gap-3">
                <div
                  className="w-10 h-10 rounded-xl flex items-center justify-center"
                  style={{ backgroundColor: `${section.color}18`, border: `1px solid ${section.color}30` }}
                >
                  <span
                    className="material-symbols-outlined text-xl"
                    style={{ color: section.color, fontVariationSettings: "'FILL' 1" }}
                  >
                    {section.icon}
                  </span>
                </div>
                <h2 className="font-['Space_Grotesk'] font-semibold text-lg text-[#e2e0fc]">
                  {section.title}
                </h2>
              </div>
              <p className="text-[#c8c4d3] text-sm leading-relaxed">{section.body}</p>
              <ul className="space-y-1.5">
                {section.items.map((item) => (
                  <li key={item} className="flex items-start gap-2">
                    <span className="w-1 h-1 rounded-full mt-1.5 flex-shrink-0" style={{ backgroundColor: section.color }} />
                    <span className="font-mono text-[0.7rem] text-[#928f9d] leading-relaxed">{item}</span>
                  </li>
                ))}
              </ul>
            </Card>
          ))}
        </div>

        {/* Metric glossary */}
        <div className="space-y-4">
          <h2 className="font-['Space_Grotesk'] font-semibold text-2xl text-[#e2e0fc]">
            9 Tracked Metrics
          </h2>
          <p className="text-[#c8c4d3] text-sm">
            Every simulation run reports all metrics for each policy that ran, plus timestep-resolution time-series data.
          </p>
          <div className="rounded-xl border border-[#474552] overflow-hidden">
            {METRIC_DESCRIPTIONS.map((m, i) => (
              <div
                key={m.key}
                className={`flex flex-col sm:flex-row sm:items-center gap-2 px-5 py-3.5 ${
                  i < METRIC_DESCRIPTIONS.length - 1 ? 'border-b border-[#474552]/50' : ''
                } ${i % 2 === 0 ? 'bg-[#111125]' : 'bg-[#0c0c1f]'}`}
              >
                <div className="sm:w-52 flex-shrink-0">
                  <span className="font-['Space_Grotesk'] font-semibold text-sm text-[#e2e0fc]">{m.label}</span>
                  <br />
                  <span className="font-mono text-[0.6rem] text-[#474552]">{m.key}</span>
                </div>
                <p className="text-[#928f9d] text-sm flex-1">{m.desc}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Baseline comparison */}
        <Card className="p-6" elevated>
          <div className="flex items-center gap-3 mb-4">
            <span className="material-symbols-outlined text-[#f39c12] text-2xl" style={{ fontVariationSettings: "'FILL' 1" }}>compare</span>
            <h2 className="font-['Space_Grotesk'] font-semibold text-lg text-[#e2e0fc]">vs. Fixed-Cycle Baseline</h2>
          </div>
          <p className="text-[#c8c4d3] text-sm leading-relaxed">
            The baseline runs a traditional <strong className="text-[#e2e0fc]">90-second fixed-cycle</strong> signal plan: 45s green for N-S, 10s yellow, 45s green for E-W, 10s yellow — repeated indefinitely regardless of actual traffic conditions. BanTRel's agent learns to adjust phase durations dynamically, cutting waiting time by up to 31% in heavy morning-rush scenarios.
          </p>
        </Card>

        {/* CTA */}
        <div className="pt-6 border-t border-[#474552]/40 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-[#928f9d] text-sm">
            Ready to see the agent in action?
          </p>
          <Link to="/simulate">
            <Button variant="primary" size="lg">
              <span className="material-symbols-outlined text-xl">rocket_launch</span>
              Run a Simulation
            </Button>
          </Link>
        </div>
      </main>
    </div>
  );
}
