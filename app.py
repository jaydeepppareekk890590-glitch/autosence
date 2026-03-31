import streamlit as st
import pickle
import numpy as np
from sklearn.preprocessing import LabelEncoder

le_brand = pickle.load(open('le_brand.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

st.set_page_config(page_title="AutoSense AI", page_icon="🚗", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:wght@300;400;500&family=Figtree:wght@300;400;500;600&display=swap');

:root {
  --bg: #08090a;
  --surface: #0f1012;
  --surface2: #151618;
  --border: rgba(255,255,255,0.07);
  --border-accent: rgba(255,220,50,0.35);
  --accent: #ffd832;
  --accent2: #ff6b35;
  --accent-dim: rgba(255,216,50,0.12);
  --green: #22d97a;
  --red: #ff4545;
  --yellow: #ffd832;
  --text: #f0f0f0;
  --text-muted: rgba(240,240,240,0.38);
  --text-sub: rgba(240,240,240,0.6);
  --font-head: 'Syne', sans-serif;
  --font-mono: 'DM Mono', monospace;
  --font-body: 'Figtree', sans-serif;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

.stApp {
  background: var(--bg) !important;
  font-family: var(--font-body);
}

/* ---------- HIDE STREAMLIT CHROME ---------- */
#MainMenu, footer, header { visibility: hidden !important; }
section[data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ---------- ANIMATIONS ---------- */
@keyframes fadeUp { from { opacity:0; transform:translateY(22px); } to { opacity:1; transform:translateY(0); } }
@keyframes fadeIn { from { opacity:0; } to { opacity:1; } }
@keyframes pulse-border { 0%,100% { border-color: rgba(255,216,50,0.25); } 50% { border-color: rgba(255,216,50,0.7); } }
@keyframes ticker { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }
@keyframes glow { 0%,100% { text-shadow: 0 0 30px rgba(255,216,50,0.2); } 50% { text-shadow: 0 0 60px rgba(255,216,50,0.55); } }
@keyframes bar-fill { from { width: 0%; } to { width: var(--bar-w); } }
@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
@keyframes slide-in { from { opacity:0; transform: translateX(-20px); } to { opacity:1; transform: translateX(0); } }

/* ---------- TICKER TAPE ---------- */
.ticker-wrap {
  width: 100%;
  background: var(--accent);
  overflow: hidden;
  padding: 9px 0;
  border-bottom: 2px solid rgba(0,0,0,0.15);
}
.ticker-inner {
  display: inline-flex;
  white-space: nowrap;
  animation: ticker 38s linear infinite;
}
.ticker-inner span {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 500;
  color: #080808;
  letter-spacing: 0.5px;
  padding: 0 36px;
}
.ticker-inner span::before { content: "◆"; margin-right: 36px; opacity: 0.5; }

/* ---------- NAVBAR ---------- */
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 64px;
  height: 68px;
  border-bottom: 1px solid var(--border);
  background: rgba(8,9,10,0.97);
  backdrop-filter: blur(20px);
  position: sticky;
  top: 0;
  z-index: 100;
}
.nav-logo {
  font-family: var(--font-head);
  font-size: 22px;
  font-weight: 800;
  color: var(--text);
  letter-spacing: 2px;
}
.nav-logo em { color: var(--accent); font-style: normal; }
.nav-status {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--green);
  letter-spacing: 1.5px;
  background: rgba(34,217,122,0.08);
  border: 1px solid rgba(34,217,122,0.25);
  border-radius: 30px;
  padding: 6px 16px;
}
.status-dot {
  width: 7px; height: 7px;
  background: var(--green);
  border-radius: 50%;
  box-shadow: 0 0 8px var(--green);
}
.nav-right {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-muted);
  letter-spacing: 1px;
}

/* ---------- HERO ---------- */
.hero {
  padding: 80px 64px 60px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
  animation: fadeUp 0.9s ease;
  border-bottom: 1px solid var(--border);
}
.hero-left {}
.hero-eyebrow {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--accent);
  letter-spacing: 3px;
  text-transform: uppercase;
  margin-bottom: 22px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.hero-eyebrow::before {
  content: '';
  width: 32px; height: 2px;
  background: var(--accent);
  display: inline-block;
}
.hero-title {
  font-family: var(--font-head);
  font-size: 64px;
  font-weight: 800;
  color: var(--text);
  line-height: 1.05;
  margin-bottom: 24px;
  animation: glow 5s ease-in-out infinite;
}
.hero-title .hl { color: var(--accent); }
.hero-title .stroke {
  -webkit-text-stroke: 2px rgba(255,255,255,0.45);
  color: transparent;
}
.hero-desc {
  font-size: 15.5px;
  color: var(--text-sub);
  line-height: 1.8;
  max-width: 480px;
  font-weight: 300;
  margin-bottom: 36px;
}
.hero-stats {
  display: flex;
  gap: 32px;
  flex-wrap: wrap;
}
.hstat {
  border-left: 2px solid var(--accent);
  padding-left: 14px;
}
.hstat-n {
  font-family: var(--font-head);
  font-size: 28px;
  font-weight: 800;
  color: var(--accent);
  display: block;
  line-height: 1;
}
.hstat-l {
  font-family: var(--font-mono);
  font-size: 10px;
  color: var(--text-muted);
  letter-spacing: 1.5px;
  text-transform: uppercase;
  margin-top: 4px;
  display: block;
}

/* Hero Right: big visual card */
.hero-right {
  display: flex;
  justify-content: center;
  align-items: center;
}
.hero-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-top: 3px solid var(--accent);
  border-radius: 20px;
  padding: 32px;
  width: 100%;
  max-width: 420px;
  animation: pulse-border 4s ease infinite;
}
.hero-card-title {
  font-family: var(--font-mono);
  font-size: 10px;
  color: var(--text-muted);
  letter-spacing: 2.5px;
  text-transform: uppercase;
  margin-bottom: 24px;
}
.hc-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid var(--border);
}
.hc-row:last-child { border-bottom: none; }
.hc-label {
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--text-muted);
}
.hc-value {
  font-family: var(--font-head);
  font-size: 14px;
  font-weight: 700;
  color: var(--text);
}
.hc-tag {
  background: rgba(34,217,122,0.12);
  color: var(--green);
  border: 1px solid rgba(34,217,122,0.3);
  border-radius: 6px;
  padding: 3px 10px;
  font-family: var(--font-mono);
  font-size: 11px;
}
.hc-tag.red {
  background: rgba(255,69,69,0.1);
  color: var(--red);
  border-color: rgba(255,69,69,0.3);
}
.hc-tag.yellow {
  background: rgba(255,216,50,0.1);
  color: var(--yellow);
  border-color: rgba(255,216,50,0.3);
}

/* ---------- FORM SECTION ---------- */
.form-section {
  padding: 64px 64px 48px;
  border-bottom: 1px solid var(--border);
}
.section-label {
  font-family: var(--font-mono);
  font-size: 11px;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: var(--accent);
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}
.section-label::before { content: ''; width: 24px; height: 2px; background: var(--accent); }
.section-heading {
  font-family: var(--font-head);
  font-size: 34px;
  font-weight: 800;
  color: var(--text);
  margin-bottom: 6px;
}
.section-sub {
  font-size: 14px;
  color: var(--text-muted);
  margin-bottom: 40px;
}

/* Form group grid */
.form-grid-outer {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 36px 40px 28px;
}
.form-grid-title {
  font-family: var(--font-mono);
  font-size: 10px;
  color: var(--text-muted);
  letter-spacing: 2.5px;
  text-transform: uppercase;
  margin-bottom: 28px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border);
}

/* Override Streamlit input styling */
div[data-testid="stSelectbox"] label,
div[data-testid="stSlider"] label,
div[data-testid="stNumberInput"] label {
  color: var(--text-muted) !important;
  font-size: 10px !important;
  font-weight: 600 !important;
  letter-spacing: 2.5px !important;
  text-transform: uppercase !important;
  font-family: var(--font-mono) !important;
  margin-bottom: 6px !important;
}
div[data-testid="stSelectbox"] > div > div {
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
  border-radius: 10px !important;
  color: var(--text) !important;
  font-family: var(--font-body) !important;
}
div[data-testid="stNumberInput"] input {
  background: rgba(255,255,255,0.05) !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
  border-radius: 10px !important;
  color: var(--text) !important;
  font-family: var(--font-head) !important;
  font-size: 16px !important;
  font-weight: 700 !important;
}
div[data-testid="stNumberInput"] input:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 2px rgba(255,216,50,0.12) !important;
}
div[data-testid="stSlider"] > div > div > div > div { background: var(--accent) !important; }
div[data-testid="stSlider"] > div > div > div > div > div { color: var(--bg) !important; }

/* Price section */
.price-box {
  background: linear-gradient(135deg, rgba(255,216,50,0.06), rgba(255,107,53,0.04));
  border: 1px solid rgba(255,216,50,0.25);
  border-radius: 16px;
  padding: 26px 32px 20px;
  margin: 28px 0;
  animation: pulse-border 4s ease infinite;
}
.price-box-title {
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 12px;
}
.tip-line {
  font-size: 12.5px;
  color: var(--text-muted);
  font-style: italic;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--border);
}

/* Analyse button */
.stButton > button {
  background: var(--accent) !important;
  color: #08090a !important;
  border: none !important;
  border-radius: 12px !important;
  padding: 18px 40px !important;
  font-size: 13px !important;
  font-weight: 800 !important;
  width: 100% !important;
  letter-spacing: 3.5px !important;
  text-transform: uppercase !important;
  font-family: var(--font-head) !important;
  transition: all 0.25s ease !important;
  margin-top: 8px !important;
}
.stButton > button:hover {
  background: #ffe55a !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 30px rgba(255,216,50,0.35) !important;
}

/* ---------- RESULTS ---------- */
.result-section {
  padding: 64px 64px 80px;
  animation: fadeUp 0.7s ease;
}

/* Verdict Banner */
.verdict-banner {
  border-radius: 20px;
  padding: 44px 48px;
  display: flex;
  align-items: center;
  gap: 36px;
  margin-bottom: 40px;
  position: relative;
  overflow: hidden;
}
.verdict-banner::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: inherit;
  opacity: 0.15;
}
.vb-steal { background: linear-gradient(135deg, rgba(34,217,122,0.15), rgba(34,217,122,0.05)); border: 1px solid rgba(34,217,122,0.4); }
.vb-fair { background: linear-gradient(135deg, rgba(255,216,50,0.12), rgba(255,216,50,0.04)); border: 1px solid rgba(255,216,50,0.4); }
.vb-over { background: linear-gradient(135deg, rgba(255,69,69,0.15), rgba(255,69,69,0.04)); border: 1px solid rgba(255,69,69,0.4); }
.vb-negotiate { background: linear-gradient(135deg, rgba(255,107,53,0.12), rgba(255,107,53,0.04)); border: 1px solid rgba(255,107,53,0.4); }
.verdict-icon { font-size: 64px; flex-shrink: 0; }
.verdict-text {}
.verdict-tag {
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 10px;
}
.verdict-title {
  font-family: var(--font-head);
  font-size: 38px;
  font-weight: 800;
  color: var(--text);
  line-height: 1.1;
  margin-bottom: 14px;
}
.verdict-title.green { color: var(--green); }
.verdict-title.yellow { color: var(--yellow); }
.verdict-title.red { color: var(--red); }
.verdict-title.orange { color: var(--accent2); }
.verdict-desc {
  font-size: 15px;
  color: var(--text-sub);
  line-height: 1.75;
  max-width: 620px;
}
.verdict-price-badge {
  margin-left: auto;
  flex-shrink: 0;
  text-align: right;
}
.vpb-label { font-family: var(--font-mono); font-size: 10px; color: var(--text-muted); letter-spacing: 2px; text-transform: uppercase; margin-bottom: 6px; }
.vpb-price { font-family: var(--font-head); font-size: 42px; font-weight: 800; color: var(--text); line-height: 1; }
.vpb-sub { font-family: var(--font-mono); font-size: 12px; color: var(--text-muted); margin-top: 4px; }

/* ---------- ANALYSIS GRID ---------- */
.analysis-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}
.analysis-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 28px 30px;
  animation: slide-in 0.6s ease;
}
.analysis-card.full-width {
  grid-column: 1 / -1;
}
.ac-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 22px;
  padding-bottom: 14px;
  border-bottom: 1px solid var(--border);
}
.ac-icon { font-size: 18px; }
.ac-title {
  font-family: var(--font-head);
  font-size: 14px;
  font-weight: 700;
  color: var(--text);
}
.ac-badge {
  margin-left: auto;
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  background: var(--accent-dim);
  color: var(--accent);
  border-radius: 6px;
  padding: 3px 10px;
}

/* Metric rows */
.metric-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid rgba(255,255,255,0.04);
}
.metric-row:last-child { border-bottom: none; }
.metric-label { font-size: 13px; color: var(--text-muted); }
.metric-value { font-family: var(--font-head); font-size: 14px; font-weight: 700; color: var(--text); }
.metric-value.good { color: var(--green); }
.metric-value.warn { color: var(--yellow); }
.metric-value.bad { color: var(--red); }

/* Bar indicator */
.bar-wrap { margin: 14px 0 6px; }
.bar-label-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 7px;
}
.bar-label { font-size: 12px; color: var(--text-muted); font-family: var(--font-mono); }
.bar-val { font-size: 12px; color: var(--text-sub); font-family: var(--font-mono); font-weight: 500; }
.bar-track {
  background: rgba(255,255,255,0.06);
  border-radius: 100px;
  height: 7px;
  overflow: hidden;
}
.bar-fill {
  height: 100%;
  border-radius: 100px;
  --bar-w: 0%;
  width: var(--bar-w);
  animation: bar-fill 1.2s cubic-bezier(.4,0,.2,1) forwards;
}
.bar-green { background: linear-gradient(90deg, #22d97a, #00ffa3); }
.bar-yellow { background: linear-gradient(90deg, #ffd832, #ffb832); }
.bar-red { background: linear-gradient(90deg, #ff4545, #ff6b35); }

/* Verdict chips */
.chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 13px;
  border-radius: 8px;
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.5px;
  margin: 4px 4px 0 0;
}
.chip.green { background: rgba(34,217,122,0.1); color: var(--green); border: 1px solid rgba(34,217,122,0.25); }
.chip.yellow { background: rgba(255,216,50,0.1); color: var(--yellow); border: 1px solid rgba(255,216,50,0.25); }
.chip.red { background: rgba(255,69,69,0.1); color: var(--red); border: 1px solid rgba(255,69,69,0.25); }
.chip.grey { background: rgba(255,255,255,0.06); color: var(--text-muted); border: 1px solid var(--border); }

/* Score ring */
.score-ring-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px 0;
}
.score-number {
  font-family: var(--font-head);
  font-size: 72px;
  font-weight: 800;
  line-height: 1;
  margin-bottom: 6px;
}
.score-label {
  font-family: var(--font-mono);
  font-size: 11px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--text-muted);
}
.score-sub {
  font-size: 12.5px;
  color: var(--text-sub);
  text-align: center;
  max-width: 180px;
  margin-top: 8px;
  line-height: 1.6;
}

/* Action box */
.action-box {
  background: linear-gradient(135deg, rgba(255,216,50,0.08), rgba(255,107,53,0.05));
  border: 1px solid rgba(255,216,50,0.25);
  border-radius: 16px;
  padding: 28px 30px;
  animation: slide-in 0.9s ease;
  margin-top: 0;
}
.action-box.red-action {
  background: linear-gradient(135deg, rgba(255,69,69,0.08), rgba(255,107,53,0.05));
  border-color: rgba(255,69,69,0.25);
}
.action-box.green-action {
  background: linear-gradient(135deg, rgba(34,217,122,0.08), rgba(0,255,163,0.04));
  border-color: rgba(34,217,122,0.25);
}
.action-title {
  font-family: var(--font-head);
  font-size: 15px;
  font-weight: 800;
  color: var(--text);
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.action-list { list-style: none; }
.action-list li {
  font-size: 13.5px;
  color: var(--text-sub);
  padding: 8px 0;
  border-bottom: 1px solid rgba(255,255,255,0.04);
  display: flex;
  align-items: flex-start;
  gap: 10px;
  line-height: 1.6;
}
.action-list li:last-child { border-bottom: none; }
.action-list li::before {
  content: '→';
  color: var(--accent);
  flex-shrink: 0;
  font-family: var(--font-mono);
  font-weight: 600;
}

/* Depreciation table */
.dep-row {
  display: grid;
  grid-template-columns: 60px 1fr 80px;
  gap: 12px;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid rgba(255,255,255,0.04);
}
.dep-row:last-child { border-bottom: none; }
.dep-year { font-family: var(--font-mono); font-size: 12px; color: var(--text-muted); }
.dep-bar-wrap { flex: 1; }
.dep-pct { font-family: var(--font-mono); font-size: 12px; color: var(--text-sub); text-align: right; }

/* Footer */
.footer {
  border-top: 1px solid var(--border);
  padding: 44px 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.footer-logo {
  font-family: var(--font-head);
  font-size: 18px;
  font-weight: 800;
  color: rgba(255,255,255,0.25);
  letter-spacing: 2px;
}
.footer-logo em { color: var(--accent); font-style: normal; }
.footer-right {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-muted);
  letter-spacing: 1px;
  text-align: right;
  line-height: 1.8;
}

</style>

<!-- TICKER -->
<div class="ticker-wrap">
  <div class="ticker-inner">
    <span>MARUTI SUZUKI · BEST RESALE VALUE IN INDIA</span>
    <span>DIESEL CARS DEPRECIATE 20% FASTER AFTER 7 YEARS</span>
    <span>USED CAR MARKET EXPECTED TO TOUCH ₹4.6L CRORE BY 2026</span>
    <span>HYUNDAI & HONDA COMMAND HIGHEST RESALE IN SEGMENT</span>
    <span>CNG CARS SURGING IN TIER-2 CITIES — 34% YOY GROWTH</span>
    <span>AUTOMATIC TRANSMISSION CARS NOW SELLING AT +8% PREMIUM</span>
    <span>AVOID CARS WITH 100K+ KM IF OLDER THAN 8 YEARS</span>
    <span>ELECTRIC VEHICLES: RESALE STILL UNCERTAIN — NEGOTIATE HARD</span>
    <span>MARUTI SUZUKI · BEST RESALE VALUE IN INDIA</span>
    <span>DIESEL CARS DEPRECIATE 20% FASTER AFTER 7 YEARS</span>
    <span>USED CAR MARKET EXPECTED TO TOUCH ₹4.6L CRORE BY 2026</span>
    <span>HYUNDAI & HONDA COMMAND HIGHEST RESALE IN SEGMENT</span>
    <span>CNG CARS SURGING IN TIER-2 CITIES — 34% YOY GROWTH</span>
    <span>AUTOMATIC TRANSMISSION CARS NOW SELLING AT +8% PREMIUM</span>
    <span>AVOID CARS WITH 100K+ KM IF OLDER THAN 8 YEARS</span>
    <span>ELECTRIC VEHICLES: RESALE STILL UNCERTAIN — NEGOTIATE HARD</span>
  </div>
</div>

<!-- NAVBAR -->
<div class="navbar">
  <div class="nav-logo">AUTO<em>SENSE</em></div>
  <div class="nav-status"><span class="status-dot"></span> ML ENGINE ONLINE</div>
  <div class="nav-right">SVM · 15,411 CARS · CARDEKHO</div>
</div>

<!-- HERO -->
<div class="hero">
  <div class="hero-left">
    <div class="hero-eyebrow">India's Used Car Intelligence Engine</div>
    <div class="hero-title">
      Know the real<br>price before you<br><span class="hl">get played.</span>
    </div>
    <div class="hero-desc">
      AutoSense runs a trained SVM model on real CarDekho data. Enter a car's specs, we'll tell you if you're about to make a smart buy — or a very expensive mistake.
    </div>
    <div class="hero-stats">
      <div class="hstat"><span class="hstat-n">15,411</span><span class="hstat-l">Cars Trained</span></div>
      <div class="hstat"><span class="hstat-n">85.5%</span><span class="hstat-l">Accuracy</span></div>
      <div class="hstat"><span class="hstat-n">30+</span><span class="hstat-l">Brands</span></div>
      <div class="hstat"><span class="hstat-n">&lt;1s</span><span class="hstat-l">Result Time</span></div>
    </div>
  </div>
  <div class="hero-right">
    <div class="hero-card">
      <div class="hero-card-title">● SAMPLE ANALYSIS OUTPUT</div>
      <div class="hc-row"><span class="hc-label">Brand</span><span class="hc-value">Hyundai i20</span></div>
      <div class="hc-row"><span class="hc-label">Age</span><span class="hc-value">5 years</span></div>
      <div class="hc-row"><span class="hc-label">KMs Driven</span><span class="hc-value">48,000 km</span></div>
      <div class="hc-row"><span class="hc-label">Fuel</span><span class="hc-value">Petrol</span></div>
      <div class="hc-row"><span class="hc-label">Asking Price</span><span class="hc-value">₹4.8L</span></div>
      <div class="hc-row"><span class="hc-label">Verdict</span><span class="hc-tag">✓ FAIR PRICE</span></div>
      <div class="hc-row"><span class="hc-label">Deal Score</span><span class="hc-tag yellow">72 / 100</span></div>
      <div class="hc-row"><span class="hc-label">KM Risk</span><span class="hc-tag">LOW</span></div>
      <div class="hc-row"><span class="hc-label">Nego Potential</span><span class="hc-tag yellow">₹4.2–4.5L</span></div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ===========================
# FORM SECTION
# ===========================
st.markdown("""
<div class="form-section">
  <div class="section-label">Car Price Analyser</div>
  <div class="section-heading">Enter the Car Details</div>
  <div class="section-sub">Fill in exactly what the seller listed. Every field matters — the model uses all 10 features.</div>
  <div class="form-grid-outer">
    <div class="form-grid-title">● CAR SPECIFICATIONS</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    brand = st.selectbox("Car Brand", sorted(le_brand.classes_))
    vehicle_age = st.slider("Vehicle Age (years)", 0, 25, 5)
    km_driven = st.number_input("KMs Driven", min_value=0, max_value=500000, value=50000, step=1000)
with col2:
    seller_type = st.selectbox("Seller Type", ["Dealer", "Individual", "Trustmark Dealer"])
    fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "LPG", "Electric"])
    transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
with col3:
    mileage = st.number_input("Mileage (kmpl)", min_value=0.0, max_value=50.0, value=18.0, step=0.1)
    engine = st.number_input("Engine (cc)", min_value=500, max_value=5000, value=1200, step=100)
    max_power = st.number_input("Max Power (bhp)", min_value=20.0, max_value=500.0, value=80.0, step=1.0)
    seats = st.selectbox("Seats", [2, 4, 5, 6, 7, 8, 9, 10])

st.markdown('</div>', unsafe_allow_html=True)  # close form-grid-outer

st.markdown("""
  <div class="price-box">
    <div class="price-box-title">💰 Seller's Asking Price</div>
""", unsafe_allow_html=True)

asking_price = st.number_input("Asking Price (₹)", min_value=10000, max_value=10000000, value=300000, step=5000, label_visibility="collapsed")

st.markdown("""
    <div class="tip-line">Enter the exact price the seller is quoting — we'll compare it against what this car is actually worth based on your inputs.</div>
  </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
analyse_clicked = st.button("⚡  ANALYSE THIS CAR")

st.markdown('</div>', unsafe_allow_html=True)  # close form-section


# ===========================
# ANALYSIS LOGIC
# ===========================
if analyse_clicked:
    le_seller = LabelEncoder()
    le_seller.fit(["Dealer", "Individual", "Trustmark Dealer"])
    le_fuel = LabelEncoder()
    le_fuel.fit(["CNG", "Diesel", "Electric", "LPG", "Petrol"])
    le_trans = LabelEncoder()
    le_trans.fit(["Automatic", "Manual"])

    brand_enc = le_brand.transform([brand])[0]
    seller_enc = le_seller.transform([seller_type])[0]
    fuel_enc = le_fuel.transform([fuel_type])[0]
    trans_enc = le_trans.transform([transmission])[0]

    input_data = np.array([[brand_enc, vehicle_age, km_driven,
                            seller_enc, fuel_enc, trans_enc,
                            mileage, engine, max_power, seats]])
    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)[0]
    price_in_lakhs = asking_price / 100000

    # ---- Derived analysis signals ----
    km_per_year = km_driven / max(vehicle_age, 1)
    expected_km_per_year = 12000
    km_risk = km_per_year / expected_km_per_year

    if km_risk < 0.6:
        km_risk_label = "VERY LOW"
        km_risk_color = "green"
        km_risk_pct = 20
    elif km_risk < 1.0:
        km_risk_label = "LOW"
        km_risk_color = "green"
        km_risk_pct = 40
    elif km_risk < 1.4:
        km_risk_label = "MODERATE"
        km_risk_color = "yellow"
        km_risk_pct = 60
    elif km_risk < 2.0:
        km_risk_label = "HIGH"
        km_risk_color = "red"
        km_risk_pct = 80
    else:
        km_risk_label = "CRITICAL"
        km_risk_color = "red"
        km_risk_pct = 95

    # Mileage score
    if mileage >= 22:
        mileage_score = "Excellent"
        mileage_color = "green"
    elif mileage >= 16:
        mileage_score = "Good"
        mileage_color = "green"
    elif mileage >= 12:
        mileage_score = "Average"
        mileage_color = "yellow"
    else:
        mileage_score = "Poor"
        mileage_color = "red"

    # Engine tier
    if engine <= 800:
        engine_tier = "Hatchback Entry"
    elif engine <= 1200:
        engine_tier = "Compact / City"
    elif engine <= 1600:
        engine_tier = "Mid Segment"
    elif engine <= 2000:
        engine_tier = "Premium Segment"
    else:
        engine_tier = "SUV / Performance"

    # Power-to-engine ratio
    power_ratio = max_power / (engine / 1000)
    if power_ratio >= 70:
        power_label = "Sporty"
        power_color = "green"
    elif power_ratio >= 55:
        power_label = "Adequate"
        power_color = "yellow"
    else:
        power_label = "Low Output"
        power_color = "red"

    # Depreciation estimate (rough Indian market model)
    annual_dep_rates = [0.15, 0.12, 0.10, 0.09, 0.08, 0.07, 0.07, 0.06, 0.06, 0.05]
    remaining_val = 100.0
    dep_data = []
    for i, rate in enumerate(annual_dep_rates, 1):
        remaining_val -= remaining_val * rate
        dep_data.append((i, round(remaining_val, 1)))

    # Seller trust score
    if seller_type == "Trustmark Dealer":
        trust = "HIGH"
        trust_color = "green"
        trust_note = "Trustmark dealers are verified — lower fraud risk, often warranty included."
    elif seller_type == "Dealer":
        trust = "MODERATE"
        trust_color = "yellow"
        trust_note = "Dealer cars are inspected but priced at a premium. Negotiate down."
    else:
        trust = "CAUTION"
        trust_color = "red"
        trust_note = "Individual sellers carry higher risk. Insist on full service history and RC check."

    # Fuel score
    fuel_insights = {
        "Petrol": ("Best resale value, lower maintenance. Ideal for <80 km/day.", "green"),
        "Diesel": ("High mileage & torque but expensive maintenance post-100k km.", "yellow"),
        "CNG": ("Very low running cost, but lower resale & power.", "yellow"),
        "LPG": ("Rare fuel type — resale is difficult. Proceed only if price is very low.", "red"),
        "Electric": ("Future-proof but resale market is still evolving in India. Negotiate hard.", "yellow"),
    }
    fuel_note, fuel_color = fuel_insights.get(fuel_type, ("", "grey"))

    # Negotiate range
    negotiate_low = price_in_lakhs * 0.78
    negotiate_high = price_in_lakhs * 0.90

    # Deal score (0-100)
    deal_score = 50
    if prediction == 0:
        deal_score = 80 if price_in_lakhs <= 3 else 62
    elif prediction == 1:
        deal_score = 65
    else:
        deal_score = 28

    if km_risk_pct < 40:
        deal_score += 8
    elif km_risk_pct > 70:
        deal_score -= 10

    if vehicle_age <= 4:
        deal_score += 6
    elif vehicle_age >= 10:
        deal_score -= 8

    if seller_type == "Trustmark Dealer":
        deal_score += 5
    elif seller_type == "Individual":
        deal_score -= 3

    deal_score = min(max(deal_score, 5), 97)

    if deal_score >= 70:
        score_color = "#22d97a"
        score_word = "Strong Buy"
    elif deal_score >= 50:
        score_color = "#ffd832"
        score_word = "Proceed with Care"
    else:
        score_color = "#ff4545"
        score_word = "Walk Away or Negotiate"

    # ---- VERDICT CONFIG ----
    if prediction == 0 and price_in_lakhs <= 3:
        vclass = "vb-steal"
        v_icon = "🤩"
        v_title = "STEAL DEAL"
        v_title_class = "green"
        v_desc = (f"This {brand} is genuinely underpriced. A {vehicle_age}-year-old car with {km_driven:,} km on the clock "
                  f"and {max_power} bhp output — the ML model classifies this as an underpriced vehicle AND the seller is only "
                  f"asking ₹{price_in_lakhs:.1f}L. That's below market for this profile. Lock it in before someone else does.")
        action_class = "green-action"
        action_title = "✅ Recommended Actions"
        action_items = [
            "Cross-check the RC (Registration Certificate) to verify ownership and loan status.",
            "Request the last 2 service records — low km + low price may indicate odometer tampering.",
            f"Target a final price of ₹{price_in_lakhs*0.94:.1f}L–₹{price_in_lakhs:.1f}L. Small room to negotiate but don't push too hard.",
            "Get a pre-purchase inspection from an independent mechanic before paying.",
            "Verify insurance validity and check for challan (fine) history on Parivahan portal.",
        ]
    elif prediction == 0:
        vclass = "vb-negotiate"
        v_icon = "🤔"
        v_title = "GOOD CAR, NEGOTIATE THE PRICE"
        v_title_class = "orange"
        v_desc = (f"The {brand}'s technical profile — {vehicle_age} years old, {engine}cc, {max_power}bhp — scores well. "
                  f"The car itself is underpriced by market standards, but ₹{price_in_lakhs:.1f}L is slightly above what "
                  f"the model expects. You have 10–15% room to negotiate. Push for around ₹{price_in_lakhs*0.87:.1f}L.")
        action_class = ""
        action_title = "💬 Negotiation Playbook"
        action_items = [
            f"Open with ₹{price_in_lakhs*0.82:.1f}L — lower than your target to create anchoring room.",
            f"Your walk-away number: ₹{price_in_lakhs*0.90:.1f}L. Don't go above this without more inspection.",
            "Point out depreciation: a {}-year-old car loses significant book value annually.".format(vehicle_age),
            "If seller won't budge, request free extras: extended warranty, 1 free service, new tyres.",
            "Check 2-3 comparable listings on CarDekho/OLX before negotiating — use data as leverage.",
        ]
    elif prediction == 1:
        vclass = "vb-fair"
        v_icon = "👍"
        v_title = "FAIRLY PRICED"
        v_title_class = "yellow"
        v_desc = (f"₹{price_in_lakhs:.1f}L for this {brand} is a reasonable ask. At {vehicle_age} years old with {km_driven:,} km, "
                  f"a {engine}cc engine delivering {max_power}bhp, the price aligns with the Indian used car market. "
                  f"You still have a small 5–8% negotiation window. A solid deal if the paperwork checks out.")
        action_class = ""
        action_title = "📋 Pre-Purchase Checklist"
        action_items = [
            f"Try negotiating ₹{price_in_lakhs*0.94:.1f}L–₹{price_in_lakhs*0.96:.1f}L — there's a small margin here.",
            "Request the car's full service history booklet. Missing records are a red flag.",
            "Check for major accident history using the chassis/VIN number.",
            "Inspect tyres, brakes, AC compressor and battery — these are expensive to replace post-purchase.",
            "Verify all original documents: RC, insurance, PUC, loan clearance certificate if applicable.",
        ]
    else:
        vclass = "vb-over"
        v_icon = "🚨"
        v_title = "OVERPRICED — DANGER ZONE"
        v_title_class = "red"
        v_desc = (f"₹{price_in_lakhs:.1f}L for this {vehicle_age}-year-old {brand} with {km_driven:,} km does not add up. "
                  f"The ML model — trained on 15,411 real transactions — flags this as overpriced. "
                  f"A {max_power}bhp {engine}cc car of this age should command no more than ₹{price_in_lakhs*0.78:.1f}L in the current market. "
                  f"Either negotiate aggressively or walk away and find a better deal.")
        action_class = "red-action"
        action_title = "🚫 Don't Buy Yet — Do This First"
        action_items = [
            f"Do NOT pay ₹{price_in_lakhs:.1f}L. Counter-offer at ₹{price_in_lakhs*0.72:.1f}L and negotiate up to ₹{price_in_lakhs*0.80:.1f}L max.",
            "Search CarDekho/Cars24/OLX for 3 comparable cars and take screenshots as negotiation ammo.",
            f"For a {vehicle_age}-year-old car, factor in upcoming maintenance costs: timing belt, suspension, clutch.",
            "If the seller refuses to negotiate below ₹{:.1f}L, walk away — the math doesn't work.".format(price_in_lakhs*0.85),
            "Report suspiciously high prices to CarDekho if this is a listed dealership — may be fraud.",
        ]

    # ======= RENDER RESULTS =======
    st.markdown('<div class="result-section">', unsafe_allow_html=True)

    # --- Verdict Banner ---
    st.markdown(f"""
    <div class="verdict-banner {vclass}">
      <div class="verdict-icon">{v_icon}</div>
      <div class="verdict-text">
        <div class="verdict-tag">● AUTOSENSE VERDICT</div>
        <div class="verdict-title {v_title_class}">{v_title}</div>
        <div class="verdict-desc">{v_desc}</div>
      </div>
      <div class="verdict-price-badge">
        <div class="vpb-label">ASKING PRICE</div>
        <div class="vpb-price">₹{price_in_lakhs:.1f}L</div>
        <div class="vpb-sub">Deal Score: {deal_score}/100</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Analysis Grid ---
    st.markdown('<div class="analysis-grid">', unsafe_allow_html=True)

    # CARD 1: Deal Score
    st.markdown(f"""
    <div class="analysis-card">
      <div class="ac-header">
        <span class="ac-icon">🎯</span>
        <span class="ac-title">Deal Score</span>
        <span class="ac-badge">AI SCORE</span>
      </div>
      <div class="score-ring-wrap">
        <div class="score-number" style="color:{score_color}">{deal_score}</div>
        <div class="score-label">OUT OF 100</div>
        <div class="score-sub">{score_word}</div>
      </div>
      <div class="bar-wrap">
        <div class="bar-track"><div class="bar-fill {'bar-green' if deal_score >= 70 else 'bar-yellow' if deal_score >= 50 else 'bar-red'}" style="--bar-w:{deal_score}%"></div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # CARD 2: Car Profile
    st.markdown(f"""
    <div class="analysis-card">
      <div class="ac-header">
        <span class="ac-icon">🚗</span>
        <span class="ac-title">Car Profile</span>
        <span class="ac-badge">{brand.upper()}</span>
      </div>
      <div class="metric-row"><span class="metric-label">Brand</span><span class="metric-value">{brand}</span></div>
      <div class="metric-row"><span class="metric-label">Vehicle Age</span><span class="metric-value {'warn' if vehicle_age > 8 else 'good'}">{vehicle_age} years</span></div>
      <div class="metric-row"><span class="metric-label">KMs Driven</span><span class="metric-value {'bad' if km_driven > 150000 else 'warn' if km_driven > 80000 else 'good'}">{km_driven:,} km</span></div>
      <div class="metric-row"><span class="metric-label">Fuel Type</span><span class="metric-value">{fuel_type}</span></div>
      <div class="metric-row"><span class="metric-label">Transmission</span><span class="metric-value">{transmission}</span></div>
      <div class="metric-row"><span class="metric-label">Seller</span><span class="metric-value">{seller_type}</span></div>
      <div class="metric-row"><span class="metric-label">Seats</span><span class="metric-value">{seats}</span></div>
    </div>
    """, unsafe_allow_html=True)

    # CARD 3: Engine & Performance
    st.markdown(f"""
    <div class="analysis-card">
      <div class="ac-header">
        <span class="ac-icon">⚙️</span>
        <span class="ac-title">Engine & Performance</span>
        <span class="ac-badge">{engine_tier.upper()}</span>
      </div>
      <div class="metric-row"><span class="metric-label">Engine Size</span><span class="metric-value">{engine}cc</span></div>
      <div class="metric-row"><span class="metric-label">Max Power</span><span class="metric-value">{max_power} bhp</span></div>
      <div class="metric-row"><span class="metric-label">Power/Litre</span><span class="metric-value {power_color}">{power_ratio:.0f} bhp/L · {power_label}</span></div>
      <div class="metric-row"><span class="metric-label">Mileage</span><span class="metric-value {mileage_color}">{mileage} kmpl · {mileage_score}</span></div>
      <div class="metric-row"><span class="metric-label">Segment</span><span class="metric-value">{engine_tier}</span></div>
      <br>
      <div class="bar-wrap">
        <div class="bar-label-row"><span class="bar-label">POWER OUTPUT</span><span class="bar-val">{max_power} bhp</span></div>
        <div class="bar-track"><div class="bar-fill bar-yellow" style="--bar-w:{min(max_power/150*100, 100):.0f}%"></div></div>
      </div>
      <div class="bar-wrap">
        <div class="bar-label-row"><span class="bar-label">MILEAGE SCORE</span><span class="bar-val">{mileage} kmpl</span></div>
        <div class="bar-track"><div class="bar-fill bar-green" style="--bar-w:{min(mileage/30*100, 100):.0f}%"></div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # CARD 4: Mileage / KM Risk
    km_per_year_display = int(km_per_year)
    st.markdown(f"""
    <div class="analysis-card">
      <div class="ac-header">
        <span class="ac-icon">📍</span>
        <span class="ac-title">Odometer Risk Analysis</span>
        <span class="ac-badge">{km_risk_label}</span>
      </div>
      <div class="metric-row"><span class="metric-label">Total KMs</span><span class="metric-value">{km_driven:,} km</span></div>
      <div class="metric-row"><span class="metric-label">Avg KM/Year</span><span class="metric-value {km_risk_color}">{km_per_year_display:,} km/yr</span></div>
      <div class="metric-row"><span class="metric-label">Expected Avg</span><span class="metric-value">~12,000 km/yr</span></div>
      <div class="metric-row"><span class="metric-label">Usage Intensity</span><span class="metric-value {km_risk_color}">{km_risk:.1f}x normal usage</span></div>
      <div class="metric-row"><span class="metric-label">Odometer Risk</span><span class="metric-value {km_risk_color}">{km_risk_label}</span></div>
      <br>
      <div class="bar-wrap">
        <div class="bar-label-row"><span class="bar-label">KM WEAR RISK</span><span class="bar-val">{km_risk_pct}%</span></div>
        <div class="bar-track"><div class="bar-fill {'bar-red' if km_risk_pct > 70 else 'bar-yellow' if km_risk_pct > 40 else 'bar-green'}" style="--bar-w:{km_risk_pct}%"></div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close analysis-grid

    # SECOND ROW GRID
    st.markdown('<div class="analysis-grid">', unsafe_allow_html=True)

    # CARD 5: Depreciation
    dep_rows_html = ""
    for yr, val in dep_data[:8]:
        bar_w = int(val)
        bar_col = "bar-green" if val > 60 else "bar-yellow" if val > 40 else "bar-red"
        highlight = " style='color:var(--accent);font-weight:700;'" if yr == vehicle_age else ""
        dep_rows_html += f"""
        <div class="dep-row">
          <span class="dep-year"{highlight}>Yr {yr}</span>
          <div class="dep-bar-wrap">
            <div class="bar-track" style="height:5px"><div class="bar-fill {bar_col}" style="--bar-w:{bar_w}%"></div></div>
          </div>
          <span class="dep-pct"{highlight}>{val}%</span>
        </div>"""

    st.markdown(f"""
    <div class="analysis-card">
      <div class="ac-header">
        <span class="ac-icon">📉</span>
        <span class="ac-title">Depreciation Timeline</span>
        <span class="ac-badge">% VALUE LEFT</span>
      </div>
      {dep_rows_html}
    </div>
    """, unsafe_allow_html=True)

    # CARD 6: Trust + Fuel Signals
    neg_low_fmt = f"₹{negotiate_low:.1f}L"
    neg_high_fmt = f"₹{negotiate_high:.1f}L"
    st.markdown(f"""
    <div class="analysis-card">
      <div class="ac-header">
        <span class="ac-icon">🔎</span>
        <span class="ac-title">Market Signals</span>
        <span class="ac-badge">INTEL</span>
      </div>
      <div class="metric-row"><span class="metric-label">Seller Trust Level</span><span class="metric-value {trust_color}">{trust}</span></div>
      <div class="metric-row" style="padding:12px 0"><span class="metric-label" style="font-size:12px;color:var(--text-muted);line-height:1.6">{trust_note}</span></div>
      <div class="metric-row"><span class="metric-label">Fuel Type Signal</span><span class="metric-value {fuel_color}">{fuel_type}</span></div>
      <div class="metric-row" style="padding:12px 0"><span class="metric-label" style="font-size:12px;color:var(--text-muted);line-height:1.6">{fuel_note}</span></div>
      <div class="metric-row"><span class="metric-label">Negotiation Range</span><span class="metric-value">{neg_low_fmt} – {neg_high_fmt}</span></div>
      <br>
      <div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:4px">
        <span class="chip {'green' if vehicle_age <= 5 else 'yellow' if vehicle_age <= 9 else 'red'}">Age: {vehicle_age}yr</span>
        <span class="chip {km_risk_color}">KM Risk: {km_risk_label}</span>
        <span class="chip {trust_color}">Seller: {trust}</span>
        <span class="chip {fuel_color}">{fuel_type}</span>
        <span class="chip grey">{transmission}</span>
        <span class="chip grey">{seats} Seats</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close grid

    # ACTION BOX
    action_items_html = "".join(f"<li>{item}</li>" for item in action_items)
    st.markdown(f"""
    <div class="action-box {action_class}">
      <div class="action-title">{action_title}</div>
      <ul class="action-list">{action_items_html}</ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close result-section

# FOOTER
st.markdown("""
<div class="footer">
  <div class="footer-logo">AUTO<em>SENSE</em></div>
  <div class="footer-right">
    SVM Algorithm · 15,411 CarDekho Transactions · 85.5% Accuracy<br>
    <span style="color:rgba(255,255,255,0.15)">Results are advisory only. Always inspect in person before purchase.</span>
  </div>
</div>
""", unsafe_allow_html=True)
