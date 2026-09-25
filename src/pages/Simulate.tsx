// src/pages/Simulate.tsx
import { useDemandForm } from '../hooks/useDemandForm';
import { DemandModeToggle } from '../components/simulate/DemandModeToggle';
import { PresetPeriodSelect } from '../components/simulate/PresetPeriodSelect';
import { CustomDemandForm } from '../components/simulate/CustomDemandForm';
import { PolicySelect } from '../components/simulate/PolicySelect';
import { AdvancedOptions } from '../components/simulate/AdvancedOptions';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';

export function Simulate() {
  const { formState, setField, isValid, errors, submit, isSubmitting, submitError } =
    useDemandForm();

  return (
    <div className="min-h-screen relative">
      <div className="fixed inset-0 grid-lines pointer-events-none opacity-20 z-0" />

      <main className="relative z-10 max-w-5xl mx-auto px-4 sm:px-6 py-10 md:py-14">

        {/* Header */}
        <div className="mb-8 pb-6 border-b border-[#474552]/60">
          <div className="flex items-center gap-2 mb-2 font-mono text-xs text-[#c5c0ff] tracking-widest uppercase">
            <span className="material-symbols-outlined text-base">tune</span>
            Reinforcement Learning Benchmark Setup
          </div>
          <h1 className="font-['Space_Grotesk'] font-bold text-3xl md:text-4xl text-[#e2e0fc] tracking-tight">
            Configure Your Simulation
          </h1>
          <p className="text-[#c8c4d3] mt-2 text-sm">
            Set traffic volume, modal split, and dispatch policies for the SUMO simulation.
          </p>
        </div>

        <div className="grid md:grid-cols-[1fr_300px] gap-8">

          {/* ── Form column ── */}
          <div className="space-y-6">

            {/* Step 1: Mode */}
            <Card className="p-5 space-y-4">
              <div className="flex items-center gap-2">
                <span className="w-5 h-5 rounded-full bg-[#a29bfe] text-[#2a1f7e] font-mono font-bold text-xs flex items-center justify-center">1</span>
                <h2 className="font-['Space_Grotesk'] font-semibold text-[#e2e0fc]">Traffic Demand Mode</h2>
              </div>
              <DemandModeToggle
                value={formState.mode}
                onChange={(m) => setField('mode', m)}
              />
            </Card>

            {/* Step 2: Preset or Custom */}
            <Card className="p-5 space-y-4">
              <div className="flex items-center gap-2">
                <span className="w-5 h-5 rounded-full bg-[#a29bfe] text-[#2a1f7e] font-mono font-bold text-xs flex items-center justify-center">2</span>
                <h2 className="font-['Space_Grotesk'] font-semibold text-[#e2e0fc]">
                  {formState.mode === 'preset' ? 'Scenario Period' : 'Custom Demand Parameters'}
                </h2>
              </div>
              {formState.mode === 'preset' ? (
                <PresetPeriodSelect
                  value={formState.period}
                  onChange={(p) => setField('period', p)}
                />
              ) : (
                <CustomDemandForm
                  state={formState}
                  setField={setField}
                  pctError={errors.pct_sum}
                />
              )}
            </Card>

            {/* Step 3: Policy */}
            <Card className="p-5 space-y-4">
              <div className="flex items-center gap-2">
                <span className="w-5 h-5 rounded-full bg-[#a29bfe] text-[#2a1f7e] font-mono font-bold text-xs flex items-center justify-center">3</span>
                <h2 className="font-['Space_Grotesk'] font-semibold text-[#e2e0fc]">Dispatch Policy</h2>
              </div>
              <PolicySelect
                value={formState.policy}
                onChange={(p) => setField('policy', p)}
              />
            </Card>

            {/* Step 4: Advanced */}
            <AdvancedOptions
              state={formState}
              setField={setField}
              nRunsError={errors.n_runs}
            />

            {/* Submit error */}
            {submitError && (
              <div className="flex items-start gap-3 p-4 rounded-xl bg-[rgba(231,76,60,0.08)] border border-[rgba(231,76,60,0.3)]">
                <span className="material-symbols-outlined text-[#e74c3c] text-base mt-0.5">error</span>
                <div>
                  <p className="font-semibold text-[#e74c3c] text-sm">Submission Failed</p>
                  <p className="font-mono text-xs text-[#c8c4d3] mt-1">{submitError}</p>
                </div>
              </div>
            )}

            {/* Submit */}
            <Button
              size="lg"
              variant="primary"
              className="w-full"
              disabled={!isValid}
              isLoading={isSubmitting}
              onClick={submit}
              id="submit-simulation"
            >
              <span className="material-symbols-outlined text-xl">rocket_launch</span>
              {isSubmitting ? 'Launching simulation…' : 'Launch Simulation'}
            </Button>

            {!isValid && (
              <p className="text-center font-mono text-xs text-[#928f9d]">
                Fix validation errors above to enable launch
              </p>
            )}
          </div>

          {/* ── Info sidebar ── */}
          <div className="space-y-4">
            <Card className="p-4 space-y-3">
              <div className="flex items-center gap-2">
                <span className="material-symbols-outlined text-[#c5c0ff] text-base">info</span>
                <h3 className="font-['Space_Grotesk'] font-semibold text-sm text-[#e2e0fc]">About This Tool</h3>
              </div>
              <p className="font-['Inter'] text-[#928f9d] text-xs leading-relaxed">
                Submits your configuration to a FastAPI backend that runs SUMO traffic simulations and returns comparison metrics between the PPO agent and fixed-cycle baseline.
              </p>
            </Card>

            <Card className="p-4 space-y-3">
              <div className="flex items-center gap-2">
                <span className="material-symbols-outlined text-[#4ae183] text-base">schedule</span>
                <h3 className="font-['Space_Grotesk'] font-semibold text-sm text-[#e2e0fc]">Estimated Time</h3>
              </div>
              <div className="space-y-2">
                {[
                  { label: 'Preset (1 run)', time: '~1–2 min' },
                  { label: 'Custom (1 run)', time: '~2–3 min' },
                  { label: 'Compare Both', time: '~3–5 min' },
                  { label: '3 runs', time: '~3× per run' },
                ].map((r) => (
                  <div key={r.label} className="flex justify-between items-center">
                    <span className="font-mono text-[0.65rem] text-[#928f9d]">{r.label}</span>
                    <span className="font-mono text-[0.65rem] text-[#c5c0ff]">{r.time}</span>
                  </div>
                ))}
              </div>
            </Card>

            <Card className="p-4 space-y-2">
              <div className="flex items-center gap-2">
                <span className="material-symbols-outlined text-[#ffb4a9] text-base">analytics</span>
                <h3 className="font-['Space_Grotesk'] font-semibold text-sm text-[#e2e0fc]">9 Tracked Metrics</h3>
              </div>
              {[
                'Total Stopped', 'Total Wait Time', 'Mean Wait Time',
                'Mean Speed', 'Avg Wait Time', 'Avg Travel Time',
                'Queue Length', 'Throughput', 'Delay',
              ].map((m) => (
                <div key={m} className="flex items-center gap-1.5">
                  <span className="w-1 h-1 rounded-full bg-[#a29bfe]" />
                  <span className="font-mono text-[0.6rem] text-[#928f9d]">{m}</span>
                </div>
              ))}
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
}
