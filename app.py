import streamlit as st
import numpy as np
import pandas as pd
import joblib
import os
import glob

st.set_page_config(
    page_title="Fraud Risk Assessment",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Inter:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #FFFFFF;
    color: #000000;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* Responsive inner padding for left column — never clips on any screen size */
div[data-testid="column"]:first-child > div:first-child {
    padding-left: clamp(16px, 5vw, 80px) !important;
    padding-right: clamp(12px, 3vw, 40px) !important;
    padding-top: 32px !important;
    padding-bottom: 36px !important;
}

/* ── TOP BAR ── */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 48px;
    border-bottom: 1px solid #E4E7EE;
    background: #FFFFFF;
}
.topbar-left { display: flex; align-items: baseline; gap: 20px; }
.topbar-wordmark {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    font-size: 18px;
    color: #000000;
    letter-spacing: 0.02em;
}
.topbar-system {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #000000;
    letter-spacing: 0.12em;
    text-transform: uppercase;

    font-weight: 700;}
.topbar-right { display: flex; align-items: center; gap: 24px; }
.model-badge {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.1em;
    color: #000000;
    background: #F4F6F9;
    border: 1px solid #E4E7EE;
    padding: 4px 10px;
}
.status-dot {
    width: 6px; height: 6px;
    background: #1A8A5E;
    border-radius: 50%;
    display: inline-block;
    margin-right: 6px;
}

/* ── MAIN LAYOUT ── */
.main-wrapper {
    display: grid;
    grid-template-columns: 420px 1fr;
    min-height: calc(100vh - 57px);
}
.form-panel {
    background: #FFFFFF;
    border-right: 1px solid #E4E7EE;
    padding: 36px 40px;
    overflow-y: auto;
}
.result-panel {
    background: #FAFBFD;
    padding: 36px 48px;
}

/* ── SECTION HEADERS ── */
.section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.14em;
    color: #000000;
    text-transform: uppercase;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid #E4E7EE;
}

/* ── FORM FIELD ROWS ── */
.field-row {
    margin-bottom: 20px;
}
.field-label {
    font-size: 11px;
    font-weight: 700;
    color: #000000;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 6px;
}

/* Streamlit input overrides */
[data-baseweb="input"] > div,
[data-baseweb="select"] > div:first-child,
[data-baseweb="textarea"] > div {
    background: #F7F8FB !important;
    border: 1px solid #DDE2EB !important;
    border-radius: 4px !important;
    color: #1A1F2E !important;
}
[data-baseweb="input"] > div:focus-within,
[data-baseweb="select"] > div:focus-within {
    border-color: #2F6FED !important;
    box-shadow: none !important;
}
input, .stSelectbox select {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13px !important;
    color: #1A1F2E !important;
    background: transparent !important;
}

/* Slider override */
[data-baseweb="slider"] [data-testid="stThumbValue"] { display: none; }
.stSlider > div > div > div {
    background: #E4E7EE !important;
}
.stSlider > div > div > div > div {
    background: #2F6FED !important;
}

/* Radio button override */
[data-testid="stRadio"] label {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 12px !important;
    color: #000000 !important;

    font-weight: 700;}

/* ── BUTTONS ── */
.stButton button {
    background: #1A1F2E !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 4px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    padding: 10px 24px !important;
    text-transform: uppercase !important;
    transition: background 0.15s !important;
    width: 100% !important;
}
.stButton button:hover {
    background: #2F3A55 !important;
}
.stButton.secondary button {
    background: transparent !important;
    color: #000000 !important;
    border: 1px solid #DDE2EB !important;
}
.stButton.secondary button:hover {
    border-color: #8A93A8 !important;
    color: #1A1F2E !important;
}

/* ── RESULT COMPONENTS ── */
.result-verdict {
    margin-bottom: 32px;
}
.verdict-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.14em;
    color: #000000;
    text-transform: uppercase;
    margin-bottom: 12px;
}
.verdict-status {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    font-size: 38px;
    line-height: 1;
    margin-bottom: 8px;
}
.verdict-safe    { color: #1A8A5E; }
.verdict-caution { color: #B8860B; }
.verdict-fraud   { color: #D1293D; }
.verdict-sub {
    font-size: 13px;
    color: #000000;
    font-weight: 400;
    line-height: 1.5;
}

/* ── RISK METER (signature element) ── */
.risk-meter-wrap {
    margin: 28px 0;
    padding: 20px 0;
    border-top: 1px solid #E4E7EE;
    border-bottom: 1px solid #E4E7EE;
}
.risk-meter-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 10px;
}
.risk-meter-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.14em;
    color: #000000;
    text-transform: uppercase;
}
.risk-meter-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 24px;
    font-weight: 500;
    letter-spacing: -0.02em;
}
.risk-meter-track {
    height: 4px;
    background: #E4E7EE;
    position: relative;
    margin-bottom: 6px;
    border-radius: 2px;
}
.risk-meter-fill {
    height: 100%;
    position: absolute;
    left: 0;
    top: 0;
    border-radius: 2px;
    transition: width 0.6s ease;
}
.risk-meter-scale {
    display: flex;
    justify-content: space-between;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    color: #000000;
    letter-spacing: 0.06em;
}

/* ── DATA TABLE ── */
.data-table { width: 100%; border-collapse: collapse; margin-top: 16px; }
.data-table td {
    padding: 9px 0;
    border-bottom: 1px solid #EEF1F6;
    font-size: 13px;
    vertical-align: top;
}
.data-table td:first-child {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #000000;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    width: 42%;
    padding-right: 16px;

    font-weight: 700;}
.data-table td:last-child {
    color: #000000;
    font-weight: 700;
    text-align: right;
    font-family: 'IBM Plex Mono', monospace;
}

/* ── FACTOR TABLE ── */
.factor-row {
    display: flex;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #EEF1F6;
    gap: 12px;
}
.factor-name {
    flex: 1;
    color: #000000;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.04em;

    font-weight: 700;}
.factor-bar-track {
    width: 120px;
    height: 3px;
    background: #E4E7EE;
    position: relative;
    border-radius: 2px;
}
.factor-bar-fill { height: 100%; position: absolute; left: 0; border-radius: 2px; }
.factor-score {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 500;
    width: 40px;
    text-align: right;
}
.factor-positive { color: #D1293D; }
.factor-negative { color: #1A8A5E; }

/* ── RECOMMENDATION ── */
.rec-box {
    background: #F7F8FB;
    border-left: 3px solid;
    border-radius: 0 4px 4px 0;
    padding: 14px 18px;
    margin-top: 24px;
}
.rec-box.safe    { border-color: #1A8A5E; }
.rec-box.caution { border-color: #B8860B; }
.rec-box.fraud   { border-color: #D1293D; }
.rec-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 6px;

    font-weight: 700;}
.rec-label.safe    { color: #1A8A5E; }
.rec-label.caution { color: #B8860B; }
.rec-label.fraud   { color: #D1293D; }
.rec-text { font-size: 13px; color: #000000; line-height: 1.6; }

/* ── PLACEHOLDER ── */
.placeholder {
    height: 60vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    gap: 12px;
}
.placeholder-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    font-size: 26px;
    color: #C5CBD8;
}
.placeholder-sub {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #000000;
    letter-spacing: 0.1em;
    text-transform: uppercase;

    font-weight: 700;}

/* ── COLS ── */
div[data-testid="column"] { padding: 0 !important; }

/* Streamlit label override */
label[data-testid="stWidgetLabel"] p {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 11px !important;
    font-weight: 700!important;
    color: #000000 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

/* Number input override */
[data-testid="stNumberInput"] input {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13px !important;
}

/* Expander override */
[data-testid="stExpander"] {
    background: #F7F8FB !important;
    border: 1px solid #E4E7EE !important;
    border-radius: 4px !important;
}
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════
# LOAD MODEL
# ════════════════════════════════════════
@st.cache_resource
def load_model():
    model_files  = glob.glob('models/best_model_*.pkl')
    scaler_files = glob.glob('models/scaler.pkl')
    if not model_files or not scaler_files:
        return None, None, "No model loaded"
    model      = joblib.load(model_files[0])
    scaler     = joblib.load(scaler_files[0])
    model_name = (os.path.basename(model_files[0])
                  .replace('best_model_','').replace('.pkl','').replace('_',' '))
    return model, scaler, model_name

model, scaler, model_name = load_model()


# ════════════════════════════════════════
# CONSTANTS
# ════════════════════════════════════════
FEATURE_COLS = [
    'amt','category_enc','hour','dayofweek','month',
    'is_weekend','is_night','age','gender','city_pop',
    'lat','long','merch_lat','merch_long','distance_km','state_enc'
]
CATEGORY_MAP = {
    'entertainment':0,'food_dining':1,'gas_transport':2,
    'grocery_net':3,'grocery_pos':4,'health_fitness':5,
    'home':6,'kids_pets':7,'misc_net':8,'misc_pos':9,
    'personal_care':10,'shopping_net':11,'shopping_pos':12,'travel':13,
}
STATE_MAP = {
    s: i for i, s in enumerate([
        'AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA',
        'HI','ID','IL','IN','IA','KS','KY','LA','ME','MD',
        'MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ',
        'NM','NY','NC','ND','OH','OK','OR','PA','RI','SC',
        'SD','TN','TX','UT','VT','VA','WA','WV','WI','WY'
    ])
}
DAYS = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
CATEGORY_RISK_LEVEL = {
    'shopping_net':'High','misc_net':'High','grocery_net':'Moderate',
    'travel':'Moderate','shopping_pos':'Moderate','misc_pos':'Moderate',
    'food_dining':'Low','gas_transport':'Low','health_fitness':'Low',
    'grocery_pos':'Low','entertainment':'Low','home':'Low',
    'kids_pets':'Low','personal_care':'Low',
}


# ════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════
def haversine(lat1, lon1, lat2, lon2):
    r = np.radians
    a = (np.sin((r(lat2)-r(lat1))/2)**2
         + np.cos(r(lat1))*np.cos(r(lat2))*np.sin((r(lon2)-r(lon1))/2)**2)
    return 6371 * 2 * np.arcsin(np.sqrt(a))

def run_prediction(amt, category, hour, dayofweek, month,
                   age, gender, city_pop, state,
                   lat_n, lon_n, lat_m, lon_m, threshold):
    is_weekend  = 1 if dayofweek >= 5 else 0
    is_night    = 1 if (hour >= 22 or hour <= 4) else 0
    dist        = haversine(lat_n, lon_n, lat_m, lon_m)
    X = pd.DataFrame([{
        'amt':amt,'category_enc':CATEGORY_MAP.get(category,0),
        'hour':hour,'dayofweek':dayofweek,'month':month,
        'is_weekend':is_weekend,'is_night':is_night,
        'age':age,'gender':1 if gender=='Male' else 0,
        'city_pop':city_pop,'lat':lat_n,'long':lon_n,
        'merch_lat':lat_m,'merch_long':lon_m,
        'distance_km':dist,'state_enc':STATE_MAP.get(state,0),
    }])[FEATURE_COLS]
    prob  = model.predict_proba(scaler.transform(X))[0][1]
    return prob, dist, is_night, is_weekend

def risk_factors(amt, hour, dist, age, is_night, category):
    f = {}
    if amt > 1000:    f['Transaction amount (high)']     = +25
    elif amt > 500:   f['Transaction amount (elevated)'] = +12
    else:             f['Transaction amount (normal)']   = -5
    if is_night:      f['Transaction time (off-hours)']  = +20
    elif 9<=hour<=17: f['Transaction time (business)']   = -8
    else:             f['Transaction time (evening)']    = +5
    if dist > 500:    f['Merchant distance (very far)']  = +30
    elif dist > 100:  f['Merchant distance (far)']       = +14
    elif dist < 20:   f['Merchant distance (local)']     = -10
    else:             f['Merchant distance (normal)']    = 0
    if age > 65:      f['Account holder age (senior)']   = +10
    elif age < 25:    f['Account holder age (young)']    = +5
    else:             f['Account holder age (standard)'] = -3
    HIGH = ['shopping_net','misc_net','grocery_net']
    LOW  = ['gas_transport','food_dining','health_fitness','grocery_pos']
    if category in HIGH:   f[f'Merchant category ({category})'] = +15
    elif category in LOW:  f[f'Merchant category ({category})'] = -8
    else:                  f[f'Merchant category ({category})'] = 0
    return f


# ════════════════════════════════════════
# TOP BAR
# ════════════════════════════════════════
st.markdown(f"""
<div class="topbar">
  <div class="topbar-left">
    <span class="topbar-wordmark">Sentinel</span>
    <span class="topbar-system">Fraud Risk Assessment System</span>
  </div>
  <div class="topbar-right">
    <span class="model-badge">MODEL &nbsp;{model_name.upper() if model_name else 'NOT LOADED'}</span>
    <span style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:#8A93A8">
      <span class="status-dot"></span>OPERATIONAL
    </span>
  </div>
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════
# LAYOUT
# ════════════════════════════════════════
left_col, right_col = st.columns([5, 7])

with left_col:
    st.markdown('<div>', unsafe_allow_html=True)

    # Example presets
    st.markdown('<div class="section-label">Load Example</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    load_normal = c1.button("Normal Transaction")
    load_fraud  = c2.button("Flagged Transaction", key="fraud_btn")

    if load_normal:
        st.session_state.update({
            'amt':47.80,'category':'food_dining','hour':13,'dow':1,
            'month':6,'age':38,'gender':'Female','city_pop':480000,
            'state':'CA','lat_n':33.96,'lon_n':-80.93,'lat_m':34.00,'lon_m':-80.97,
        })
    if load_fraud:
        st.session_state.update({
            'amt':1875.00,'category':'shopping_net','hour':2,'dow':6,
            'month':11,'age':71,'gender':'Male','city_pop':1400,
            'state':'NY','lat_n':33.96,'lon_n':-80.93,'lat_m':40.71,'lon_m':-74.00,
        })

    st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)

    # ── Transaction ──
    st.markdown('<div class="section-label">Transaction Details</div>', unsafe_allow_html=True)

    amt = st.number_input("Amount (USD)", min_value=0.01, max_value=99999.99,
                           value=float(st.session_state.get('amt', 47.80)),
                           format="%.2f", step=1.0)
    category = st.selectbox("Merchant Category",
                             options=list(CATEGORY_MAP.keys()),
                             index=list(CATEGORY_MAP.keys()).index(
                                 st.session_state.get('category','food_dining')))
    c1, c2 = st.columns(2)
    hour  = c1.number_input("Hour (0–23)", 0, 23,
                             int(st.session_state.get('hour',13)))
    month = c2.number_input("Month (1–12)", 1, 12,
                             int(st.session_state.get('month',6)))
    dayofweek = st.select_slider("Day of Week", options=list(range(7)),
                                  format_func=lambda x: DAYS[x],
                                  value=int(st.session_state.get('dow',1)))

    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)

    # ── Account ──
    st.markdown('<div class="section-label">Account Information</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    age    = c1.number_input("Age", 18, 100, int(st.session_state.get('age',38)))
    gender = c2.radio("Gender", ['Male','Female'],
                       index=0 if st.session_state.get('gender','Female')=='Male' else 1,
                       horizontal=True)
    c1, c2 = st.columns(2)
    city_pop = c1.number_input("City Population", 100, 9999999,
                                int(st.session_state.get('city_pop',480000)), step=1000)
    state = c2.selectbox("State", list(STATE_MAP.keys()),
                          index=list(STATE_MAP.keys()).index(
                              st.session_state.get('state','CA')))

    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)

    # ── Location ──
    st.markdown('<div class="section-label">Coordinates</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    lat_n = c1.number_input("Cardholder Lat", value=float(st.session_state.get('lat_n',33.9659)),
                              format="%.4f", key="lat_n")
    lon_n = c2.number_input("Cardholder Long", value=float(st.session_state.get('lon_n',-80.9355)),
                              format="%.4f", key="lon_n")
    c1, c2 = st.columns(2)
    lat_m = c1.number_input("Merchant Lat", value=float(st.session_state.get('lat_m',34.00)),
                              format="%.4f", key="lat_m")
    lon_m = c2.number_input("Merchant Long", value=float(st.session_state.get('lon_m',-80.97)),
                              format="%.4f", key="lon_m")

    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)

    # ── Threshold ──
    with st.expander("Detection Sensitivity"):
        threshold = st.slider("Fraud Threshold (%)", 10, 90, 50, 5,
                               help="Lower values increase sensitivity but may raise false positives.")
        st.caption(f"Transactions scoring above {threshold}% are flagged as fraud.")

    st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)
    run_btn = st.button("Run Assessment")
    st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════
# RESULTS PANEL
# ════════════════════════════════════════
with right_col:
    st.markdown('<div style="padding:32px 64px 36px 56px;">', unsafe_allow_html=True)

    if 'last_result' not in st.session_state:
        st.session_state['last_result'] = None

    if run_btn and model is not None:
        prob, dist, is_night, is_weekend = run_prediction(
            amt, category, hour, dayofweek, month,
            age, gender, city_pop, state,
            lat_n, lon_n, lat_m, lon_m, threshold
        )
        st.session_state['last_result'] = {
            'prob': prob, 'dist': dist, 'is_night': is_night,
            'amt': amt, 'category': category, 'hour': hour,
            'dayofweek': dayofweek, 'month': month, 'age': age,
            'gender': gender, 'city_pop': city_pop, 'state': state,
            'threshold': threshold,
        }

    result = st.session_state.get('last_result')

    if result is None:
        st.markdown("""
        <div class="placeholder">
          <div class="placeholder-title">No assessment loaded</div>
          <div class="placeholder-sub">Complete the form and run an assessment</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        prob      = result['prob']
        pct       = round(prob * 100, 1)
        threshold = result['threshold']
        is_fraud  = pct >= threshold

        if pct < 30:
            verdict_class = "verdict-safe"
            verdict_text  = "Low Risk"
            rec_class     = "safe"
            rec_label     = "Recommended Action"
            rec_text      = "Transaction presents no significant fraud indicators. Standard processing is appropriate. Continue routine monitoring."
            meter_color   = "#1A6B4A"
        elif pct < 60:
            verdict_class = "verdict-caution"
            verdict_text  = "Elevated Risk"
            rec_class     = "caution"
            rec_label     = "Recommended Action"
            rec_text      = "Transaction exhibits moderate risk signals. Consider requesting secondary authentication or cardholder verification before approval."
            meter_color   = "#B8860B"
        else:
            verdict_class = "verdict-fraud"
            verdict_text  = "High Risk — Fraud Indicated"
            rec_class     = "fraud"
            rec_label     = "Immediate Action Required"
            rec_text      = "Transaction probability exceeds the fraud threshold. Block transaction, issue a real-time alert to the cardholder, and escalate to the fraud operations team."
            meter_color   = "#C8102E"

        # Verdict
        st.markdown(f"""
        <div class="result-verdict">
          <div class="verdict-label">Risk Verdict</div>
          <div class="verdict-status {verdict_class}">{verdict_text}</div>
          <div class="verdict-sub">
            Fraud probability score of {pct}% against a threshold of {threshold}%.
            Model: {model_name}.
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Risk Meter — the signature element
        st.markdown(f"""
        <div class="risk-meter-wrap">
          <div class="risk-meter-header">
            <span class="risk-meter-title">Fraud Probability</span>
            <span class="risk-meter-value" style="color:{meter_color}">{pct}%</span>
          </div>
          <div class="risk-meter-track">
            <div class="risk-meter-fill" style="width:{pct}%;background:{meter_color};"></div>
            <div style="position:absolute;left:{threshold}%;top:-4px;width:1px;height:11px;background:#4A5270;"></div>
          </div>
          <div class="risk-meter-scale">
            <span>0%</span><span>25%</span>
            <span style="color:#4A5270">T:{threshold}%</span>
            <span>75%</span><span>100%</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Two-column detail tables
        d_col1, d_col2 = st.columns(2)
        with d_col1:
            st.markdown('<div class="section-label">Transaction</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <table class="data-table">
              <tr><td>Amount</td><td>${result['amt']:,.2f}</td></tr>
              <tr><td>Category</td><td>{result['category'].replace('_',' ').title()}</td></tr>
              <tr><td>Category Risk</td><td>{CATEGORY_RISK_LEVEL.get(result['category'],'—')}</td></tr>
              <tr><td>Hour</td><td>{result['hour']:02d}:00</td></tr>
              <tr><td>Day</td><td>{DAYS[result['dayofweek']]}</td></tr>
              <tr><td>Month</td><td>{result['month']}</td></tr>
              <tr><td>Off-Hours</td><td>{'Yes' if result['is_night'] else 'No'}</td></tr>
            </table>
            """, unsafe_allow_html=True)

        with d_col2:
            st.markdown('<div class="section-label">Account + Location</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <table class="data-table">
              <tr><td>Age</td><td>{result['age']} yrs</td></tr>
              <tr><td>Gender</td><td>{result['gender']}</td></tr>
              <tr><td>State</td><td>{result['state']}</td></tr>
              <tr><td>City Population</td><td>{result['city_pop']:,}</td></tr>
              <tr><td>Merchant Distance</td><td>{result['dist']:.1f} km</td></tr>
            </table>
            """, unsafe_allow_html=True)

        # Risk Factors
        st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Risk Factor Breakdown</div>', unsafe_allow_html=True)

        factors = risk_factors(
            result['amt'], result['hour'], result['dist'],
            result['age'], result['is_night'], result['category']
        )
        max_abs = max(abs(v) for v in factors.values()) if factors else 1
        for name, score in sorted(factors.items(), key=lambda x: -abs(x[1])):
            bar_pct  = int(abs(score) / max_abs * 100)
            cls      = "factor-positive" if score > 0 else "factor-negative"
            bar_col  = "#C8102E" if score > 0 else "#1A6B4A"
            sign     = "+" if score > 0 else ""
            st.markdown(f"""
            <div class="factor-row">
              <span class="factor-name">{name}</span>
              <div class="factor-bar-track">
                <div class="factor-bar-fill" style="width:{bar_pct}%;background:{bar_col};"></div>
              </div>
              <span class="factor-score {cls}">{sign}{score}</span>
            </div>
            """, unsafe_allow_html=True)

        # Recommendation
        st.markdown(f"""
        <div class="rec-box {rec_class}">
          <div class="rec-label {rec_class}">{rec_label}</div>
          <div class="rec-text">{rec_text}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
