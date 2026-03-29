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
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500&display=swap');

* { font-family: 'Space Grotesk', sans-serif; margin: 0; padding: 0; box-sizing: border-box; }

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}
@keyframes glowPulse {
    0%, 100% { box-shadow: 0 0 20px rgba(34,197,94,0.4); }
    50% { box-shadow: 0 0 50px rgba(34,197,94,0.9); }
}
@keyframes scanLine {
    0% { top: -2px; }
    100% { top: 100vh; }
}
@keyframes borderGlow {
    0%, 100% { border-color: rgba(34,197,94,0.2); }
    50% { border-color: rgba(34,197,94,0.7); }
}
@keyframes shimmer {
    0% { background-position: -200% center; }
    100% { background-position: 200% center; }
}
@keyframes ripple {
    0% { transform: scale(0.95); opacity: 1; }
    100% { transform: scale(1.5); opacity: 0; }
}
@keyframes typewriter {
    from { width: 0; }
    to { width: 100%; }
}
@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
}
@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-40px); }
    to { opacity: 1; transform: translateX(0); }
}
@keyframes slideInRight {
    from { opacity: 0; transform: translateX(40px); }
    to { opacity: 1; transform: translateX(0); }
}
@keyframes particle {
    0% { transform: translateY(0) translateX(0); opacity: 1; }
    100% { transform: translateY(-100px) translateX(50px); opacity: 0; }
}

.stApp {
    background: #030806;
    min-height: 100vh;
}

.scan-line {
    position: fixed;
    left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #22c55e, transparent);
    animation: scanLine 5s linear infinite;
    z-index: 9999;
    pointer-events: none;
}

.navbar {
    background: rgba(3,8,6,0.97);
    backdrop-filter: blur(30px);
    border-bottom: 1px solid rgba(34,197,94,0.25);
    padding: 0 60px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 72px;
    animation: borderGlow 4s ease infinite;
}

.nav-logo {
    font-size: 26px;
    font-weight: 700;
    color: white;
    letter-spacing: 3px;
}
.nav-logo span { color: #22c55e; }

.nav-links {
    display: flex;
    gap: 36px;
    list-style: none;
}
.nav-links a {
    color: rgba(255,255,255,0.5);
    text-decoration: none;
    font-size: 13px;
    font-weight: 500;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    transition: all 0.3s;
    position: relative;
    padding-bottom: 4px;
}
.nav-links a::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0;
    width: 0; height: 1px;
    background: #22c55e;
    transition: width 0.3s;
}
.nav-links a:hover { color: #22c55e; }
.nav-links a:hover::after { width: 100%; }

.nav-badge {
    background: rgba(34,197,94,0.1);
    border: 1px solid rgba(34,197,94,0.4);
    color: #22c55e;
    padding: 8px 18px;
    border-radius: 30px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    animation: glowPulse 2s ease infinite;
}

.hero-section {
    text-align: center;
    padding: 90px 40px 60px;
    animation: fadeInUp 1s ease;
    position: relative;
}

.hero-tag {
    display: inline-block;
    background: rgba(34,197,94,0.08);
    border: 1px solid rgba(34,197,94,0.3);
    color: #22c55e;
    padding: 8px 24px;
    border-radius: 30px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 28px;
}

.hero-title {
    font-size: 68px;
    font-weight: 700;
    color: white;
    line-height: 1.1;
    margin-bottom: 24px;
    animation: float 5s ease-in-out infinite;
}
.hero-title .green { color: #22c55e; }
.hero-title .outline {
    -webkit-text-stroke: 2px rgba(255,255,255,0.6);
    color: transparent;
}

.hero-sub {
    font-size: 17px;
    color: rgba(255,255,255,0.45);
    font-weight: 300;
    max-width: 580px;
    margin: 0 auto 50px;
    line-height: 1.8;
    font-family: 'Inter', sans-serif;
}

.stats-row {
    display: flex;
    justify-content: center;
    gap: 70px;
    margin: 40px 0;
    flex-wrap: wrap;
    animation: slideInLeft 1.2s ease;
}
.stat-item { text-align: center; }
.stat-num {
    font-size: 40px;
    font-weight: 700;
    color: #22c55e;
    display: block;
    text-shadow: 0 0 20px rgba(34,197,94,0.4);
}
.stat-lbl {
    font-size: 11px;
    color: rgba(255,255,255,0.35);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 6px;
}

.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(34,197,94,0.4), transparent);
    margin: 10px 60px 40px;
}

.features-banner {
    background: rgba(255,255,255,0.015);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 28px;
    padding: 50px;
    margin: 0 60px 40px;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    animation: fadeInUp 1.3s ease;
}

.feature-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 18px;
    padding: 28px 20px;
    text-align: center;
    transition: all 0.4s ease;
    position: relative;
    overflow: hidden;
}
.feature-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #22c55e, transparent);
    opacity: 0;
    transition: opacity 0.4s;
}
.feature-card:hover { 
    background: rgba(34,197,94,0.05);
    border-color: rgba(34,197,94,0.2);
    transform: translateY(-4px);
}
.feature-card:hover::before { opacity: 1; }
.feature-icon { font-size: 34px; margin-bottom: 14px; display: block; }
.feature-title { font-size: 14px; font-weight: 600; color: white; margin-bottom: 8px; }
.feature-desc { font-size: 12px; color: rgba(255,255,255,0.35); line-height: 1.6; font-family: 'Inter', sans-serif; }
.coming-soon {
    background: rgba(234,179,8,0.08);
    border: 1px solid rgba(234,179,8,0.25);
    color: #eab308;
    padding: 3px 10px;
    border-radius: 10px;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    display: inline-block;
    margin-top: 10px;
}

.analyser-header {
    margin: 0 60px 0;
    padding: 40px 50px 10px;
    animation: slideInLeft 1.4s ease;
}
.analyser-title {
    font-size: 30px;
    font-weight: 700;
    color: white;
    margin-bottom: 6px;
}
.analyser-sub {
    font-size: 14px;
    color: rgba(255,255,255,0.35);
    font-family: 'Inter', sans-serif;
}

.analyser-body {
    margin: 0 60px;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(34,197,94,0.15);
    border-radius: 24px;
    padding: 40px 50px 50px;
    animation: borderGlow 5s ease infinite;
}

div[data-testid="stSelectbox"] label,
div[data-testid="stSlider"] label,
div[data-testid="stNumberInput"] label {
    color: rgba(255,255,255,0.55) !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

div[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: white !important;
}

div[data-testid="stNumberInput"] input {
    background: white !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #111111 !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

div[data-testid="stNumberInput"] button {
    background: rgba(255,255,255,0.08) !important;
    color: white !important;
    border: none !important;
}

div[data-testid="stSlider"] > div > div > div > div {
    background: #22c55e !important;
}

.price-section {
    background: rgba(34,197,94,0.04);
    border: 1px solid rgba(34,197,94,0.2);
    border-radius: 16px;
    padding: 24px 28px;
    margin: 24px 0;
}

.tip-box {
    background: rgba(255,255,255,0.02);
    border-left: 3px solid rgba(34,197,94,0.5);
    border-radius: 0 10px 10px 0;
    padding: 14px 20px;
    margin-top: 16px;
    font-size: 13px;
    color: rgba(255,255,255,0.4);
    font-family: 'Inter', sans-serif;
    line-height: 1.6;
}

.stButton > button {
    background: linear-gradient(135deg, #22c55e, #16a34a) !important;
    color: #030806 !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 20px 40px !important;
    font-size: 15px !important;
    font-weight: 800 !important;
    width: 100% !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    animation: glowPulse 2s ease infinite !important;
    transition: all 0.3s ease !important;
    font-family: 'Space Grotesk', sans-serif !important;
    margin-top: 10px !important;
}
.stButton > button:hover {
    transform: translateY(-3px) !important;
    letter-spacing: 4px !important;
}

.result-container {
    border-radius: 22px;
    padding: 50px 40px;
    text-align: center;
    margin-top: 30px;
    animation: fadeInUp 0.7s ease;
    position: relative;
    overflow: hidden;
}
.result-container::after {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: linear-gradient(45deg, transparent 40%, rgba(255,255,255,0.02) 50%, transparent 60%);
    animation: shimmer 4s ease infinite;
    background-size: 200% auto;
}
.result-great { background: rgba(34,197,94,0.07); border: 1px solid rgba(34,197,94,0.35); }
.result-fair { background: rgba(234,179,8,0.07); border: 1px solid rgba(234,179,8,0.35); }
.result-over { background: rgba(239,68,68,0.07); border: 1px solid rgba(239,68,68,0.35); }
.result-emoji { font-size: 72px; display: block; margin-bottom: 18px; animation: float 3s ease-in-out infinite; }
.result-verdict { font-size: 30px; font-weight: 700; color: white; margin-bottom: 14px; letter-spacing: 1px; }
.result-detail { font-size: 16px; color: rgba(255,255,255,0.55); line-height: 1.8; font-family: 'Inter', sans-serif; max-width: 620px; margin: 0 auto; }

.footer {
    text-align: center;
    padding: 50px 40px;
    color: rgba(255,255,255,0.15);
    font-size: 13px;
    border-top: 1px solid rgba(255,255,255,0.04);
    margin-top: 80px;
    line-height: 2;
}

section[data-testid="stSidebar"] { display: none; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
</style>

<div class="scan-line"></div>

<div class="navbar">
    <div class="nav-logo">AUTO<span>SENSE</span></div>
    <ul class="nav-links">
        <li><a href="#">Analyser</a></li>
        <li><a href="#">Compare Cars</a></li>
        <li><a href="#">Market Trends</a></li>
        <li><a href="#">Price History</a></li>
        <li><a href="#">About</a></li>
    </ul>
    <div class="nav-badge">● LIVE ML ENGINE</div>
</div>

<div class="hero-section">
    <div class="hero-tag">● India's Smartest Car Price Checker</div>
    <div class="hero-title">
        Don't Get <span class="green">Cheated</span><br>
        On Your Next <span class="outline">Car Deal</span>
    </div>
    <div class="hero-sub">AutoSense uses real Machine Learning trained on 15,411 Indian car transactions to tell you in 1 second if a used car is a steal, fair, or a rip-off.</div>
    <div class="stats-row">
        <div class="stat-item"><span class="stat-num">15,411</span><span class="stat-lbl">Cars Trained</span></div>
        <div class="stat-item"><span class="stat-num">85.5%</span><span class="stat-lbl">Accuracy</span></div>
        <div class="stat-item"><span class="stat-num">30+</span><span class="stat-lbl">Brands</span></div>
        <div class="stat-item"><span class="stat-num">SVM</span><span class="stat-lbl">Best Model</span></div>
        <div class="stat-item"><span class="stat-num">&lt;1s</span><span class="stat-lbl">Result Time</span></div>
    </div>
</div>

<div class="section-divider"></div>

<div class="features-banner">
    <div class="feature-card">
        <span class="feature-icon">🧠</span>
        <div class="feature-title">ML Price Engine</div>
        <div class="feature-desc">SVM model trained on 15,411 real Indian car deals from CarDekho</div>
    </div>
    <div class="feature-card">
        <span class="feature-icon">⚡</span>
        <div class="feature-title">Instant Result</div>
        <div class="feature-desc">Analysis in under 1 second — no signup, no waiting, no BS</div>
    </div>
    <div class="feature-card">
        <span class="feature-icon">📊</span>
        <div class="feature-title">Market Trends</div>
        <div class="feature-desc">Live price trends by brand, age and fuel type across India</div>
        <span class="coming-soon">Coming Soon</span>
    </div>
    <div class="feature-card">
        <span class="feature-icon">🔄</span>
        <div class="feature-title">Car Comparator</div>
        <div class="feature-desc">Compare two used cars side by side — pick the better deal</div>
        <span class="coming-soon">Coming Soon</span>
    </div>
    <div class="feature-card">
        <span class="feature-icon">📈</span>
        <div class="feature-title">Price History</div>
        <div class="feature-desc">See how any car model's resale value has changed over the years</div>
        <span class="coming-soon">Coming Soon</span>
    </div>
    <div class="feature-card">
        <span class="feature-icon">🛡️</span>
        <div class="feature-title">Fraud Detector</div>
        <div class="feature-desc">Flags suspiciously low prices that may indicate odometer fraud</div>
        <span class="coming-soon">Coming Soon</span>
    </div>
    <div class="feature-card">
        <span class="feature-icon">📍</span>
        <div class="feature-title">City Price Map</div>
        <div class="feature-desc">Compare car prices across Mumbai, Delhi, Bangalore and more</div>
        <span class="coming-soon">Coming Soon</span>
    </div>
    <div class="feature-card">
        <span class="feature-icon">🤖</span>
        <div class="feature-title">AI Negotiator</div>
        <div class="feature-desc">Get a personalised script to negotiate the best price with any seller</div>
        <span class="coming-soon">Coming Soon</span>
    </div>
</div>

<div class="section-divider"></div>

<div class="analyser-header">
    <div class="analyser-title">🔍 Car Price Analyser</div>
    <div class="analyser-sub">Enter the car details exactly as listed by the seller — we'll do the rest</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="analyser-body">', unsafe_allow_html=True)

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

st.markdown('<div class="price-section">', unsafe_allow_html=True)
asking_price = st.number_input("💰 Seller's Asking Price (₹)", min_value=10000, max_value=10000000, value=300000, step=5000)
st.markdown("""
<div class="tip-box">
💡 Enter the exact price the seller is quoting. AutoSense compares it against what this car should actually cost based on brand, age, mileage, engine power and more.
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if st.button("⚡ ANALYSE THIS CAR NOW"):
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

    if prediction == 0:
        if price_in_lakhs <= 3:
            st.markdown(f"""<div class="result-container result-great">
                <span class="result-emoji">🤩</span>
                <div class="result-verdict">STEAL DEAL — BUY IT NOW!</div>
                <div class="result-detail">This {brand} is genuinely underpriced AND the seller is only asking ₹{price_in_lakhs:.1f}L. Based on its {vehicle_age} year age, {km_driven:,}km driven, {engine}cc engine and {max_power}bhp — this is a rare find. Don't overthink it!</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="result-container result-fair">
                <span class="result-emoji">🤔</span>
                <div class="result-verdict">NEGOTIATE THE PRICE</div>
                <div class="result-detail">This {brand} has features of an underpriced car but the seller is asking ₹{price_in_lakhs:.1f}L which is slightly high. Try negotiating 10-15% down to around ₹{price_in_lakhs*0.87:.1f}L — you have solid room to bargain!</div>
            </div>""", unsafe_allow_html=True)
    elif prediction == 1:
        st.markdown(f"""<div class="result-container result-fair">
            <span class="result-emoji">👍</span>
            <div class="result-verdict">FAIRLY PRICED — REASONABLE DEAL</div>
            <div class="result-detail">This {brand} at ₹{price_in_lakhs:.1f}L is fairly priced based on its {vehicle_age} year age, {km_driven:,}km driven, {engine}cc engine and {max_power}bhp power output. You can proceed confidently or try a small 5% negotiation.</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="result-container result-over">
            <span class="result-emoji">🚨</span>
            <div class="result-verdict">OVERPRICED — DON'T BUY YET!</div>
            <div class="result-detail">At ₹{price_in_lakhs:.1f}L this {brand} is overpriced. A {vehicle_age} year old car with {km_driven:,}km driven and {max_power}bhp should not cost this much in the Indian market. Negotiate hard below ₹{price_in_lakhs*0.78:.1f}L or walk away and find a better deal!</div>
        </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    <strong style="color:rgba(255,255,255,0.4);font-size:18px;letter-spacing:3px;">AUTO<span style="color:#22c55e">SENSE</span></strong><br><br>
    Built with Machine Learning · SVM Algorithm · 15,411 Indian Cars · CarDekho Dataset<br>
    <span style="font-size:11px;color:rgba(255,255,255,0.08);">
        Market Trends · Price History · Car Comparator · City Price Map · AI Negotiator — Coming Soon
    </span>
</div>
""", unsafe_allow_html=True)