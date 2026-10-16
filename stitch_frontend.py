"""Self-contained responsive BanTRel landing page for the Gradio Space.

All CSS is embedded directly in STITCH_HTML as a <style> tag so it applies
regardless of how Gradio's css= parameter is scoped. Material Symbols icons
are replaced with inline SVGs so they render even if the icon font fails.
"""

from embedded_assets import LOGO_DATA_URI

# Only font preconnect links go in HEAD (no scripts, no Tailwind).
HEAD_HTML = r"""
<link rel="icon" type="image/x-icon" href="/favicon.ico" />
<link rel="shortcut icon" type="image/x-icon" href="/favicon.ico" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap" rel="stylesheet" />
"""

# Gradio's css= parameter is kept for the container-level resets only.
CUSTOM_CSS = r"""
.gradio-container {
  max-width: 100% !important;
  width: 100% !important;
  padding: 0 !important;
  margin: 0 !important;
  background: #f7f9fc !important;
}
.gradio-container .main,
.gradio-container .wrap,
.gradio-container .contain {
  max-width: 100% !important;
  width: 100% !important;
  padding: 0 !important;
  margin: 0 !important;
}
.gradio-container .block,
.gradio-container .form { border: 0 !important; box-shadow: none !important; }
.gradio-container footer:not(#bantrel-landing footer),
.gradio-container .built-with,
.gradio-container > [class*="footer"] { display: none !important; }
"""

# The full CSS lives here, inside the HTML, so it always travels with the markup.
_RAW_STITCH_HTML = r"""
<style>
:root {
  --bt-ink: #071a33;
  --bt-green: #00c878;
  --bt-green-deep: #006d3f;
  --bt-green-soft: #e7fbf2;
  --bt-bg: #f7f9fc;
  --bt-text: #13243a;
  --bt-muted: #536174;
  --bt-line: #dce3eb;
}

#bantrel-landing, #bantrel-landing * { box-sizing: border-box; }
#bantrel-landing {
  color: var(--bt-text);
  background: var(--bt-bg);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: 15px;
  line-height: 1.65;
  width: 100%;
  -webkit-font-smoothing: antialiased;
}
#bantrel-landing a { color: inherit; text-decoration: none; }
#bantrel-landing a:focus-visible { outline: 3px solid rgba(0,200,120,.55); outline-offset: 3px; }
#bantrel-landing .bt-shell { width: min(1180px, calc(100% - 56px)); margin-inline: auto; }
#bantrel-landing .bt-eyebrow { color: var(--bt-green-deep); font: 700 11px/1.4 "JetBrains Mono", monospace; letter-spacing: .14em; text-transform: uppercase; }
#bantrel-landing .bt-section { padding: 88px 0; border-bottom: 1px solid var(--bt-line); }
#bantrel-landing .bt-section-head { max-width: 720px; margin-bottom: 34px; }
#bantrel-landing h1, #bantrel-landing h2, #bantrel-landing h3, #bantrel-landing p { margin-top: 0; }
#bantrel-landing h1, #bantrel-landing h2, #bantrel-landing h3 {
  font-family: "Plus Jakarta Sans", Inter, sans-serif;
  letter-spacing: -.035em;
}
#bantrel-landing h1 { color: var(--bt-ink); font-size: clamp(2.7rem, 4.7vw, 4.15rem); line-height: 1.08; font-weight: 800; margin-bottom: 22px; }
#bantrel-landing h2 { color: var(--bt-ink); font-size: clamp(1.9rem, 3vw, 2.6rem); line-height: 1.18; font-weight: 700; margin-bottom: 14px; }
#bantrel-landing h3 { color: var(--bt-ink); font-size: 1.03rem; font-weight: 700; line-height: 1.4; margin-bottom: 10px; letter-spacing: -.02em; }
#bantrel-landing .bt-lead { color: var(--bt-muted); font-size: 17px; line-height: 1.8; max-width: 650px; margin-bottom: 0; }
#bantrel-landing .bt-btn {
  display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 9px;
  min-height: 46px; padding: 12px 18px; border-radius: 9px;
  font-weight: 700; font-size: 14px; border: none; cursor: pointer;
  transition: transform .18s ease, box-shadow .18s ease, background .18s ease;
  text-decoration: none !important;
}
#bantrel-landing .bt-btn:hover { transform: translateY(-1px); }
#bantrel-landing .bt-btn,
#bantrel-landing .bt-btn span,
#bantrel-landing .bt-btn .bt-svg-icon {
  color: inherit !important;
}
#bantrel-landing .bt-btn svg,
#bantrel-landing .bt-btn .bt-svg-icon svg {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  width: 16px !important; height: 16px !important;
  min-width: 16px !important; min-height: 16px !important;
  vertical-align: middle;
  flex-shrink: 0 !important;
  fill: currentColor !important;
  color: inherit !important;
}
#bantrel-landing .bt-btn-primary {
  color: #071A33 !important;
  background: var(--bt-green) !important;
  box-shadow: 0 5px 16px rgba(0,200,120,.14);
}
#bantrel-landing .bt-btn-primary:hover {
  background: #19d88b !important;
  box-shadow: 0 8px 22px rgba(0,200,120,.24);
}
#bantrel-landing .bt-btn-primary svg,
#bantrel-landing .bt-btn-primary .bt-svg-icon,
#bantrel-landing .bt-btn-primary .bt-svg-icon svg {
  fill: #071A33 !important;
  color: #071A33 !important;
}
#bantrel-landing .bt-btn-secondary {
  color: #071A33 !important;
  border: 1.5px solid #cbd5e1 !important;
  background: white !important;
}
#bantrel-landing .bt-btn-secondary:hover {
  background: #f2f6fa !important;
  border-color: #aab8c8 !important;
}
#bantrel-landing .bt-btn-secondary svg,
#bantrel-landing .bt-btn-secondary .bt-svg-icon,
#bantrel-landing .bt-btn-secondary .bt-svg-icon svg {
  fill: #071A33 !important;
  color: #071A33 !important;
}
#bantrel-landing .bt-svg-icon {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  width: 1em; height: 1em;
  vertical-align: middle;
}
#bantrel-landing .bt-svg-icon svg {
  width: 100%; height: 100%;
  fill: currentColor;
}

/* Navigation */
#bantrel-landing .bt-nav {
  position: sticky; top: 0; z-index: 20;
  background: rgba(255,255,255,.95);
  border-bottom: 1px solid rgba(220,227,235,.9);
  backdrop-filter: blur(14px);
}
#bantrel-landing .bt-nav-inner {
  display: flex; align-items: center; justify-content: space-between;
  gap: 24px; min-height: 72px;
}
#bantrel-landing .bt-brand { display: inline-flex; align-items: center; gap: 10px; flex-shrink: 0; }
#bantrel-landing .bt-brand-symbol,
#bantrel-landing .bt-brand-logo {
  display: inline-flex; align-items: center; justify-content: center;
  width: 38px; height: 38px; border-radius: 10px;
  object-fit: cover; flex-shrink: 0;
}
#bantrel-landing .bt-brand-symbol {
  background: var(--bt-ink); color: white;
}
#bantrel-landing .bt-wordmark {
  color: var(--bt-ink); font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 20px; line-height: 1; font-weight: 800; letter-spacing: -.05em;
}
#bantrel-landing .bt-wordmark span { color: var(--bt-green-deep); }
#bantrel-landing .bt-nav-links {
  display: flex; align-items: center; gap: 26px;
  color: #435165; font-size: 13px; font-weight: 600;
}
#bantrel-landing .bt-nav-links a:hover { color: var(--bt-green-deep); }
#bantrel-landing .bt-nav-action { flex-shrink: 0; }

/* Hero */
#bantrel-landing .bt-hero {
  padding: 76px 0 78px;
  background: radial-gradient(ellipse at 85% 20%, rgba(0,200,120,.08), transparent 32%), var(--bt-bg);
}
#bantrel-landing .bt-hero-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  align-items: center;
  gap: 52px;
}
#bantrel-landing .bt-pill {
  display: inline-flex; align-items: center; gap: 9px;
  padding: 7px 11px; margin-bottom: 22px;
  border-radius: 999px; border: 1px solid #b7eed6;
  background: var(--bt-green-soft); color: var(--bt-green-deep);
  font: 700 10px/1.4 "JetBrains Mono", monospace; letter-spacing: .1em;
}
#bantrel-landing .bt-pill-dot {
  width: 7px; height: 7px; border-radius: 50%;
  background: var(--bt-green); box-shadow: 0 0 0 4px rgba(0,200,120,.13);
  display: inline-block; flex-shrink: 0;
}
#bantrel-landing .bt-hero-copy .bt-lead { margin-bottom: 27px; }
#bantrel-landing .bt-actions { display: flex; flex-wrap: wrap; gap: 11px; }
#bantrel-landing .bt-meta {
  display: flex; align-items: center; flex-wrap: wrap;
  gap: 10px 13px; margin-top: 26px; padding-top: 18px;
  border-top: 1px solid var(--bt-line);
  color: var(--bt-ink); font: 700 12px/1.6 "JetBrains Mono", monospace;
}
#bantrel-landing .bt-meta span,
#bantrel-landing .bt-meta-item {
  color: var(--bt-ink) !important;
  font-weight: 700 !important;
  display: inline-flex; align-items: center; gap: 7px;
}
#bantrel-landing .bt-meta-dot {
  display: inline-block; width: 7px; height: 7px;
  background: var(--bt-green-deep); border-radius: 50%;
}

/* Diagram panel */
#bantrel-landing .bt-diagram-card {
  border: 1px solid #dbe3ec; border-radius: 16px; padding: 15px;
  background: rgba(255,255,255,.92); box-shadow: 0 22px 55px rgba(7,26,51,.08);
}
#bantrel-landing .bt-diagram-top {
  display: flex; justify-content: space-between; align-items: center;
  gap: 12px; padding: 1px 2px 13px; margin-bottom: 12px;
  border-bottom: 1px solid #e7edf3;
  color: #637083; font: 500 10px/1.5 "JetBrains Mono", monospace;
}
#bantrel-landing .bt-terminal-dots { display: inline-flex; gap: 5px; margin-right: 7px; }
#bantrel-landing .bt-terminal-dots i { width: 7px; height: 7px; display: block; border-radius: 50%; }
#bantrel-landing .bt-terminal-title { display: inline-flex; align-items: center; flex-wrap: wrap; }
#bantrel-landing .bt-status-label {
  display: inline-flex; align-items: center; padding: 4px 7px; border-radius: 5px;
  background: #e7fbf2; color: #006d3f; font-size: 9px; font-weight: 700;
  letter-spacing: .08em; text-transform: uppercase;
}
#bantrel-landing .bt-diagram {
  position: relative; overflow: hidden; border-radius: 10px;
  background: var(--bt-ink); aspect-ratio: 1 / 1; max-height: 440px;
}
#bantrel-landing .bt-diagram svg { display: block; width: 100%; height: 100%; }
#bantrel-landing .bt-float-tag {
  position: absolute; display: inline-flex; align-items: center; gap: 6px;
  max-width: calc(100% - 20px); padding: 6px 8px;
  border: 1px solid rgba(0,200,120,.32); border-radius: 6px;
  color: #f6fbff; background: rgba(7,26,51,.93);
  font: 500 9px/1.35 "JetBrains Mono", monospace;
}
#bantrel-landing .bt-float-tag.top { top: 12px; left: 12px; }
#bantrel-landing .bt-float-tag.bottom-left { bottom: 12px; left: 12px; }
#bantrel-landing .bt-float-tag.bottom-right { bottom: 12px; right: 12px; }
#bantrel-landing .bt-tag-dot { width: 6px; height: 6px; background: var(--bt-green); border-radius: 50%; flex-shrink: 0; }
#bantrel-landing .bt-diagram-foot {
  display: flex; justify-content: flex-end; align-items: center;
  gap: 12px; padding: 13px 2px 1px;
  color: #697689; font-size: 10px;
}
#bantrel-landing .bt-diagram-foot strong { color: var(--bt-ink); font: 500 10px "JetBrains Mono", monospace; }
#bantrel-landing .bt-flow-anim { animation: bt-flow 2.6s ease-in-out infinite; }
@keyframes bt-flow { 0%,100% { opacity: .4; } 50% { opacity: 1; } }

/* Feature cards */
#bantrel-landing .bt-section-alt { background: white; }
#bantrel-landing .bt-feature-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
}
#bantrel-landing .bt-card {
  padding: 25px; background: #fbfcfe;
  border: 1px solid var(--bt-line); border-radius: 13px;
  transition: border-color .2s ease, transform .2s ease, box-shadow .2s ease;
  display: flex; flex-direction: column;
}
#bantrel-landing .bt-card:hover { border-color: #9adfc2; transform: translateY(-2px); box-shadow: 0 13px 30px rgba(7,26,51,.05); }
#bantrel-landing .bt-feature-icon {
  width: 48px !important; height: 48px !important; min-width: 48px !important; min-height: 48px !important;
  display: flex !important; align-items: center !important; justify-content: center !important;
  margin-bottom: 21px; color: var(--bt-ink) !important;
  background: #eaf1f8 !important; border: 1px solid #d4e0ec; border-radius: 12px !important;
  flex-shrink: 0 !important;
}
#bantrel-landing .bt-feature-icon svg {
  display: block !important;
  width: 28px !important; height: 28px !important;
  min-width: 28px !important; min-height: 28px !important;
  flex-shrink: 0 !important;
  fill: #071A33 !important;
  color: #071A33 !important;
}
#bantrel-landing .bt-card-kicker { margin-bottom: 7px; color: #6e7b8d; font: 600 10px/1.4 "JetBrains Mono", monospace; letter-spacing: .1em; text-transform: uppercase; }
#bantrel-landing .bt-card > p { margin-bottom: 0; color: var(--bt-muted); font-size: 13px; line-height: 1.75; flex: 1; }
#bantrel-landing .bt-card-foot {
  display: flex !important; justify-content: space-between !important; align-items: center !important;
  gap: 10px; margin-top: 22px; padding-top: 14px;
  border-top: 1px solid #e6ecf2;
  color: var(--bt-green-deep) !important; font: 500 10px/1.5 "JetBrains Mono", monospace;
}
#bantrel-landing .bt-card-foot svg {
  display: inline-block !important;
  width: 16px !important; height: 16px !important;
  min-width: 16px !important; min-height: 16px !important;
  flex-shrink: 0 !important;
  fill: var(--bt-green-deep) !important;
  color: var(--bt-green-deep) !important;
}

/* How it works */
#bantrel-landing .bt-center-head { text-align: center; margin-inline: auto; }
#bantrel-landing .bt-center-head .bt-lead { margin-inline: auto; }
#bantrel-landing .bt-step-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
}
#bantrel-landing .bt-step {
  display: flex; flex-direction: column; min-height: 236px;
  padding: 21px; border: 1px solid var(--bt-line);
  border-radius: 12px; background: white;
}
#bantrel-landing .bt-step-top {
  display: flex; align-items: center; justify-content: space-between; margin-bottom: 21px;
}
#bantrel-landing .bt-step-number {
  padding: 4px 7px; border-radius: 5px;
  background: #e6fbf1; color: #007447;
  font: 700 10px "JetBrains Mono", monospace;
}
#bantrel-landing .bt-step-icon { color: #8b98a8; display: flex; align-items: center; }
#bantrel-landing .bt-step > p { color: var(--bt-muted); font-size: 12px; line-height: 1.7; margin-bottom: 18px; flex: 1; }
#bantrel-landing .bt-step-foot {
  display: flex; justify-content: space-between; align-items: center;
  gap: 6px; margin-top: auto; padding-top: 13px;
  border-top: 1px solid #e7edf3;
  color: #6e7b8d; font: 500 9px/1.5 "JetBrains Mono", monospace;
}
#bantrel-landing .bt-step-foot .bt-step-arrow { color: var(--bt-green-deep); }

/* Contributors */
#bantrel-landing .bt-contributor-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}
#bantrel-landing .bt-contributor {
  display: flex; flex-direction: column; min-height: 230px;
  padding: 22px; background: white;
  border: 1px solid var(--bt-line); border-radius: 13px;
  transition: border-color .2s ease, box-shadow .2s ease;
}
#bantrel-landing .bt-contributor:hover { border-color: #a6e6cc; box-shadow: 0 12px 26px rgba(7,26,51,.05); }
#bantrel-landing .bt-person { display: flex; align-items: center; gap: 12px; margin-bottom: 16px; }
#bantrel-landing .bt-avatar {
  width: 46px; height: 46px; display: flex; align-items: center; justify-content: center;
  flex-shrink: 0; border-radius: 50%;
  background: var(--bt-ink); color: white;
  font: 700 13px "Plus Jakarta Sans", sans-serif;
}
#bantrel-landing .bt-avatar.alt { background: #e8f0f7; color: var(--bt-ink); }
#bantrel-landing .bt-person h3 { font-size: 14px; margin: 0 0 3px; letter-spacing: -.02em; }
#bantrel-landing .bt-role { display: block; color: var(--bt-green-deep); font-size: 11px; line-height: 1.5; font-weight: 600; }
#bantrel-landing .bt-contributor > p { margin: 0 0 17px; color: var(--bt-muted); font-size: 12px; line-height: 1.75; flex: 1; }
#bantrel-landing .bt-profile-link {
  display: inline-flex; align-items: center; gap: 6px;
  margin-top: auto; padding-top: 13px; border-top: 1px solid #e7edf3;
  color: #344358 !important; font: 500 10px "JetBrains Mono", monospace;
}
#bantrel-landing .bt-profile-link:hover { color: var(--bt-green-deep) !important; }
#bantrel-landing .bt-contributor-links {
  display: flex; align-items: center; gap: 8px; flex-wrap: wrap;
  margin-top: auto; padding-top: 14px; border-top: 1px solid #e7edf3;
}
#bantrel-landing .bt-icon-link {
  display: inline-flex !important; align-items: center !important; justify-content: center !important;
  width: 38px !important; height: 38px !important; min-width: 38px !important; min-height: 38px !important;
  border-radius: 10px !important;
  background: #ffffff !important; border: 1.5px solid #cbd5e1 !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
  transition: all .18s ease;
  flex-shrink: 0 !important;
  text-decoration: none !important;
  cursor: pointer;
}
#bantrel-landing .bt-icon-link:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}
#bantrel-landing .bt-icon-link svg {
  width: 20px !important; height: 20px !important; min-width: 20px !important; min-height: 20px !important;
  display: block !important; flex-shrink: 0 !important;
}
#bantrel-landing .bt-icon-link.bt-icon-github {
  background: #f8fafc !important; border-color: #cbd5e1 !important;
}
#bantrel-landing .bt-icon-link.bt-icon-github svg {
  fill: #181717 !important;
}
#bantrel-landing .bt-icon-link.bt-icon-github:hover {
  background: #181717 !important; border-color: #181717 !important;
}
#bantrel-landing .bt-icon-link.bt-icon-github:hover svg {
  fill: #ffffff !important;
}
#bantrel-landing .bt-icon-link.bt-icon-hf {
  background: #fffbeb !important; border-color: #fde68a !important;
}
#bantrel-landing .bt-icon-link.bt-icon-hf svg {
  fill: #FF9D00 !important;
}
#bantrel-landing .bt-icon-link.bt-icon-hf:hover {
  background: #fef3c7 !important; border-color: #f59e0b !important;
}
#bantrel-landing .bt-icon-link.bt-icon-hf:hover svg {
  fill: #d97706 !important;
}
#bantrel-landing .bt-icon-link.bt-icon-portfolio {
  background: #f0f9ff !important; border-color: #bae6fd !important;
}
#bantrel-landing .bt-icon-link.bt-icon-portfolio svg {
  stroke: #0284c7 !important; fill: none !important;
}
#bantrel-landing .bt-icon-link.bt-icon-portfolio:hover {
  background: #e0f2fe !important; border-color: #0284c7 !important;
}
#bantrel-landing .bt-icon-link.bt-icon-portfolio:hover svg {
  stroke: #0369a1 !important;
}
#bantrel-landing .bt-contributor-badge {
  display: inline-flex; align-items: center; gap: 6px;
  color: #536174; font: 500 10px "JetBrains Mono", monospace;
  height: 32px;
}
#bantrel-landing .bt-centered-link { margin-top: 28px; text-align: center; }
#bantrel-landing .bt-text-link {
  display: inline-flex; align-items: center; gap: 7px;
  color: var(--bt-green-deep) !important; font-weight: 700; font-size: 13px;
}
#bantrel-landing .bt-text-link:hover { text-decoration: underline; text-underline-offset: 4px; }

/* CTA + footer */
#bantrel-landing .bt-cta-section { padding: 75px 0; }
#bantrel-landing .bt-cta {
  position: relative; overflow: hidden;
  padding: clamp(28px, 5vw, 58px); border-radius: 18px;
  background: var(--bt-ink); color: white;
}
#bantrel-landing .bt-cta::after {
  content: ""; position: absolute; top: -140px; right: -100px;
  width: 340px; height: 340px; border-radius: 50%;
  background: rgba(0,200,120,.12); filter: blur(4px); pointer-events: none;
}
#bantrel-landing .bt-cta-content { position: relative; z-index: 1; max-width: 690px; }
#bantrel-landing .bt-cta .bt-eyebrow { color: #73efb9; }
#bantrel-landing .bt-cta h2 { color: white; margin-top: 13px; }
#bantrel-landing .bt-cta p { max-width: 600px; color: #c3cfdd; font-size: 16px; line-height: 1.8; margin-bottom: 25px; }
#bantrel-landing .bt-cta .bt-btn-secondary {
  background: #ffffff !important;
  color: #071A33 !important;
  border: 1.5px solid #cbd5e1 !important;
}
#bantrel-landing .bt-cta .bt-btn-secondary:hover {
  background: #f1f5f9 !important;
  border-color: #94a3b8 !important;
  color: #071A33 !important;
}
#bantrel-landing .bt-cta .bt-btn-secondary svg,
#bantrel-landing .bt-cta .bt-btn-secondary .bt-svg-icon,
#bantrel-landing .bt-cta .bt-btn-secondary .bt-svg-icon svg {
  fill: #071A33 !important;
  color: #071A33 !important;
}
#bantrel-landing .bt-footer { background: white; border-top: 1px solid var(--bt-line); }
#bantrel-landing .bt-footer-main {
  display: flex; align-items: center; justify-content: space-between;
  gap: 24px; padding: 27px 0;
}
#bantrel-landing .bt-footer-blurb { display: flex; align-items: center; gap: 16px; }
#bantrel-landing .bt-footer-blurb p { max-width: 320px; margin: 0; color: var(--bt-muted); font-size: 11px; }
#bantrel-landing .bt-footer-links {
  display: flex; flex-wrap: wrap; align-items: center;
  justify-content: flex-end; gap: 16px;
  color: #536174; font-size: 11px; font-weight: 600;
}
#bantrel-landing .bt-footer-links a:hover { color: var(--bt-green-deep); }
#bantrel-landing .bt-copyright {
  padding: 13px 0; border-top: 1px solid #edf0f4;
  color: #748195; text-align: center;
  font: 500 9px/1.5 "JetBrains Mono", monospace;
}

/* Responsive */
@media (max-width: 960px) {
  #bantrel-landing .bt-hero-grid { grid-template-columns: 1fr; gap: 38px; }
  #bantrel-landing .bt-hero-copy { max-width: 780px; }
  #bantrel-landing .bt-diagram-card { max-width: 680px; width: 100%; margin-inline: auto; }
  #bantrel-landing .bt-feature-grid,
  #bantrel-landing .bt-contributor-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  #bantrel-landing .bt-step-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  #bantrel-landing .bt-nav-links { gap: 15px; }
  #bantrel-landing .bt-section { padding: 72px 0; }
}
@media (max-width: 680px) {
  #bantrel-landing .bt-shell { width: min(100% - 32px, 540px); }
  #bantrel-landing .bt-nav-inner { min-height: 64px; gap: 12px; }
  #bantrel-landing .bt-nav-links { display: none; }
  #bantrel-landing .bt-brand-symbol,
  #bantrel-landing .bt-brand-logo { width: 34px; height: 34px; }
  #bantrel-landing .bt-wordmark { font-size: 18px; }
  #bantrel-landing .bt-nav-action .bt-btn { min-height: 40px; padding: 9px 11px; font-size: 11px; }
  #bantrel-landing .bt-hero { padding: 55px 0 58px; }
  #bantrel-landing h1 { font-size: clamp(2.35rem, 10vw, 3.3rem); }
  #bantrel-landing .bt-lead { font-size: 15px; line-height: 1.75; }
  #bantrel-landing .bt-actions { flex-direction: column; align-items: stretch; width: 100%; }
  #bantrel-landing .bt-actions .bt-btn { width: 100%; }
  #bantrel-landing .bt-meta { gap: 8px 10px; font-size: 9px; }
  #bantrel-landing .bt-diagram-card { padding: 9px; border-radius: 12px; }
  #bantrel-landing .bt-diagram-top { font-size: 8px; }
  #bantrel-landing .bt-float-tag { font-size: 7px; padding: 4px 5px; }
  #bantrel-landing .bt-section { padding: 60px 0; }
  #bantrel-landing .bt-section-head { margin-bottom: 25px; }
  #bantrel-landing .bt-feature-grid,
  #bantrel-landing .bt-contributor-grid,
  #bantrel-landing .bt-step-grid { grid-template-columns: 1fr; }
  #bantrel-landing .bt-card,
  #bantrel-landing .bt-step,
  #bantrel-landing .bt-contributor { padding: 21px; }
  #bantrel-landing .bt-step { min-height: 0; }
  #bantrel-landing .bt-cta-section { padding: 52px 0; }
  #bantrel-landing .bt-cta { border-radius: 14px; }
  #bantrel-landing .bt-footer-main,
  #bantrel-landing .bt-footer-blurb { align-items: flex-start; flex-direction: column; }
  #bantrel-landing .bt-footer-links { justify-content: flex-start; gap: 12px 16px; }
}
@media (prefers-reduced-motion: reduce) {
  #bantrel-landing *, #bantrel-landing *::before, #bantrel-landing *::after {
    animation-duration: .01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: .01ms !important;
  }
}
</style>

<div id="bantrel-landing">
  <!-- ===== NAVIGATION ===== -->
  <header class="bt-nav">
    <div class="bt-shell bt-nav-inner">
      <a class="bt-brand" href="#top" aria-label="BanTRel home">
        <img class="bt-brand-logo" src="__LOGO_SRC__" alt="BanTRel Logo" width="38" height="38" onerror="if(!this.dataset.retried){this.dataset.retried='1';this.src='/assets/logo.png';}" />
        <span class="bt-wordmark">Ban<span>TRel</span></span>
      </a>
      <nav class="bt-nav-links" aria-label="Main navigation">
        <a href="#about">About</a>
        <a href="#how-it-works">How it works</a>
        <a href="#contributors">Contributors</a>
        <a href="https://github.com/Jyotibrat/BanTRel" target="_blank" rel="noopener noreferrer">GitHub
          <span class="bt-svg-icon" aria-hidden="true" style="font-size:14px">
            <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M19 19H5V5h7V3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7h-2v7zM14 3v2h3.59l-9.83 9.83 1.41 1.41L19 6.41V10h2V3h-7z"/></svg>
          </span>
        </a>
      </nav>
      <div class="bt-nav-action">
        <a class="bt-btn bt-btn-primary" href="https://bantrel.becore.space/" target="_blank" rel="noopener noreferrer">
          Open simulation
          <span class="bt-svg-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M19 19H5V5h7V3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7h-2v7zM14 3v2h3.59l-9.83 9.83 1.41 1.41L19 6.41V10h2V3h-7z"/></svg>
          </span>
        </a>
      </div>
    </div>
  </header>

  <main id="top">
    <!-- ===== HERO ===== -->
    <section class="bt-hero">
      <div class="bt-shell bt-hero-grid">
        <div class="bt-hero-copy">
          <h1>Smarter Traffic.<br>Intelligent Decisions.</h1>
          <p class="bt-lead">BanTRel explores reinforcement learning for adaptive traffic signal control, using simulated traffic environments to evaluate intelligent policies and understand their impact on traffic flow.</p>
          <div class="bt-actions">
            <a class="bt-btn bt-btn-primary" href="https://bantrel.becore.space/" target="_blank" rel="noopener noreferrer" style="color:#071A33;">
              Explore the simulation
              <span class="bt-svg-icon" aria-hidden="true" style="color:#071A33;">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="#071A33" style="width:16px;height:16px;fill:#071A33;color:#071A33;display:inline-block;" xmlns="http://www.w3.org/2000/svg"><path d="M12 4l-1.41 1.41L16.17 11H4v2h12.17l-5.58 5.59L12 20l8-8-8-8z"/></svg>
              </span>
            </a>
            <a class="bt-btn bt-btn-secondary" href="https://github.com/Jyotibrat/BanTRel" target="_blank" rel="noopener noreferrer" style="color:#071A33;">
              View on GitHub
              <span class="bt-svg-icon" aria-hidden="true" style="color:#071A33;">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="#071A33" style="width:16px;height:16px;fill:#071A33;color:#071A33;display:inline-block;" xmlns="http://www.w3.org/2000/svg"><path d="M19 19H5V5h7V3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7h-2v7zM14 3v2h3.59l-9.83 9.83 1.41 1.41L19 6.41V10h2V3h-7z"/></svg>
              </span>
            </a>
          </div>
          <div class="bt-meta">
            <span class="bt-meta-item"><i class="bt-meta-dot" aria-hidden="true"></i> PPO Actor-Critic</span>
            <span aria-hidden="true">•</span>
            <span class="bt-meta-item">SUMO Simulation</span>
            <span aria-hidden="true">•</span>
            <span class="bt-meta-item">PyTorch</span>
          </div>
        </div>

        <!-- Intersection diagram -->
        <div class="bt-diagram-card" aria-label="Illustration of an AI-controlled traffic intersection">
          <div class="bt-diagram-top">
            <span class="bt-terminal-title">
              <span class="bt-terminal-dots" aria-hidden="true">
                <i style="background:#ef4444"></i>
                <i style="background:#f59e0b"></i>
                <i style="background:#00c878"></i>
              </span>
              INTERSECTION_CTRL // PPO
            </span>
            <span class="bt-status-label">Concept view</span>
          </div>
          <div class="bt-diagram">
            <svg viewBox="0 0 400 400" role="img" aria-label="Four-way road intersection with green and red traffic flow indicators" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <pattern id="bt-grid" width="22" height="22" patternUnits="userSpaceOnUse">
                  <path d="M22 0H0V22" fill="none" stroke="#143152" stroke-width=".7"/>
                </pattern>
              </defs>
              <rect width="400" height="400" fill="#071A33"/>
              <rect width="400" height="400" fill="url(#bt-grid)"/>
              <rect x="150" width="100" height="400" fill="#102846"/>
              <rect y="150" width="400" height="100" fill="#102846"/>
              <rect x="150" y="150" width="100" height="100" fill="#183757" stroke="#294762" stroke-width="2"/>
              <g stroke="#a3b3c4" stroke-width="2" stroke-dasharray="7 7" opacity=".65">
                <path d="M200 0V145M200 255V400M0 200H145M255 200H400"/>
              </g>
              <g class="bt-flow-anim" stroke="#00C878" stroke-width="3" stroke-linecap="round" stroke-dasharray="8 5" fill="none">
                <path d="M174 35V132M174 268V360M226 360V268M226 132V35"/>
              </g>
              <g fill="#00C878">
                <path d="M168 128L174 140L180 128Z"/>
                <path d="M168 354L174 366L180 354Z"/>
                <path d="M220 272L226 260L232 272Z"/>
                <path d="M220 41L226 29L232 41Z"/>
              </g>
              <g>
                <rect x="79" y="163" width="24" height="11" rx="2" fill="#EF4444"/>
                <rect x="44" y="163" width="24" height="11" rx="2" fill="#77879a"/>
                <rect x="298" y="225" width="24" height="11" rx="2" fill="#EF4444"/>
                <rect x="333" y="225" width="24" height="11" rx="2" fill="#77879a"/>
              </g>
              <g fill="#00C878">
                <circle cx="140" cy="140" r="6"/>
                <circle cx="260" cy="260" r="6"/>
              </g>
              <g fill="#EF4444">
                <circle cx="260" cy="140" r="6"/>
                <circle cx="140" cy="260" r="6"/>
              </g>
              <circle cx="200" cy="200" r="26" fill="#071A33" stroke="#00C878" stroke-width="2" stroke-dasharray="4 4"/>
              <text x="200" y="204" fill="#83f0bd" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700">PPO</text>
            </svg>
            <span class="bt-float-tag top"><i class="bt-tag-dot" aria-hidden="true"></i> Adaptive signal policy</span>
            <span class="bt-float-tag bottom-left">SUMO · simulated traffic</span>
            <span class="bt-float-tag bottom-right">PPO ↔ environment</span>
          </div>
          <div class="bt-diagram-foot">
            <strong>SIMULATION CONCEPT</strong>
          </div>
        </div>
      </div>
    </section>

    <!-- ===== ABOUT ===== -->
    <section class="bt-section bt-section-alt" id="about">
      <div class="bt-shell">
        <div class="bt-section-head">
          <h2>Building a smarter way to manage traffic</h2>
          <p class="bt-lead">BanTRel combines reinforcement learning and microscopic traffic simulation to investigate adaptive traffic signal strategies. PPO-based control is evaluated against a fixed-cycle baseline under simulated conditions.</p>
        </div>
        <div class="bt-feature-grid">
          <article class="bt-card">
            <div class="bt-feature-icon">
              <svg viewBox="0 -960 960 960" width="28" height="28" fill="#071A33" style="width:28px;height:28px;fill:#071A33;display:block;" xmlns="http://www.w3.org/2000/svg"><path d="M390-120q-51 0-88-35.5T260-241q-60-8-100-53t-40-106q0-21 5.5-41.5T142-480q-11-18-16.5-38t-5.5-42q0-61 40-105.5t99-52.5q3-51 41-86.5t90-35.5q26 0 48.5 10t41.5 27q18-17 41-27t49-10q52 0 89.5 35t40.5 86q59 8 99.5 53T840-560q0 22-5.5 42T818-480q11 18 16.5 38.5T840-400q0 62-40.5 106.5T699-241q-5 50-41.5 85.5T570-120q-25 0-48.5-9.5T480-156q-19 17-42 26.5t-48 9.5Zm130-590v460q0 21 14.5 35.5T570-200q20 0 34.5-16t15.5-36q-21-8-38.5-21.5T550-306q-10-14-7.5-30t16.5-26q14-10 30-7.5t26 16.5q11 16 28 24.5t37 8.5q33 0 56.5-23.5T760-400q0-5-.5-10t-2.5-10q-17 10-36.5 15t-40.5 5q-17 0-28.5-11.5T640-440q0-17 11.5-28.5T680-480q33 0 56.5-23.5T760-560q0-33-23.5-56T680-640q-11 18-28.5 31.5T613-587q-16 6-31-1t-20-23q-5-16 1.5-31t22.5-20q15-5 24.5-18t9.5-30q0-21-14.5-35.5T570-760q-21 0-35.5 14.5T520-710Zm-80 460v-460q0-21-14.5-35.5T390-760q-21 0-35.5 14.5T340-710q0 16 9 29.5t24 18.5q16 5 23 20t2 31q-6 16-21 23t-31 1q-21-8-38.5-21.5T279-640q-32 1-55.5 24.5T200-560q0 33 23.5 56.5T280-480q17 0 28.5 11.5T320-440q0 17-11.5 28.5T280-400q-21 0-40.5-5T203-420q-2 5-2.5 10t-.5 10q0 33 23.5 56.5T280-320q20 0 37-8.5t28-24.5q10-14 26-16.5t30 7.5q14 10 16.5 26t-7.5 30q-14 19-32 33t-39 22q1 20 16 35.5t35 15.5q21 0 35.5-14.5T440-250Zm40-230Z"/></svg>
            </div>
            <div class="bt-card-kicker">Algorithmic engine</div>
            <h3>Reinforcement Learning</h3>
            <p>A Proximal Policy Optimization (PPO) agent selects traffic-signal actions from simulated intersection states, balancing competing traffic-flow objectives.</p>
            <div class="bt-card-foot">
              <span>PPO Actor-Critic</span>
              <svg viewBox="0 -960 960 960" width="16" height="16" fill="#006d3f" style="width:16px;height:16px;fill:#006d3f;display:inline-block;" xmlns="http://www.w3.org/2000/svg"><path d="M440-120v-240h80v80h320v80H520v80h-80Zm-320-80v-80h240v80H120Zm160-160v-80H120v-80h160v-80h80v240h-80Zm160-80v-80h400v80H440Zm160-160v-240h80v80h160v80H680v80h-80Zm-480-80v-80h400v80H120Z"/></svg>
            </div>
          </article>
          <article class="bt-card">
            <div class="bt-feature-icon">
              <svg viewBox="0 -960 960 960" width="28" height="28" fill="#071A33" style="width:28px;height:28px;fill:#071A33;display:block;" xmlns="http://www.w3.org/2000/svg"><path d="M240-200v40q0 17-11.5 28.5T200-120h-40q-17 0-28.5-11.5T120-160v-320l84-240q6-18 21.5-29t34.5-11h440q19 0 34.5 11t21.5 29l84 240v320q0 17-11.5 28.5T800-120h-40q-17 0-28.5-11.5T720-160v-40H240Zm-8-360h496l-42-120H274l-42 120Zm-32 80v200-200Zm100 160q25 0 42.5-17.5T360-380q0-25-17.5-42.5T300-440q-25 0-42.5 17.5T240-380q0 25 17.5 42.5T300-320Zm360 0q25 0 42.5-17.5T720-380q0-25-17.5-42.5T660-440q-25 0-42.5 17.5T600-380q0 25 17.5 42.5T660-320Zm-460 40h560v-200H200v200Z"/></svg>
            </div>
            <div class="bt-card-kicker">Microscopic world</div>
            <h3>Traffic Simulation</h3>
            <p>SUMO provides the microscopic multi-vehicle environment for evaluating synthetic traffic demand, intersection behavior, and signal-control strategies.</p>
            <div class="bt-card-foot">
              <span>TraCI Interface</span>
              <svg viewBox="0 -960 960 960" width="16" height="16" fill="#006d3f" style="width:16px;height:16px;fill:#006d3f;display:inline-block;" xmlns="http://www.w3.org/2000/svg"><path d="M240-40q-50 0-85-35t-35-85q0-50 35-85t85-35q14 0 26 3t23 8l57-71q-28-31-39-70t-5-78l-81-27q-17 25-43 40t-58 15q-50 0-85-35T0-580q0-50 35-85t85-35q50 0 85 35t35 85v8l81 28q20-36 53.5-61t75.5-32v-87q-39-11-64.5-42.5T360-840q0-50 35-85t85-35q50 0 85 35t35 85q0 42-26 73.5T510-724v87q42 7 75.5 32t53.5 61l81-28v-8q0-50 35-85t85-35q50 0 85 35t35 85q0 50-35 85t-85 35q-32 0-58.5-15T739-515l-81 27q6 39-5 77.5T614-340l57 70q11-5 23-7.5t26-2.5q50 0 85 35t35 85q0 50-35 85t-85 35q-50 0-85-35t-35-85q0-20 6.5-38.5T624-232l-57-71q-41 23-87.5 23T392-303l-56 71q11 15 17.5 33.5T360-160q0 50-35 85t-85 35ZM120-540q17 0 28.5-11.5T160-580q0-17-11.5-28.5T120-620q-17 0-28.5 11.5T80-580q0 17 11.5 28.5T120-540Zm120 420q17 0 28.5-11.5T280-160q0-17-11.5-28.5T240-200q-17 0-28.5 11.5T200-160q0 17 11.5 28.5T240-120Zm240-680q17 0 28.5-11.5T520-840q0-17-11.5-28.5T480-880q-17 0-28.5 11.5T440-840q0 17 11.5 28.5T480-800Zm0 440q42 0 71-29t29-71q0-42-29-71t-71-29q-42 0-71 29t-29 71q0 42 29 71t71 29Zm240 240q17 0 28.5-11.5T760-160q0-17-11.5-28.5T720-200q-17 0-28.5 11.5T680-160q0 17 11.5 28.5T720-120Zm120-420q17 0 28.5-11.5T880-580q0-17-11.5-28.5T840-620q-17 0-28.5 11.5T800-580q0 17 11.5 28.5T840-540ZM480-840ZM120-580Zm360 120Zm360-120ZM240-160Zm480 0Z"/></svg>
            </div>
          </article>
          <article class="bt-card">
            <div class="bt-feature-icon">
              <svg viewBox="0 -960 960 960" width="28" height="28" fill="#071A33" style="width:28px;height:28px;fill:#071A33;display:block;" xmlns="http://www.w3.org/2000/svg"><path d="M280-280h80v-200h-80v200Zm320 0h80v-400h-80v400Zm-160 0h80v-120h-80v120Zm0-200h80v-80h-80v80ZM200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H200Zm0-80h560v-560H200v560Zm0-560v560-560Z"/></svg>
            </div>
            <div class="bt-card-kicker">Benchmarking</div>
            <h3>Performance Evaluation</h3>
            <p>Simulation results can be compared using waiting time, queue length, throughput, speed, and delay metrics against a fixed-cycle baseline.</p>
            <div class="bt-card-foot">
              <span>Metric comparison</span>
              <svg viewBox="0 0 24 24" width="16" height="16" fill="#006d3f" style="width:16px;height:16px;fill:#006d3f;display:inline-block;" xmlns="http://www.w3.org/2000/svg"><path d="M3 20q-.825 0-1.412-.587Q1 18.825 1 18q0-.825.588-1.413Q2.175 16 3 16h.263q.112 0 .237.05l4.55-4.55Q8 11.375 8 11.262V11q0-.825.588-1.413Q9.175 9 10 9t1.413.587Q12 10.175 12 11q0 .05-.05.5l2.55 2.55q.125-.05.238-.05h.524q.113 0 .238.05l3.55-3.55q-.05-.125-.05-.238V10q0-.825.587-1.413Q20.175 8 21 8q.825 0 1.413.587Q23 9.175 23 10q0 .825-.587 1.412Q21.825 12 21 12h-.262q-.113 0-.238-.05l-3.55 3.55q.05.125.05.238V16q0 .825-.587 1.413Q15.825 18 15 18q-.825 0-1.412-.587Q13 16.825 13 16v-.262q0-.113.05-.238l-2.55-2.55q-.125.05-.238.05H10q-.05 0-.5-.05L4.95 17.5q.05.125.05.238V18q0 .825-.588 1.413Q3.825 20 3 20ZM4 9.975l-.625-1.35L2.025 8l1.35-.625L4 6.025l.625 1.35L5.975 8l-1.35.625ZM15 9l-.95-2.05L12 6l2.05-.95L15 3l.95 2.05L18 6l-2.05.95Z"/></svg>
            </div>
          </article>
        </div>
      </div>
    </section>

    <!-- ===== HOW IT WORKS ===== -->
    <section class="bt-section" id="how-it-works">
      <div class="bt-shell">
        <div class="bt-section-head bt-center-head">
          <h2>How it works</h2>
          <p class="bt-lead">A closed-loop simulation framework for investigating reinforcement-learning-based traffic control.</p>
        </div>
        <div class="bt-step-grid">
          <article class="bt-step">
            <div class="bt-step-top">
              <span class="bt-step-number">01</span>
              <span class="bt-step-icon" aria-hidden="true">
                <svg style="width:22px;height:22px;fill:#8b98a8" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M20 2H4c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-9 14H5v-2h6v2zm0-4H5v-2h6v2zm0-4H5V6h6v2zm8 8h-6v-2h6v2zm0-4h-6v-2h6v2zm0-4h-6V6h6v2z"/></svg>
              </span>
            </div>
            <h3>Traffic environment</h3>
            <p>SUMO simulates vehicle flows and supplies the state observations used by the control policy.</p>
            <div class="bt-step-foot">
              <span>State representation</span>
              <span class="bt-step-arrow">
                <svg style="width:16px;height:16px;fill:currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 4l-1.41 1.41L16.17 11H4v2h12.17l-5.58 5.59L12 20l8-8-8-8z"/></svg>
              </span>
            </div>
          </article>
          <article class="bt-step">
            <div class="bt-step-top">
              <span class="bt-step-number">02</span>
              <span class="bt-step-icon" aria-hidden="true">
                <svg style="width:22px;height:22px;fill:#8b98a8" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2c-4.97 0-9 4.03-9 9 0 4.17 2.84 7.67 6.69 8.69L12 22l2.31-2.31C18.16 18.67 21 15.17 21 11c0-4.97-4.03-9-9-9zm0 2c3.86 0 7 3.14 7 7s-3.14 7-7 7-7-3.14-7-7 3.14-7 7-7zm0 3c-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4-1.79-4-4-4zm0 2c1.1 0 2 .9 2 2s-.9 2-2 2-2-.9-2-2 .9-2 2-2z"/></svg>
              </span>
            </div>
            <h3>RL policy</h3>
            <p>The trained PPO policy processes observations and selects a signal-control action.</p>
            <div class="bt-step-foot">
              <span>Action selection</span>
              <span class="bt-step-arrow">
                <svg style="width:16px;height:16px;fill:currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 4l-1.41 1.41L16.17 11H4v2h12.17l-5.58 5.59L12 20l8-8-8-8z"/></svg>
              </span>
            </div>
          </article>
          <article class="bt-step">
            <div class="bt-step-top">
              <span class="bt-step-number">03</span>
              <span class="bt-step-icon" aria-hidden="true">
                <svg style="width:22px;height:22px;fill:#8b98a8" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
              </span>
            </div>
            <h3>Signal decisions</h3>
            <p>Actions are applied to the simulated intersection through the TraCI interface.</p>
            <div class="bt-step-foot">
              <span>Environment step</span>
              <span class="bt-step-arrow">
                <svg style="width:16px;height:16px;fill:currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 4l-1.41 1.41L16.17 11H4v2h12.17l-5.58 5.59L12 20l8-8-8-8z"/></svg>
              </span>
            </div>
          </article>
          <article class="bt-step">
            <div class="bt-step-top">
              <span class="bt-step-number">04</span>
              <span class="bt-step-icon" aria-hidden="true">
                <svg style="width:22px;height:22px;fill:#8b98a8" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M5 9.2h3V19H5V9.2zM10.6 5h2.8v14h-2.8V5zm5.6 8H19v6h-2.8v-6z"/></svg>
              </span>
            </div>
            <h3>Performance analysis</h3>
            <p>Collected metrics summarize the simulated run and support comparison with the baseline.</p>
            <div class="bt-step-foot">
              <span>Result comparison</span>
              <span class="bt-step-arrow">
                <svg style="width:16px;height:16px;fill:currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/></svg>
              </span>
            </div>
          </article>
        </div>
      </div>
    </section>

    <!-- ===== CONTRIBUTORS ===== -->
    <section class="bt-section bt-section-alt" id="contributors">
      <div class="bt-shell">
        <div class="bt-section-head">
          <h2>Project contributors</h2>
          <p class="bt-lead">BanTRel is made possible by people contributing to its research, engineering, simulation, and development.</p>
        </div>
        <div class="bt-contributor-grid">
          <!-- Bindupautra Jyotibrat -->
          <article class="bt-contributor">
            <div class="bt-person">
              <div class="bt-avatar">BJ</div>
              <div>
                <h3>Bindupautra Jyotibrat</h3>
                <span class="bt-role">Project Lead</span>
              </div>
            </div>
            <p>RL architecture, PPO agent, SUMO integration, and simulation environment pipeline.</p>
            <div class="bt-contributor-links">
              <a class="bt-icon-link bt-icon-github" href="https://github.com/Jyotibrat" target="_blank" rel="noopener noreferrer" title="GitHub Profile" aria-label="Bindupautra Jyotibrat on GitHub">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="#181717" xmlns="http://www.w3.org/2000/svg"><path d="M12 2A10 10 0 0 0 2 12c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0 0 12 2z"/></svg>
              </a>
              <a class="bt-icon-link bt-icon-hf" href="https://huggingface.co/BJyotibrat" target="_blank" rel="noopener noreferrer" title="Hugging Face Profile" aria-label="Bindupautra Jyotibrat on Hugging Face">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="#FF9D00" xmlns="http://www.w3.org/2000/svg"><path d="M12.025 1.13c-5.77 0-10.449 4.647-10.449 10.378 0 1.112.178 2.181.503 3.185.064-.222.203-.444.416-.577a.96.96 0 0 1 .524-.15c.293 0 .584.124.84.284.278.173.48.408.71.694.226.282.458.611.684.951v-.014c.017-.324.106-.622.264-.874s.403-.487.762-.543c.3-.047.596.06.787.203s.31.313.4.467c.15.257.212.468.233.542.01.026.653 1.552 1.657 2.54.616.605 1.01 1.223 1.082 1.912.055.537-.096 1.059-.38 1.572.637.121 1.294.187 1.967.187.657 0 1.298-.063 1.921-.178-.287-.517-.44-1.041-.384-1.581.07-.69.465-1.307 1.081-1.913 1.004-.987 1.647-2.513 1.657-2.539.021-.074.083-.285.233-.542.09-.154.208-.323.4-.467a1.08 1.08 0 0 1 .787-.203c.359.056.604.29.762.543s.247.55.265.874v.015c.225-.34.457-.67.683-.952.23-.286.432-.52.71-.694.257-.16.547-.284.84-.285a.97.97 0 0 1 .524.151c.228.143.373.388.43.625l.006.04a10.3 10.3 0 0 0 .534-3.273c0-5.731-4.678-10.378-10.449-10.378M8.327 6.583a1.5 1.5 0 0 1 .713.174 1.487 1.487 0 0 1 .617 2.013c-.183.343-.762-.214-1.102-.094-.38.134-.532.914-.917.71a1.487 1.487 0 0 1 .69-2.803m7.486 0a1.487 1.487 0 0 1 .689 2.803c-.385.204-.536-.576-.916-.71-.34-.12-.92.437-1.103.094a1.487 1.487 0 0 1 .617-2.013 1.5 1.5 0 0 1 .713-.174m-10.68 1.55a.96.96 0 1 1 0 1.921.96.96 0 0 1 0-1.92m13.838 0a.96.96 0 1 1 0 1.92.96.96 0 0 1 0-1.92M8.489 11.458c.588.01 1.965 1.157 3.572 1.164 1.607-.007 2.984-1.155 3.572-1.164.196-.003.305.12.305.454 0 .886-.424 2.328-1.563 3.202-.22-.756-1.396-1.366-1.63-1.32q-.011.001-.02.006l-.044.026-.01.008-.03.024q-.018.017-.035.036l-.032.04a1 1 0 0 0-.058.09l-.014.025q-.049.088-.11.19a1 1 0 0 1-.083.116 1.2 1.2 0 0 1-.173.18q-.035.029-.075.058a1.3 1.3 0 0 1-.251-.243 1 1 0 0 1-.076-.107c-.124-.193-.177-.363-.337-.444-.034-.016-.104-.008-.2.022q-.094.03-.216.087-.06.028-.125.063l-.13.074q-.067.04-.136.086a3 3 0 0 0-.135.096 3 3 0 0 0-.26.219 2 2 0 0 0-.12.121 2 2 0 0 0-.106.128l-.002.002a2 2 0 0 0-.09.132l-.001.001a1.2 1.2 0 0 0-.105.212q-.013.036-.024.073c-1.139-.875-1.563-2.317-1.563-3.203 0-.334.109-.457.305-.454m.836 10.354c.824-1.19.766-2.082-.365-3.194-1.13-1.112-1.789-2.738-1.789-2.738s-.246-.945-.806-.858-.97 1.499.202 2.362c1.173.864-.233 1.45-.685.64-.45-.812-1.683-2.896-2.322-3.295s-1.089-.175-.938.647 2.822 2.813 2.562 3.244-1.176-.506-1.176-.506-2.866-2.567-3.49-1.898.473 1.23 2.037 2.16c1.564.932 1.686 1.178 1.464 1.53s-3.675-2.511-4-1.297c-.323 1.214 3.524 1.567 3.287 2.405-.238.839-2.71-1.587-3.216-.642-.506.946 3.49 2.056 3.522 2.064 1.29.33 4.568 1.028 5.713-.624m5.349 0c-.824-1.19-.766-2.082.365-3.194 1.13-1.112 1.789-2.738 1.789-2.738s.246-.945.806-.858.97 1.499-.202 2.362c-1.173.864.233 1.45.685.64.451-.812 1.683-2.896 2.322-3.295s1.089-.175.938.647-2.822 2.813-2.562 3.244 1.176-.506 1.176-.506 2.866-2.567 3.49-1.898-.473 1.23-2.037 2.16c-1.564.932-1.686 1.178-1.464 1.53s3.675-2.511 4-1.297c.323 1.214-3.524 1.567-3.287 2.405.238.839 2.71-1.587 3.216-.642.506.946-3.49 2.056-3.522 2.064-1.29.33-4.568 1.028-5.713-.624"/></svg>
              </a>
              <a class="bt-icon-link bt-icon-portfolio" href="https://becore.space/" target="_blank" rel="noopener noreferrer" title="Personal Portfolio" aria-label="Bindupautra Jyotibrat's Portfolio">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#0284c7" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>
              </a>
            </div>
          </article>
          <!-- Rana Talukdar -->
          <article class="bt-contributor">
            <div class="bt-person">
              <div class="bt-avatar alt">RT</div>
              <div>
                <h3>Rana Talukdar</h3>
                <span class="bt-role">Core contributor</span>
              </div>
            </div>
            <p>Simulation environment, reward-function engineering, and benchmark baselines.</p>
            <div class="bt-contributor-links">
              <a class="bt-icon-link bt-icon-github" href="https://github.com/Auth0r-C0dez" target="_blank" rel="noopener noreferrer" title="GitHub Profile" aria-label="Rana Talukdar on GitHub">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="#181717" xmlns="http://www.w3.org/2000/svg"><path d="M12 2A10 10 0 0 0 2 12c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0 0 12 2z"/></svg>
              </a>
              <a class="bt-icon-link bt-icon-hf" href="https://huggingface.co/Rana-15" target="_blank" rel="noopener noreferrer" title="Hugging Face Profile" aria-label="Rana Talukdar on Hugging Face">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="#FF9D00" xmlns="http://www.w3.org/2000/svg"><path d="M12.025 1.13c-5.77 0-10.449 4.647-10.449 10.378 0 1.112.178 2.181.503 3.185.064-.222.203-.444.416-.577a.96.96 0 0 1 .524-.15c.293 0 .584.124.84.284.278.173.48.408.71.694.226.282.458.611.684.951v-.014c.017-.324.106-.622.264-.874s.403-.487.762-.543c.3-.047.596.06.787.203s.31.313.4.467c.15.257.212.468.233.542.01.026.653 1.552 1.657 2.54.616.605 1.01 1.223 1.082 1.912.055.537-.096 1.059-.38 1.572.637.121 1.294.187 1.967.187.657 0 1.298-.063 1.921-.178-.287-.517-.44-1.041-.384-1.581.07-.69.465-1.307 1.081-1.913 1.004-.987 1.647-2.513 1.657-2.539.021-.074.083-.285.233-.542.09-.154.208-.323.4-.467a1.08 1.08 0 0 1 .787-.203c.359.056.604.29.762.543s.247.55.265.874v.015c.225-.34.457-.67.683-.952.23-.286.432-.52.71-.694.257-.16.547-.284.84-.285a.97.97 0 0 1 .524.151c.228.143.373.388.43.625l.006.04a10.3 10.3 0 0 0 .534-3.273c0-5.731-4.678-10.378-10.449-10.378M8.327 6.583a1.5 1.5 0 0 1 .713.174 1.487 1.487 0 0 1 .617 2.013c-.183.343-.762-.214-1.102-.094-.38.134-.532.914-.917.71a1.487 1.487 0 0 1 .69-2.803m7.486 0a1.487 1.487 0 0 1 .689 2.803c-.385.204-.536-.576-.916-.71-.34-.12-.92.437-1.103.094a1.487 1.487 0 0 1 .617-2.013 1.5 1.5 0 0 1 .713-.174m-10.68 1.55a.96.96 0 1 1 0 1.921.96.96 0 0 1 0-1.92m13.838 0a.96.96 0 1 1 0 1.92.96.96 0 0 1 0-1.92M8.489 11.458c.588.01 1.965 1.157 3.572 1.164 1.607-.007 2.984-1.155 3.572-1.164.196-.003.305.12.305.454 0 .886-.424 2.328-1.563 3.202-.22-.756-1.396-1.366-1.63-1.32q-.011.001-.02.006l-.044.026-.01.008-.03.024q-.018.017-.035.036l-.032.04a1 1 0 0 0-.058.09l-.014.025q-.049.088-.11.19a1 1 0 0 1-.083.116 1.2 1.2 0 0 1-.173.18q-.035.029-.075.058a1.3 1.3 0 0 1-.251-.243 1 1 0 0 1-.076-.107c-.124-.193-.177-.363-.337-.444-.034-.016-.104-.008-.2.022q-.094.03-.216.087-.06.028-.125.063l-.13.074q-.067.04-.136.086a3 3 0 0 0-.135.096 3 3 0 0 0-.26.219 2 2 0 0 0-.12.121 2 2 0 0 0-.106.128l-.002.002a2 2 0 0 0-.09.132l-.001.001a1.2 1.2 0 0 0-.105.212q-.013.036-.024.073c-1.139-.875-1.563-2.317-1.563-3.203 0-.334.109-.457.305-.454m.836 10.354c.824-1.19.766-2.082-.365-3.194-1.13-1.112-1.789-2.738-1.789-2.738s-.246-.945-.806-.858-.97 1.499.202 2.362c1.173.864-.233 1.45-.685.64-.45-.812-1.683-2.896-2.322-3.295s-1.089-.175-.938.647 2.822 2.813 2.562 3.244-1.176-.506-1.176-.506-2.866-2.567-3.49-1.898.473 1.23 2.037 2.16c1.564.932 1.686 1.178 1.464 1.53s-3.675-2.511-4-1.297c-.323 1.214 3.524 1.567 3.287 2.405-.238.839-2.71-1.587-3.216-.642-.506.946 3.49 2.056 3.522 2.064 1.29.33 4.568 1.028 5.713-.624m5.349 0c-.824-1.19-.766-2.082.365-3.194 1.13-1.112 1.789-2.738 1.789-2.738s.246-.945.806-.858.97 1.499-.202 2.362c-1.173.864.233 1.45.685.64.451-.812 1.683-2.896 2.322-3.295s1.089-.175.938.647-2.822 2.813-2.562 3.244 1.176-.506 1.176-.506 2.866-2.567 3.49-1.898-.473 1.23-2.037 2.16c-1.564.932-1.686 1.178-1.464 1.53s3.675-2.511 4-1.297c.323 1.214-3.524 1.567-3.287 2.405.238.839 2.71-1.587 3.216-.642.506.946-3.49 2.056-3.522 2.064-1.29.33-4.568 1.028-5.713-.624"/></svg>
              </a>
              <a class="bt-icon-link bt-icon-portfolio" href="https://devwithrana.vercel.app/" target="_blank" rel="noopener noreferrer" title="Personal Portfolio" aria-label="Rana Talukdar's Portfolio">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#0284c7" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>
              </a>
            </div>
          </article>
          <!-- Daiwik Paul Chowdhury -->
          <article class="bt-contributor">
            <div class="bt-person">
              <div class="bt-avatar alt">DP</div>
              <div>
                <h3>Daiwik Paul Chowdhury</h3>
                <span class="bt-role">Core contributor</span>
              </div>
            </div>
            <p>TraCI interface integration, model optimization, and traffic telemetry.</p>
            <div class="bt-contributor-links">
              <a class="bt-icon-link bt-icon-github" href="https://github.com/daiwikpc" target="_blank" rel="noopener noreferrer" title="GitHub Profile" aria-label="Daiwik Paul Chowdhury on GitHub">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="#181717" xmlns="http://www.w3.org/2000/svg"><path d="M12 2A10 10 0 0 0 2 12c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0 0 12 2z"/></svg>
              </a>
            </div>
          </article>
          <!-- Navjot Singh Gill -->
          <article class="bt-contributor">
            <div class="bt-person">
              <div class="bt-avatar alt">NG</div>
              <div>
                <h3>Navjot Singh Gill</h3>
                <span class="bt-role">Contributor</span>
              </div>
            </div>
            <p>Performance benchmarks, data analysis, and deployment infrastructure.</p>
            <div class="bt-contributor-links">
              <a class="bt-icon-link bt-icon-github" href="https://github.com/NAVJOT2005" target="_blank" rel="noopener noreferrer" title="GitHub Profile" aria-label="Navjot Singh Gill on GitHub">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="#181717" xmlns="http://www.w3.org/2000/svg"><path d="M12 2A10 10 0 0 0 2 12c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0 0 12 2z"/></svg>
              </a>
            </div>
          </article>
          <!-- Chandril Ghosh -->
          <article class="bt-contributor">
            <div class="bt-person">
              <div class="bt-avatar alt">CG</div>
              <div>
                <h3>Chandril Ghosh</h3>
                <span class="bt-role">Contributor</span>
              </div>
            </div>
            <p>Urban intersection topology, vehicle-flow scenarios, and testing.</p>
            <div class="bt-contributor-links">
              <span class="bt-contributor-badge">
                <svg style="width:14px;height:14px;fill:currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/></svg>
                Project contributor
              </span>
            </div>
          </article>
          <!-- Rupanjan Paul -->
          <article class="bt-contributor">
            <div class="bt-person">
              <div class="bt-avatar alt">RP</div>
              <div>
                <h3>Rupanjan Paul</h3>
                <span class="bt-role">Contributor</span>
              </div>
            </div>
            <p>State-space modeling, evaluation diagnostics, and metrics pipeline.</p>
            <div class="bt-contributor-links">
              <span class="bt-contributor-badge">
                <svg style="width:14px;height:14px;fill:currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/></svg>
                Project contributor
              </span>
            </div>
          </article>
        </div>
        <div class="bt-centered-link">
          <a class="bt-text-link" href="https://github.com/Jyotibrat/BanTRel" target="_blank" rel="noopener noreferrer">
            Explore the project on GitHub
            <svg style="width:14px;height:14px;fill:currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 4l-1.41 1.41L16.17 11H4v2h12.17l-5.58 5.59L12 20l8-8-8-8z"/></svg>
          </a>
        </div>
      </div>
    </section>

    <!-- ===== CTA ===== -->
    <section class="bt-cta-section">
      <div class="bt-shell">
        <div class="bt-cta">
          <div class="bt-cta-content">
            <div class="bt-eyebrow">Explore the live application</div>
            <h2>See BanTRel in action</h2>
            <p>Open the interactive simulation to experiment with traffic scenarios and compare signal-control strategies.</p>
            <div class="bt-actions">
              <a class="bt-btn bt-btn-primary" href="https://bantrel.becore.space/" target="_blank" rel="noopener noreferrer" style="color:#071A33;">
                Launch simulation
                <span class="bt-svg-icon" aria-hidden="true" style="color:#071A33;">
                  <svg viewBox="0 0 24 24" width="16" height="16" fill="#071A33" style="width:16px;height:16px;fill:#071A33;color:#071A33;display:inline-block;" xmlns="http://www.w3.org/2000/svg"><path d="M12 4l-1.41 1.41L16.17 11H4v2h12.17l-5.58 5.59L12 20l8-8-8-8z"/></svg>
                </span>
              </a>
              <a class="bt-btn bt-btn-secondary" href="https://github.com/Jyotibrat/BanTRel" target="_blank" rel="noopener noreferrer" style="color:#071A33;background:#ffffff;border-color:#cbd5e1;">
                Explore source code
                <span class="bt-svg-icon" aria-hidden="true" style="color:#071A33;">
                  <svg viewBox="0 0 24 24" width="16" height="16" fill="#071A33" style="width:16px;height:16px;fill:#071A33;color:#071A33;display:inline-block;" xmlns="http://www.w3.org/2000/svg"><path d="M19 19H5V5h7V3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7h-2v7zM14 3v2h3.59l-9.83 9.83 1.41 1.41L19 6.41V10h2V3h-7z"/></svg>
                </span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>

  <!-- ===== FOOTER ===== -->
  <footer class="bt-footer">
    <div class="bt-shell bt-footer-main">
      <div class="bt-footer-blurb">
        <a class="bt-brand" href="#top">
          <img class="bt-brand-logo" src="__LOGO_SRC__" alt="BanTRel Logo" width="38" height="38" onerror="if(!this.dataset.retried){this.dataset.retried='1';this.src='/assets/logo.png';}" />
          <span class="bt-wordmark">Ban<span>TRel</span></span>
        </a>
        <p>Exploring intelligent traffic signal control through reinforcement learning.</p>
      </div>
      <nav class="bt-footer-links" aria-label="Footer navigation">
        <a href="https://bantrel.becore.space/" target="_blank" rel="noopener noreferrer">Simulation</a>
        <a href="https://github.com/Jyotibrat/BanTRel" target="_blank" rel="noopener noreferrer">GitHub</a>
        <a href="https://huggingface.co/BJyotibrat/BanTRel-v1.0.0" target="_blank" rel="noopener noreferrer">Hugging Face</a>
      </nav>
    </div>
    <div class="bt-copyright">
      <div class="bt-shell">BanTRel · AI-powered traffic signal control research</div>
    </div>
  </footer>
</div>
"""

STITCH_HTML = _RAW_STITCH_HTML.replace("__LOGO_SRC__", LOGO_DATA_URI)
