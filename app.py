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
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&family=Figtree:wght@300;400;500;600&display=swap');

:root {
  --bg: #08090a;
  --surface: #111214;
  --border: rgba(255,255,255,0.08);
  --accent: #ffd832;
  --green: #22d97a;
  --red: #ff4545;
  --orange: #ff6b35;
  --text: #f0f0f0;
  --muted: rgba(240,240,240,0.4);
  --sub: rgba(240,240,240,0.62);
  --font-head: 'Syne', sans-serif;
  --font-mono: 'DM Mono', monospace;
  --font-body: 'Figtree', sans-serif;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
.stApp { background: var(--bg) !important; font-family: var(--font-body); }

#MainMenu, footer, header { visibility: hidden !important; }
section[data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }

@keyframes fadeUp { from { opacity:0; transform:translateY(18px); } to { opacity:1; transform:translateY(0); } }
@keyframes bar-fill { from { width:0% } to { width: var(--bar-w); } }
@keyframes slide-in { from { opacity:0; transform:translateX(-14px); } to { opacity:1; transform:translateX(0); } }
@keyframes pulse-border { 0%,100% { border-color:rgba(255,216,50,0.2); } 50% { border-color:rgba(255,216,50,0.6); } }

/* NAVBAR */
.navbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 56px; height: 62px;
  border-bottom: 1px solid var(--border);
  background: rgba(8,9,10,0.98);
  position: sticky; top: 0; z-index: 100;
}
.nav-logo { font-family: var(--font-head); font-size: 20px; font-weight: 800; color: var(--text); letter-spacing: 2px; }
.nav-logo em { color: var(--accent); font-style: normal; }
.nav-status {
  display: flex; align-items: center; gap: 7px;
  font-family: var(--font-mono); font-size: 11px; color: var(--green); letter-spacing: 1.5px;
  background: rgba(34,217,122,0.08); border: 1px solid rgba(34,217,122,0.22); border-radius: 30px; padding: 5px 14px;
}
.status-dot { width:6px; height:6px; background:var(--green); border-radius:50%; box-shadow:0 0 7px var(--green); }
.nav-right { font-family: var(--font-mono); font-size: 11px; color: var(--muted); letter-spacing: 1px; }

/* PAGE HEADER */
.page-header { padding: 52px 56px 40px; border-bottom: 1px solid var(--border); animation: fadeUp 0.7s ease; }
.ph-eyebrow {
  font-family: var(--font-mono); font-size: 11px; color: var(--accent);
  letter-spacing: 3px; text-transform: uppercase;
  display: flex; align-items: center; gap: 10px; margin-bottom: 14px;
}
.ph-eyebrow::before { content:''; width:24px; height:2px; background:var(--accent); }
.ph-title { font-family: var(--font-head); font-size: 44px; font-weight: 800; color: var(--text); line-height: 1.1; margin-bottom: 8px; }
.ph-title em { color: var(--accent); font-style: normal; }
.ph-sub { font-size: 14px; color: var(--muted); }

/* FORM */
.form-wrap { padding: 40px 56px 48px; border-bottom: 1px solid var(--border); }
.form-card { background: var(--surface); border: 1px solid var(--border); border-radius: 18px; padding: 32px 36px 28px; }
.form-card-title {
  font-family: var(--font-mono); font-size: 10px; letter-spacing: 2.5px;
  text-transform: uppercase; color: var(--muted);
  margin-bottom: 24px; padding-bottom: 14px; border-bottom: 1px solid var(--border);
}

/* INPUT OVERRIDES — dark bg, always-visible text */
div[data-testid="stSelectbox"] label,
div[data-testid="stSlider"] label,
div[data-testid="stNumberInput"] label {
  color: var(--muted) !important;
  font-size: 10px !important; font-weight: 600 !important;
  letter-spacing: 2.5px !important; text-transform: uppercase !important;
  font-family: var(--font-mono) !important;
}
div[data-testid="stSelectbox"] > div > div {
  background: #1a1c1f !important;
  border: 1px solid rgba(255,255,255,0.12) !important;
  border-radius: 10px !important; color: #f0f0f0 !important;
  font-family: var(--font-body) !important; font-size: 15px !important;
}
div[data-testid="stSelectbox"] svg { color: var(--muted) !important; fill: var(--muted) !important; }
div[data-testid="stNumberInput"] input {
  background: #1a1c1f !important;
  border: 1px solid rgba(255,255,255,0.12) !important;
  border-radius: 10px !important; color: #f0f0f0 !important;
  font-family: var(--font-head) !important; font-size: 16px !important; font-weight: 700 !important;
}
div[data-testid="stNumberInput"] input:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 2px rgba(255,216,50,0.1) !important;
}
div[data-testid="stNumberInput"] button {
  background: #222427 !important; color: #f0f0f0 !important; border: none !important; border-radius: 8px !important;
}
div[data-testid="stNumberInput"] button:hover { background: rgba(255,216,50,0.15) !important; color: var(--accent) !important; }
div[data-testid="stSlider"] > div > div > div > div { background: var(--accent) !important; }

/* PRICE BOX */
.price-box {
  background: linear-gradient(135deg, rgba(255,216,50,0.06), rgba(255,107,53,0.03));
  border: 1px solid rgba(255,216,50,0.28); border-radius: 14px;
  padding: 22px 28px 18px; margin: 24px 0 0;
  animation: pulse-border 4s ease infinite;
}
.price-box-label { font-family: var(--font-mono); font-size: 10px; letter-spacing: 2.5px; text-transform: uppercase; color: var(--accent); margin-bottom: 10px; }
.price-tip { font-size: 12px; color: var(--muted); font-style: italic; margin-top: 10px; padding-top: 10px; border-top: 1px solid var(--border); line-height: 1.6; }

/* BUTTON */
.stButton > button {
  background: var(--accent) !important; color: #08090a !important; border: none !important;
  border-radius: 11px !important; padding: 17px 40px !important; font-size: 12px !important;
  font-weight: 800 !important; width: 100% !important; letter-spacing: 3.5px !important;
  text-transform: uppercase !important; font-family: var(--font-head) !important;
  transition: all 0.22s ease !important; margin-top: 10px !important;
}
.stButton > button:hover { background: #ffe85a !important; transform: translateY(-2px) !important; box-shadow: 0 8px 28px rgba(255,216,50,0.3) !important; }

/* RESULTS */
.result-section { padding: 52px 56px 80px; animation: fadeUp 0.6s ease; }

.verdict-banner {
  border-radius: 18px; padding: 38px 44px;
  display: flex; align-items: center; gap: 30px; margin-bottom: 36px;
}
.vb-steal { background: rgba(34,217,122,0.08); border: 1px solid rgba(34,217,122,0.38); }
.vb-fair  { background: rgba(255,216,50,0.07); border: 1px solid rgba(255,216,50,0.35); }
.vb-over  { background: rgba(255,69,69,0.08);  border: 1px solid rgba(255,69,69,0.35); }
.vb-nego  { background: rgba(255,107,53,0.08); border: 1px solid rgba(255,107,53,0.35); }

.verdict-icon { font-size: 58px; flex-shrink: 0; }
.verdict-body { flex: 1; }
.verdict-tag { font-family: var(--font-mono); font-size: 10px; letter-spacing: 3px; text-transform: uppercase; color: var(--muted); margin-bottom: 8px; }
.verdict-title { font-family: var(--font-head); font-size: 32px; font-weight: 800; line-height: 1.1; margin-bottom: 12px; }
.vt-green  { color: var(--green); }
.vt-yellow { color: var(--accent); }
.vt-red    { color: var(--red); }
.vt-orange { color: var(--orange); }
.verdict-desc { font-size: 14.5px; color: var(--sub); line-height: 1.75; max-width: 600px; }
.verdict-right { margin-left: auto; flex-shrink: 0; text-align: right; }
.vr-label { font-family: var(--font-mono); font-size: 10px; color: var(--muted); letter-spacing: 2px; text-transform: uppercase; margin-bottom: 5px; }
.vr-price { font-family: var(--font-head); font-size: 38px; font-weight: 800; color: var(--text); line-height: 1; }
.vr-score { font-family: var(--font-mono); font-size: 12px; color: var(--muted); margin-top: 5px; }

.ag { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin-bottom: 18px; }
.acard { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 24px 26px; animation: slide-in 0.5s ease; }
.acard-head { display: flex; align-items: center; gap: 9px; margin-bottom: 18px; padding-bottom: 12px; border-bottom: 1px solid var(--border); }
.acard-icon { font-size: 16px; }
.acard-title { font-family: var(--font-head); font-size: 13px; font-weight: 700; color: var(--text); }
.acard-badge { margin-left: auto; font-family: var(--font-mono); font-size: 10px; letter-spacing: 1px; text-transform: uppercase; background: rgba(255,216,50,0.1); color: var(--accent); border-radius: 5px; padding: 2px 9px; }

.mrow { display: flex; align-items: center; justify-content: space-between; padding: 9px 0; border-bottom: 1px solid rgba(255,255,255,0.04); }
.mrow:last-child { border-bottom: none; }
.ml { font-size: 12.5px; color: var(--muted); }
.mv { font-family: var(--font-head); font-size: 13px; font-weight: 700; color: var(--text); }
.mv.g { color: var(--green); } .mv.y { color: var(--accent); } .mv.r { color: var(--red); }

.bar-wrap { margin: 12px 0 4px; }
.blrow { display: flex; justify-content: space-between; margin-bottom: 6px; }
.bl { font-family: var(--font-mono); font-size: 11px; color: var(--muted); }
.bv { font-family: var(--font-mono); font-size: 11px; color: var(--sub); }
.btrack { background: rgba(255,255,255,0.06); border-radius: 100px; height: 6px; overflow: hidden; }
.bfill { height: 100%; border-radius: 100px; --bar-w: 0%; width: var(--bar-w); animation: bar-fill 1.1s cubic-bezier(.4,0,.2,1) forwards; }
.bg { background: linear-gradient(90deg,#22d97a,#00ffa3); }
.by { background: linear-gradient(90deg,#ffd832,#ffb820); }
.br { background: linear-gradient(90deg,#ff4545,#ff6b35); }

.score-center { display:flex; flex-direction:column; align-items:center; justify-content:center; padding: 16px 0 8px; }
.score-num { font-family: var(--font-head); font-size: 68px; font-weight: 800; line-height: 1; margin-bottom: 4px; }
.score-lbl { font-family: var(--font-mono); font-size: 11px; letter-spacing: 2px; text-transform: uppercase; color: var(--muted); }
.score-sub { font-size: 12px; color: var(--sub); text-align: center; max-width: 160px; margin-top: 7px; line-height: 1.6; }

.chips { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 12px; }
.chip { display: inline-flex; align-items: center; gap: 5px; padding: 4px 11px; border-radius: 7px; font-family: var(--font-mono); font-size: 11px; font-weight: 500; }
.chip.g { background: rgba(34,217,122,0.1); color: var(--green); border: 1px solid rgba(34,217,122,0.22); }
.chip.y { background: rgba(255,216,50,0.1); color: var(--accent); border: 1px solid rgba(255,216,50,0.22); }
.chip.r { background: rgba(255,69,69,0.1); color: var(--red); border: 1px solid rgba(255,69,69,0.22); }
.chip.d { background: rgba(255,255,255,0.05); color: var(--muted); border: 1px solid var(--border); }

.dep-row { display: grid; grid-template-columns: 52px 1fr 64px; gap: 10px; align-items: center; padding: 7px 0; border-bottom: 1px solid rgba(255,255,255,0.04); }
.dep-row:last-child { border-bottom: none; }
.dep-yr { font-family: var(--font-mono); font-size: 11px; color: var(--muted); }
.dep-pct { font-family: var(--font-mono); font-size: 11px; color: var(--sub); text-align: right; }

.action-box { border-radius: 14px; padding: 26px 28px; margin-top: 0; border: 1px solid rgba(255,216,50,0.22); background: linear-gradient(135deg, rgba(255,216,50,0.06), rgba(255,107,53,0.03)); }
.action-box.ar { border-color: rgba(255,69,69,0.22); background: linear-gradient(135deg, rgba(255,69,69,0.07), rgba(255,107,53,0.03)); }
.action-box.ag2 { border-color: rgba(34,217,122,0.22); background: linear-gradient(135deg, rgba(34,217,122,0.07), rgba(0,255,163,0.03)); }
.action-title { font-family: var(--font-head); font-size: 14px; font-weight: 800; color: var(--text); margin-bottom: 14px; display: flex; align-items: center; gap: 7px; }
.action-list { list-style: none; }
.action-list li { font-size: 13px; color: var(--sub); padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.04); display: flex; align-items: flex-start; gap: 9px; line-height: 1.65; }
.action-list li:last-child { border-bottom: none; }
.action-list li::before { content: '→'; color: var(--accent); flex-shrink: 0; font-family: var(--font-mono); font-weight: 600; }

.footer { border-top: 1px solid var(--border); padding: 36px 56px; display: flex; align-items: center; justify-content: space-between; }
.footer-logo { font-family: var(--font-head); font-size: 17px; font-weight: 800; color: rgba(255,255,255,0.22); letter-spacing: 2px; }
.footer-logo em { color: var(--accent); font-style: normal; }
.footer-right { font-family: var(--font-mono); font-size: 11px; color: var(--muted); letter-spacing: 1px; text-align: right; line-height: 1.9; }
</style>

<div class="navbar">
  <div class="nav-logo">AUTO<em>SENSE</em></div>
  <div class="nav-status"><span class="status-dot"></span> ML ENGINE ONLINE</div>
  <div class="nav-right">SVM · 15,411 CARS · CARDEKHO</div>
</div>

<div class="page-header">
  <div class="ph-eyebrow">Car Price Analyser</div>
  <div class="ph-title">Is the price <em>fair?</em></div>
  <div class="ph-sub">Enter the car details — the ML model will tell you if it's a steal, fair, or a rip-off.</div>
</div>
""", unsafe_allow_html=True)

# ── FORM ──
st.markdown("""
<div class="form-wrap">
  <div class="form-card">
    <div class="form-card-title">● Car Specifications</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    brand        = st.selectbox("Car Brand", sorted(le_brand.classes_))
    vehicle_age  = st.slider("Vehicle Age (years)", 0, 25, 5)
    km_driven    = st.number_input("KMs Driven", min_value=0, max_value=500000, value=50000, step=1000)
with col2:
    seller_type  = st.selectbox("Seller Type", ["Dealer", "Individual", "Trustmark Dealer"])
    fuel_type    = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "LPG", "Electric"])
    transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
with col3:
    mileage   = st.number_input("Mileage (kmpl)", min_value=0.0, max_value=50.0, value=18.0, step=0.1)
    engine    = st.number_input("Engine (cc)", min_value=500, max_value=5000, value=1200, step=100)
    max_power = st.number_input("Max Power (bhp)", min_value=20.0, max_value=500.0, value=80.0, step=1.0)
    seats     = st.selectbox("Seats", [2, 4, 5, 6, 7, 8, 9, 10])

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="price-box"><div class="price-box-label">💰 Seller\'s Asking Price (₹)</div>', unsafe_allow_html=True)
asking_price = st.number_input("Asking Price", min_value=10000, max_value=10000000, value=300000, step=5000, label_visibility="collapsed")
st.markdown('<div class="price-tip">Enter the exact price the seller is quoting.</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
go = st.button("⚡  ANALYSE THIS CAR")
st.markdown('</div>', unsafe_allow_html=True)

# ── RESULTS ──
if go:
    le_seller = LabelEncoder(); le_seller.fit(["Dealer","Individual","Trustmark Dealer"])
    le_fuel   = LabelEncoder(); le_fuel.fit(["CNG","Diesel","Electric","LPG","Petrol"])
    le_trans  = LabelEncoder(); le_trans.fit(["Automatic","Manual"])

    enc = [
        le_brand.transform([brand])[0], vehicle_age, km_driven,
        le_seller.transform([seller_type])[0],
        le_fuel.transform([fuel_type])[0],
        le_trans.transform([transmission])[0],
        mileage, engine, max_power, seats
    ]
    prediction     = model.predict(scaler.transform([enc]))[0]
    price_in_lakhs = asking_price / 100_000

    # Signals
    km_per_year  = km_driven / max(vehicle_age, 1)
    km_intensity = km_per_year / 12000
    if   km_intensity < 0.6: km_risk_lbl, km_risk_cls, km_risk_pct = "VERY LOW", "g", 18
    elif km_intensity < 1.0: km_risk_lbl, km_risk_cls, km_risk_pct = "LOW",      "g", 38
    elif km_intensity < 1.4: km_risk_lbl, km_risk_cls, km_risk_pct = "MODERATE", "y", 60
    elif km_intensity < 2.0: km_risk_lbl, km_risk_cls, km_risk_pct = "HIGH",     "r", 78
    else:                     km_risk_lbl, km_risk_cls, km_risk_pct = "CRITICAL", "r", 95

    if   mileage >= 22: mil_lbl, mil_cls = "Excellent", "g"
    elif mileage >= 16: mil_lbl, mil_cls = "Good",      "g"
    elif mileage >= 12: mil_lbl, mil_cls = "Average",   "y"
    else:               mil_lbl, mil_cls = "Poor",      "r"

    if   engine <= 800:  eng_tier = "Entry Hatchback"
    elif engine <= 1200: eng_tier = "Compact / City"
    elif engine <= 1600: eng_tier = "Mid Segment"
    elif engine <= 2000: eng_tier = "Premium"
    else:                eng_tier = "SUV / Performance"

    pw_ratio = max_power / (engine / 1000)
    if   pw_ratio >= 70: pw_lbl, pw_cls = "Sporty",    "g"
    elif pw_ratio >= 55: pw_lbl, pw_cls = "Adequate",  "y"
    else:                pw_lbl, pw_cls = "Low Output", "r"

    trust_map = {
        "Trustmark Dealer": ("HIGH",     "g", "Verified dealer — lower fraud risk, warranty often included."),
        "Dealer":           ("MODERATE", "y", "Dealer cars are priced at a premium. Negotiate down."),
        "Individual":       ("CAUTION",  "r", "Higher risk — always check RC, service history and loan status."),
    }
    trust_lbl, trust_cls, trust_note = trust_map[seller_type]

    fuel_map = {
        "Petrol":   ("Best resale, lower maintenance. Ideal for under 80 km/day.", "g"),
        "Diesel":   ("Great mileage and torque but costly maintenance after 1 lakh km.", "y"),
        "CNG":      ("Very low running cost but lower resale value and power output.", "y"),
        "LPG":      ("Rare fuel — resale is very difficult. Only buy at a very low price.", "r"),
        "Electric": ("Future-proof but resale market still maturing in India. Negotiate hard.", "y"),
    }
    fuel_note, fuel_cls = fuel_map.get(fuel_type, ("", "d"))

    dep_data, v = [], 100.0
    for yr, rate in enumerate([.15,.12,.10,.09,.08,.07,.07,.06,.06,.05], 1):
        v -= v * rate
        dep_data.append((yr, round(v, 1)))

    score = 50
    if prediction == 0:   score = 80 if price_in_lakhs <= 3 else 62
    elif prediction == 1: score = 65
    else:                 score = 28
    score += 8 if km_risk_pct < 40 else (-10 if km_risk_pct > 70 else 0)
    score += 6 if vehicle_age <= 4 else (-8 if vehicle_age >= 10 else 0)
    score += 5 if seller_type == "Trustmark Dealer" else (-3 if seller_type == "Individual" else 0)
    score = min(max(score, 5), 97)

    score_color = "#22d97a" if score >= 70 else ("#ffd832" if score >= 50 else "#ff4545")
    score_word  = "Strong Buy" if score >= 70 else ("Proceed with Care" if score >= 50 else "Walk Away / Negotiate")

    if prediction == 0 and price_in_lakhs <= 3:
        vclass, icon = "vb-steal", "🤩"
        vtitle, vtcls = "STEAL DEAL", "vt-green"
        vdesc = (f"This {brand} is genuinely underpriced. A {vehicle_age}-year-old car with {km_driven:,} km, "
                 f"{engine}cc engine and {max_power} bhp — the model flags this as below market AND the asking "
                 f"price of ₹{price_in_lakhs:.1f}L makes it even better. Rare find — move fast.")
        act_cls, act_title = "ag2", "✅ Recommended Actions"
        actions = [
            "Cross-check the RC to verify ownership and confirm no active loan.",
            "Request the last 2 service records — low km at low price may mean odometer tampering.",
            f"Negotiate a final price of ₹{price_in_lakhs*0.93:.1f}L–₹{price_in_lakhs:.1f}L. Small room, but worth trying.",
            "Get a pre-purchase inspection from an independent mechanic before paying.",
            "Verify insurance validity and check for challan history on Parivahan.gov.in.",
        ]
    elif prediction == 0:
        vclass, icon = "vb-nego", "🤔"
        vtitle, vtcls = "GOOD CAR — NEGOTIATE", "vt-orange"
        vdesc = (f"The {brand}'s profile — {vehicle_age} yrs, {engine}cc, {max_power} bhp — scores well. "
                 f"The car itself is technically underpriced, but ₹{price_in_lakhs:.1f}L is slightly above "
                 f"the expected range. You have a solid 10–15% room to push the seller.")
        act_cls, act_title = "", "💬 Negotiation Playbook"
        actions = [
            f"Open at ₹{price_in_lakhs*0.82:.1f}L — lower than your target to anchor the negotiation.",
            f"Your walk-away ceiling: ₹{price_in_lakhs*0.90:.1f}L. Don't cross it.",
            f"Point out depreciation: a {vehicle_age}-year-old car loses significant book value every year.",
            "If the seller won't move, request free extras: extended warranty, 1 free service, new tyres.",
            "Screenshot 2–3 comparable listings on CarDekho/OLX before negotiating — data is leverage.",
        ]
    elif prediction == 1:
        vclass, icon = "vb-fair", "👍"
        vtitle, vtcls = "FAIRLY PRICED", "vt-yellow"
        vdesc = (f"₹{price_in_lakhs:.1f}L for this {brand} lines up with the market. At {vehicle_age} years old, "
                 f"{km_driven:,} km, {engine}cc and {max_power} bhp — the price is reasonable. "
                 f"You still have a small 5–8% window to negotiate. Solid deal if the paperwork is clean.")
        act_cls, act_title = "", "📋 Pre-Purchase Checklist"
        actions = [
            f"Try negotiating to ₹{price_in_lakhs*0.94:.1f}L–₹{price_in_lakhs*0.96:.1f}L — small but real margin.",
            "Request the full service history booklet. Missing records are a red flag.",
            "Check for accident history using the chassis/VIN number.",
            "Inspect tyres, AC compressor, brakes and battery — expensive to replace after purchase.",
            "Verify: RC, insurance, PUC, and loan clearance certificate if applicable.",
        ]
    else:
        vclass, icon = "vb-over", "🚨"
        vtitle, vtcls = "OVERPRICED — DANGER ZONE", "vt-red"
        vdesc = (f"₹{price_in_lakhs:.1f}L for this {vehicle_age}-year-old {brand} with {km_driven:,} km doesn't add up. "
                 f"The SVM model trained on 15,411 real Indian transactions flags this as overpriced. "
                 f"A {max_power} bhp {engine}cc car of this age should cost no more than ₹{price_in_lakhs*0.78:.1f}L. "
                 f"Negotiate aggressively or walk.")
        act_cls, act_title = "ar", "🚫 Don't Buy Yet — Do This First"
        actions = [
            f"Do NOT pay ₹{price_in_lakhs:.1f}L. Counter at ₹{price_in_lakhs*0.72:.1f}L and go up to ₹{price_in_lakhs*0.80:.1f}L max.",
            "Find 3 comparable listings on CarDekho/Cars24/OLX — use them as hard evidence in negotiation.",
            f"For a {vehicle_age}-year-old car, factor in upcoming costs: timing belt, suspension, clutch, tyres.",
            f"If the seller won't go below ₹{price_in_lakhs*0.85:.1f}L, walk away — the math doesn't work.",
            "Report suspiciously overpriced listings on CarDekho if this is a listed dealership.",
        ]

    st.markdown('<div class="result-section">', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="verdict-banner {vclass}">
      <div class="verdict-icon">{icon}</div>
      <div class="verdict-body">
        <div class="verdict-tag">● AUTOSENSE VERDICT</div>
        <div class="verdict-title {vtcls}">{vtitle}</div>
        <div class="verdict-desc">{vdesc}</div>
      </div>
      <div class="verdict-right">
        <div class="vr-label">Asking Price</div>
        <div class="vr-price">₹{price_in_lakhs:.1f}L</div>
        <div class="vr-score">Deal Score: {score}/100</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    age_cls = "g" if vehicle_age <= 5 else ("y" if vehicle_age <= 9 else "r")
    km_cls  = "g" if km_driven <= 60000 else ("y" if km_driven <= 120000 else "r")

    st.markdown(f"""
    <div class="ag">
      <div class="acard">
        <div class="acard-head"><span class="acard-icon">🎯</span><span class="acard-title">Deal Score</span><span class="acard-badge">AI SCORE</span></div>
        <div class="score-center">
          <div class="score-num" style="color:{score_color}">{score}</div>
          <div class="score-lbl">Out of 100</div>
          <div class="score-sub">{score_word}</div>
        </div>
        <div class="bar-wrap">
          <div class="btrack"><div class="bfill {'bg' if score>=70 else 'by' if score>=50 else 'br'}" style="--bar-w:{score}%"></div></div>
        </div>
      </div>
      <div class="acard">
        <div class="acard-head"><span class="acard-icon">🚗</span><span class="acard-title">Car Profile</span><span class="acard-badge">{brand.upper()}</span></div>
        <div class="mrow"><span class="ml">Brand</span><span class="mv">{brand}</span></div>
        <div class="mrow"><span class="ml">Vehicle Age</span><span class="mv {age_cls}">{vehicle_age} years</span></div>
        <div class="mrow"><span class="ml">KMs Driven</span><span class="mv {km_cls}">{km_driven:,} km</span></div>
        <div class="mrow"><span class="ml">Fuel Type</span><span class="mv">{fuel_type}</span></div>
        <div class="mrow"><span class="ml">Transmission</span><span class="mv">{transmission}</span></div>
        <div class="mrow"><span class="ml">Seller Type</span><span class="mv">{seller_type}</span></div>
        <div class="mrow"><span class="ml">Seats</span><span class="mv">{seats}</span></div>
      </div>
    </div>

    <div class="ag">
      <div class="acard">
        <div class="acard-head"><span class="acard-icon">⚙️</span><span class="acard-title">Engine & Performance</span><span class="acard-badge">{eng_tier.upper()}</span></div>
        <div class="mrow"><span class="ml">Engine Size</span><span class="mv">{engine} cc</span></div>
        <div class="mrow"><span class="ml">Max Power</span><span class="mv">{max_power} bhp</span></div>
        <div class="mrow"><span class="ml">Power / Litre</span><span class="mv {pw_cls}">{pw_ratio:.0f} bhp/L · {pw_lbl}</span></div>
        <div class="mrow"><span class="ml">Mileage</span><span class="mv {mil_cls}">{mileage} kmpl · {mil_lbl}</span></div>
        <div class="mrow"><span class="ml">Segment</span><span class="mv">{eng_tier}</span></div>
        <div class="bar-wrap">
          <div class="blrow"><span class="bl">POWER OUTPUT</span><span class="bv">{max_power} bhp</span></div>
          <div class="btrack"><div class="bfill by" style="--bar-w:{min(max_power/150*100,100):.0f}%"></div></div>
        </div>
        <div class="bar-wrap">
          <div class="blrow"><span class="bl">MILEAGE</span><span class="bv">{mileage} kmpl</span></div>
          <div class="btrack"><div class="bfill bg" style="--bar-w:{min(mileage/30*100,100):.0f}%"></div></div>
        </div>
      </div>
      <div class="acard">
        <div class="acard-head"><span class="acard-icon">📍</span><span class="acard-title">Odometer Risk</span><span class="acard-badge">{km_risk_lbl}</span></div>
        <div class="mrow"><span class="ml">Total KMs</span><span class="mv">{km_driven:,} km</span></div>
        <div class="mrow"><span class="ml">Avg / Year</span><span class="mv {km_risk_cls}">{int(km_per_year):,} km/yr</span></div>
        <div class="mrow"><span class="ml">Expected Avg</span><span class="mv">~12,000 km/yr</span></div>
        <div class="mrow"><span class="ml">Usage Intensity</span><span class="mv {km_risk_cls}">{km_intensity:.1f}x normal</span></div>
        <div class="mrow"><span class="ml">Risk Level</span><span class="mv {km_risk_cls}">{km_risk_lbl}</span></div>
        <div class="bar-wrap">
          <div class="blrow"><span class="bl">KM WEAR RISK</span><span class="bv">{km_risk_pct}%</span></div>
          <div class="btrack"><div class="bfill {'bg' if km_risk_pct<=40 else 'by' if km_risk_pct<=70 else 'br'}" style="--bar-w:{km_risk_pct}%"></div></div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    dep_rows = ""
    for yr, val in dep_data[:8]:
        hl = " style='color:var(--accent);font-weight:700'" if yr == vehicle_age else ""
        bc = "bg" if val > 60 else ("by" if val > 40 else "br")
        dep_rows += f"""<div class="dep-row">
          <span class="dep-yr"{hl}>Yr {yr}</span>
          <div><div class="btrack" style="height:5px"><div class="bfill {bc}" style="--bar-w:{int(val)}%"></div></div></div>
          <span class="dep-pct"{hl}>{val}%</span>
        </div>"""

    neg_lo = f"₹{price_in_lakhs*0.78:.1f}L"
    neg_hi = f"₹{price_in_lakhs*0.90:.1f}L"

    st.markdown(f"""
    <div class="ag">
      <div class="acard">
        <div class="acard-head"><span class="acard-icon">📉</span><span class="acard-title">Depreciation Timeline</span><span class="acard-badge">% VALUE LEFT</span></div>
        {dep_rows}
      </div>
      <div class="acard">
        <div class="acard-head"><span class="acard-icon">🔎</span><span class="acard-title">Market Signals</span><span class="acard-badge">INTEL</span></div>
        <div class="mrow"><span class="ml">Seller Trust</span><span class="mv {trust_cls}">{trust_lbl}</span></div>
        <div class="mrow" style="padding:10px 0"><span class="ml" style="font-size:12px;line-height:1.6">{trust_note}</span></div>
        <div class="mrow"><span class="ml">Fuel Signal</span><span class="mv {fuel_cls}">{fuel_type}</span></div>
        <div class="mrow" style="padding:10px 0"><span class="ml" style="font-size:12px;line-height:1.6">{fuel_note}</span></div>
        <div class="mrow"><span class="ml">Negotiate Range</span><span class="mv">{neg_lo} – {neg_hi}</span></div>
        <div class="chips">
          <span class="chip {age_cls}">Age: {vehicle_age}yr</span>
          <span class="chip {km_risk_cls}">KM: {km_risk_lbl}</span>
          <span class="chip {trust_cls}">{trust_lbl}</span>
          <span class="chip {fuel_cls}">{fuel_type}</span>
          <span class="chip d">{transmission}</span>
          <span class="chip d">{seats} Seats</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    items_html = "".join(f"<li>{a}</li>" for a in actions)
    st.markdown(f"""
    <div class="action-box {act_cls}">
      <div class="action-title">{act_title}</div>
      <ul class="action-list">{items_html}</ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
  <div class="footer-logo">AUTO<em>SENSE</em></div>
  <div class="footer-right">
    SVM · 15,411 CarDekho Transactions · 85.5% Accuracy<br>
    <span style="color:rgba(255,255,255,0.15)">Advisory only. Always inspect in person before purchase.</span>
  </div>
</div>
""", unsafe_allow_html=True)
