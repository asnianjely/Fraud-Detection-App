import streamlit as st
import numpy as np
import pandas as pd
import joblib
import os
import glob

st.set_page_config(
    page_title="Sentinel — Fraud Risk Assessment",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700&family=Inter:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; margin: 0; }

.stApp { background: #111318; color: #E8EAF0; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
div[data-testid="column"] { padding: 0 !important; }

/* ── LEFT COLUMN INNER PADDING ── */
div[data-testid="column"]:first-child > div:first-child {
    padding: 36px clamp(20px, 4vw, 56px) 40px clamp(20px, 5vw, 64px) !important;
    background: #16191F;
    border-right: 1px solid #2E3340;
    min-height: 100vh;
}
div[data-testid="column"]:last-child > div:first-child {
    padding: 36px clamp(20px, 5vw, 72px) 40px clamp(20px, 4vw, 56px) !important;
    background: #111318;
    min-height: 100vh;
}

/* ── TOPBAR ── */
.topbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 clamp(20px, 4vw, 56px);
    height: 58px;
    background: #16191F;
    border-bottom: 1px solid #2E3340;
    position: sticky; top: 0; z-index: 100;
}
.topbar-brand {
    display: flex; align-items: center; gap: 10px;
}
.topbar-logo {
    width: 28px; height: 28px;
    background: #111827;
    border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
}
.topbar-logo svg { width: 14px; height: 14px; }
.topbar-name {
    font-family: 'Sora', sans-serif;
    font-size: 15px; font-weight: 700;
    color: #E8EAF0; letter-spacing: -0.01em;
}
.topbar-divider {
    width: 1px; height: 16px;
    background: #2E3340; margin: 0 12px;
}
.topbar-subtitle {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px; color: #5A6175;
    letter-spacing: 0.12em; text-transform: uppercase;
}
.topbar-right { display: flex; align-items: center; gap: 16px; }
.topbar-badge {
    display: flex; align-items: center; gap: 6px;
    background: #22262E; border: 1px solid #2E3340;
    border-radius: 6px; padding: 5px 10px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px; color: #8A92A8; letter-spacing: 0.08em;
}
.topbar-badge span { color: #E8EAF0; font-weight: 500; }
.pulse {
    width: 7px; height: 7px; border-radius: 50%;
    background: #10B981;
    box-shadow: 0 0 0 2px #D1FAE5;
}
.topbar-status {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px; color: #10B981; letter-spacing: 0.1em;
    display: flex; align-items: center; gap: 6px;
}

/* ── SECTION LABEL ── */
.sec-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px; font-weight: 500;
    letter-spacing: 0.16em; color: #5A6175;
    text-transform: uppercase;
    margin: 0 0 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid #2A2F3A;
    display: flex; align-items: center; gap: 8px;
}
.sec-label::before {
    content: '';
    display: inline-block;
    width: 3px; height: 12px;
    background: #6366F1;
    border-radius: 2px;
}

/* ── STREAMLIT WIDGET OVERRIDES ── */
label[data-testid="stWidgetLabel"] p {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 10px !important; font-weight: 500 !important;
    color: #6B7280 !important; letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}
[data-baseweb="input"] > div,
[data-baseweb="select"] > div:first-child {
    background: #22262E !important;
    border: 1px solid #2E3340 !important;
    border-radius: 8px !important;
    transition: border-color .15s !important;
}
[data-baseweb="input"] > div:focus-within,
[data-baseweb="select"] > div:focus-within {
    border-color: #6366F1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.08) !important;
}
input {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13px !important; color: #111827 !important;
    background: transparent !important;
}
[data-testid="stNumberInput"] input { font-size: 13px !important; }
[data-testid="stRadio"] label {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 12px !important; color: #374151 !important;
}
[data-testid="stExpander"] {
    background: #22262E !important;
    border: 1px solid #2E3340 !important;
    border-radius: 8px !important;
}
[data-baseweb="slider"] [data-testid="stThumbValue"] { display: none; }

/* ── BUTTONS ── */
.stButton button {
    background: #111827 !important; color: #FFFFFF !important;
    border: none !important; border-radius: 8px !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 12px !important; font-weight: 600 !important;
    letter-spacing: 0.04em !important; padding: 11px 24px !important;
    text-transform: uppercase !important; width: 100% !important;
    transition: all .2s !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.15) !important;
}
.stButton button:hover {
    background: #D0D4DF !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
    transform: translateY(-1px) !important;
}
.stButton button:active { transform: translateY(0) !important; }

/* Example preset buttons — outlined style */
.stButton:not(:last-child) button {
    background: #22262E !important; color: #B8BDD0 !important;
    border: 1px solid #2E3340 !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
    font-size: 11px !important;
}
.stButton:not(:last-child) button:hover {
    border-color: #6366F1 !important; color: #6366F1 !important;
    background: #1F2329 !important;
    box-shadow: 0 2px 8px rgba(99,102,241,0.12) !important;
    transform: translateY(-1px) !important;
}

/* ── VERDICT CARD ── */
.verdict-card {
    background: #1D2027;
    border: 1px solid #2E3340;
    border-radius: 12px;
    padding: 24px 28px;
    margin-bottom: 20px;
    position: relative; overflow: hidden;
}
.verdict-card::before {
    content: '';
    position: absolute; left: 0; top: 0; bottom: 0;
    width: 4px;
    border-radius: 12px 0 0 12px;
}
.verdict-card.safe::before   { background: #10B981; }
.verdict-card.caution::before { background: #F59E0B; }
.verdict-card.fraud::before  { background: #EF4444; }
.verdict-card.safe   { border-color: #D1FAE5; }
.verdict-card.caution { border-color: #FEF3C7; }
.verdict-card.fraud  { border-color: #FEE2E2; }
.verdict-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px; letter-spacing: 0.16em;
    color: #5A6175; text-transform: uppercase; margin-bottom: 8px;
}
.verdict-headline {
    font-family: 'Sora', sans-serif;
    font-size: 32px; font-weight: 700; line-height: 1.1;
    letter-spacing: -0.02em; margin-bottom: 8px;
}
.verdict-headline.safe    { color: #059669; }
.verdict-headline.caution { color: #D97706; }
.verdict-headline.fraud   { color: #DC2626; }
.verdict-desc { font-size: 13px; color: #8A92A8; line-height: 1.6; }
.verdict-chip {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 4px 10px; border-radius: 20px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px; font-weight: 500;
    margin-top: 12px;
}
.verdict-chip.safe    { background: #ECFDF5; color: #059669; }
.verdict-chip.caution { background: #FFFBEB; color: #D97706; }
.verdict-chip.fraud   { background: #FEF2F2; color: #DC2626; }

/* ── RISK METER ── */
.meter-card {
    background: #22262E; border: 1px solid #2E3340;
    border-radius: 12px; padding: 20px 24px; margin-bottom: 20px;
}
.meter-header {
    display: flex; justify-content: space-between;
    align-items: flex-end; margin-bottom: 14px;
}
.meter-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px; font-weight: 500;
    letter-spacing: 0.14em; color: #5A6175; text-transform: uppercase;
}
.meter-pct {
    font-family: 'Sora', sans-serif;
    font-size: 28px; font-weight: 700; letter-spacing: -0.03em;
    line-height: 1;
}
.meter-track {
    height: 8px; background: #2A2F3A;
    border-radius: 99px; position: relative; overflow: hidden;
    margin-bottom: 8px;
}
.meter-fill {
    height: 100%; border-radius: 99px;
    transition: width .8s cubic-bezier(.4,0,.2,1);
}
.meter-zones {
    display: flex; height: 3px; border-radius: 99px;
    overflow: hidden; gap: 2px; margin-bottom: 8px;
}
.meter-zone-s { flex: 30; background: #D1FAE5; }
.meter-zone-m { flex: 30; background: #FEF3C7; }
.meter-zone-h { flex: 40; background: #FEE2E2; }
.meter-scale {
    display: flex; justify-content: space-between;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px; color: #4B5563;
}
.meter-threshold-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px; color: #5A6175; margin-top: 8px;
    text-align: center;
}

/* ── STATS GRID ── */
.stats-grid {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 10px; margin-bottom: 20px;
}
.stat-card {
    background: #22262E; border: 1px solid #2E3340;
    border-radius: 10px; padding: 14px 16px;
}
.stat-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px; letter-spacing: 0.12em;
    color: #5A6175; text-transform: uppercase; margin-bottom: 4px;
}
.stat-value {
    font-family: 'Sora', sans-serif;
    font-size: 18px; font-weight: 700; color: #E8EAF0; letter-spacing: -0.02em;
}
.stat-sub { font-size: 11px; color: #5A6175; margin-top: 2px; }

/* ── DATA TABLE ── */
.dt-wrap {
    background: #22262E; border: 1px solid #2E3340;
    border-radius: 10px; overflow: hidden; margin-bottom: 20px;
}
.dt-head {
    background: #22262E; padding: 10px 16px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px; font-weight: 500;
    letter-spacing: 0.12em; color: #8A92A8; text-transform: uppercase;
    border-bottom: 1px solid #2E3340;
}
.data-table { width: 100%; border-collapse: collapse; }
.data-table td {
    padding: 10px 16px; border-bottom: 1px solid #2A2F3A; font-size: 12px;
}
.data-table tr:last-child td { border-bottom: none; }
.data-table td:first-child {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px; color: #5A6175;
    letter-spacing: 0.06em; text-transform: uppercase; width: 45%;
}
.data-table td:last-child {
    color: #E8EAF0; font-weight: 600; text-align: right;
    font-family: 'IBM Plex Mono', monospace; font-size: 12px;
}

/* ── FACTOR BREAKDOWN ── */
.factor-wrap {
    background: #22262E; border: 1px solid #2E3340;
    border-radius: 10px; overflow: hidden; margin-bottom: 20px;
}
.factor-head {
    background: #22262E; padding: 10px 16px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px; font-weight: 500;
    letter-spacing: 0.12em; color: #8A92A8; text-transform: uppercase;
    border-bottom: 1px solid #2E3340;
}
.factor-row {
    display: flex; align-items: center;
    padding: 11px 16px; border-bottom: 1px solid #2A2F3A; gap: 12px;
}
.factor-row:last-child { border-bottom: none; }
.factor-dot {
    width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0;
}
.factor-name {
    flex: 1; font-size: 12px; color: #B8BDD0; font-weight: 400;
}
.factor-bar-track {
    width: 80px; height: 4px;
    background: #2A2F3A; border-radius: 99px; position: relative;
}
.factor-bar-fill { height: 100%; border-radius: 99px; position: absolute; left: 0; }
.factor-score {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px; font-weight: 500; width: 34px; text-align: right;
}
.f-pos { color: #EF4444; }
.f-neg { color: #10B981; }

/* ── RECOMMENDATION ── */
.rec-card {
    border-radius: 10px; padding: 16px 20px; margin-bottom: 8px;
}
.rec-card.safe    { background: #ECFDF5; border: 1px solid #A7F3D0; }
.rec-card.caution { background: #FFFBEB; border: 1px solid #FDE68A; }
.rec-card.fraud   { background: #FEF2F2; border: 1px solid #FECACA; }
.rec-card-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px; font-weight: 500;
    letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 6px;
}
.rec-card.safe    .rec-card-label { color: #059669; }
.rec-card.caution .rec-card-label { color: #D97706; }
.rec-card.fraud   .rec-card-label { color: #DC2626; }
.rec-card-text { font-size: 13px; line-height: 1.65; }
.rec-card.safe    .rec-card-text { color: #065F46; }
.rec-card.caution .rec-card-text { color: #92400E; }
.rec-card.fraud   .rec-card-text { color: #991B1B; }

/* ── PLACEHOLDER ── */
.placeholder-wrap {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    height: 60vh; gap: 12px; text-align: center;
}
.placeholder-icon {
    width: 56px; height: 56px; border-radius: 16px;
    background: #2A2F3A; display: flex; align-items: center;
    justify-content: center; margin-bottom: 4px;
}
.placeholder-title {
    font-family: 'Sora', sans-serif;
    font-size: 20px; font-weight: 600; color: #4B5563;
}
.placeholder-sub {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px; color: #B8BDD0; letter-spacing: 0.1em; text-transform: uppercase;
}

/* ── SPACER ── */
.sp8  { height: 8px;  }
.sp16 { height: 16px; }
.sp24 { height: 24px; }
</style>
""", unsafe_allow_html=True)


# ── Load Model ──
@st.cache_resource
def load_model():
    model_files  = glob.glob('models/best_model_*.pkl')
    scaler_files = glob.glob('models/scaler.pkl')
    if not model_files or not scaler_files:
        return None, None, None
    model      = joblib.load(model_files[0])
    scaler     = joblib.load(scaler_files[0])
    model_name = (os.path.basename(model_files[0])
                  .replace('best_model_','').replace('.pkl','').replace('_',' '))
    return model, scaler, model_name

model, scaler, model_name = load_model()

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
STATE_MAP = {s:i for i,s in enumerate([
    'AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA',
    'HI','ID','IL','IN','IA','KS','KY','LA','ME','MD',
    'MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ',
    'NM','NY','NC','ND','OH','OK','OR','PA','RI','SC',
    'SD','TN','TX','UT','VT','VA','WA','WV','WI','WY'
])}
DAYS = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
CAT_RISK = {
    'shopping_net':'High','misc_net':'High','grocery_net':'Moderate',
    'travel':'Moderate','shopping_pos':'Moderate','misc_pos':'Moderate',
    'food_dining':'Low','gas_transport':'Low','health_fitness':'Low',
    'grocery_pos':'Low','entertainment':'Low','home':'Low',
    'kids_pets':'Low','personal_care':'Low',
}

def haversine(lat1,lon1,lat2,lon2):
    r=np.radians
    a=(np.sin((r(lat2)-r(lat1))/2)**2+np.cos(r(lat1))*np.cos(r(lat2))*np.sin((r(lon2)-r(lon1))/2)**2)
    return 6371*2*np.arcsin(np.sqrt(a))

def run_prediction(amt,category,hour,dayofweek,month,age,gender,city_pop,state,lat_n,lon_n,lat_m,lon_m,threshold):
    is_weekend=1 if dayofweek>=5 else 0
    is_night=1 if(hour>=22 or hour<=4) else 0
    dist=haversine(lat_n,lon_n,lat_m,lon_m)
    X=pd.DataFrame([{
        'amt':amt,'category_enc':CATEGORY_MAP.get(category,0),
        'hour':hour,'dayofweek':dayofweek,'month':month,
        'is_weekend':is_weekend,'is_night':is_night,
        'age':age,'gender':1 if gender=='Male' else 0,
        'city_pop':city_pop,'lat':lat_n,'long':lon_n,
        'merch_lat':lat_m,'merch_long':lon_m,
        'distance_km':dist,'state_enc':STATE_MAP.get(state,0),
    }])[FEATURE_COLS]
    prob=model.predict_proba(scaler.transform(X))[0][1]
    return prob,dist,is_night

def risk_factors(amt,hour,dist,age,is_night,category):
    f={}
    if amt>1000:    f['Transaction amount (high)']=+25
    elif amt>500:   f['Transaction amount (elevated)']=+12
    else:           f['Transaction amount (normal)']=-5
    if is_night:    f['Transaction time (off-hours)']=+20
    elif 9<=hour<=17:f['Transaction time (business hours)']=-8
    else:           f['Transaction time (evening)']=+5
    if dist>500:    f['Merchant distance (very far)']=+30
    elif dist>100:  f['Merchant distance (far)']=+14
    elif dist<20:   f['Merchant distance (local)']=-10
    else:           f['Merchant distance (normal)']=0
    if age>65:      f['Account holder age (senior)']=+10
    elif age<25:    f['Account holder age (young)']=+5
    else:           f['Account holder age (standard)']=-3
    HIGH=['shopping_net','misc_net','grocery_net']
    LOW=['gas_transport','food_dining','health_fitness','grocery_pos']
    if category in HIGH:   f[f'Merchant category ({category})']=+15
    elif category in LOW:  f[f'Merchant category ({category})']=-8
    else:                  f[f'Merchant category ({category})']=0
    return f


# ── Top Bar ──
st.markdown(f"""
<div class="topbar">
  <div class="topbar-brand">
    <div class="topbar-logo">
      <svg viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round">
        <path d="M12 2L3 7v5c0 5 4 9.27 9 10.93C17 21.27 21 17 21 12V7L12 2z"/>
      </svg>
    </div>
    <span class="topbar-name">Sentinel</span>
    <div class="topbar-divider"></div>
    <span class="topbar-subtitle">Fraud Risk Assessment</span>
  </div>
  <div class="topbar-right">
    <div class="topbar-badge">MODEL &nbsp;<span>{model_name.upper() if model_name else 'NOT LOADED'}</span></div>
    <div class="topbar-status"><div class="pulse"></div>OPERATIONAL</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── Layout ──
left_col, right_col = st.columns([5, 7])

with left_col:
    # Load Examples
    st.markdown('<div class="sec-label">Load Example</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    if c1.button("Normal Transaction"):
        st.session_state.update({
            'amt':47.80,'cat':'food_dining','hour':13,'dow':1,'month':6,
            'age':38,'gender':'Female','city_pop':480000,'state':'CA',
            'lat_n':33.96,'lon_n':-80.93,'lat_m':34.00,'lon_m':-80.97,
        })
    if c2.button("Flagged Transaction"):
        st.session_state.update({
            'amt':1875.00,'cat':'shopping_net','hour':2,'dow':6,'month':11,
            'age':71,'gender':'Male','city_pop':1400,'state':'NY',
            'lat_n':33.96,'lon_n':-80.93,'lat_m':40.71,'lon_m':-74.00,
        })

    st.markdown('<div class="sp24"></div>', unsafe_allow_html=True)

    # Transaction
    st.markdown('<div class="sec-label">Transaction Details</div>', unsafe_allow_html=True)
    amt = st.number_input("Amount (USD)", 0.01, 99999.99,
                           float(st.session_state.get('amt',47.80)), step=1.0, format="%.2f")
    category = st.selectbox("Merchant Category", list(CATEGORY_MAP.keys()),
                             index=list(CATEGORY_MAP.keys()).index(st.session_state.get('cat','food_dining')))
    c1, c2 = st.columns(2)
    hour  = c1.number_input("Hour (0–23)", 0, 23, int(st.session_state.get('hour',13)))
    month = c2.number_input("Month (1–12)", 1, 12, int(st.session_state.get('month',6)))
    dayofweek = st.select_slider("Day of Week", options=list(range(7)),
                                  format_func=lambda x: DAYS[x],
                                  value=int(st.session_state.get('dow',1)))

    st.markdown('<div class="sp16"></div>', unsafe_allow_html=True)

    # Account
    st.markdown('<div class="sec-label">Account Information</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    age    = c1.number_input("Age", 18, 100, int(st.session_state.get('age',38)))
    gender = c2.radio("Gender", ['Male','Female'], horizontal=True,
                       index=0 if st.session_state.get('gender','Female')=='Male' else 1)
    c1, c2 = st.columns(2)
    city_pop = c1.number_input("City Population", 100, 9999999,
                                int(st.session_state.get('city_pop',480000)), step=1000)
    state = c2.selectbox("State", list(STATE_MAP.keys()),
                          index=list(STATE_MAP.keys()).index(st.session_state.get('state','CA')))

    st.markdown('<div class="sp16"></div>', unsafe_allow_html=True)

    # Coordinates
    st.markdown('<div class="sec-label">Coordinates</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    lat_n = c1.number_input("Cardholder Lat",  value=float(st.session_state.get('lat_n',33.9659)), format="%.4f")
    lon_n = c2.number_input("Cardholder Long", value=float(st.session_state.get('lon_n',-80.9355)), format="%.4f")
    c1, c2 = st.columns(2)
    lat_m = c1.number_input("Merchant Lat",    value=float(st.session_state.get('lat_m',34.00)), format="%.4f")
    lon_m = c2.number_input("Merchant Long",   value=float(st.session_state.get('lon_m',-80.97)), format="%.4f")

    st.markdown('<div class="sp16"></div>', unsafe_allow_html=True)

    with st.expander("Detection Sensitivity"):
        threshold = st.slider("Fraud Threshold (%)", 10, 90, 50, 5,
                               help="Lower = more sensitive, higher = fewer alerts.")
        st.caption(f"Transactions above {threshold}% probability are flagged as fraud.")

    st.markdown('<div class="sp24"></div>', unsafe_allow_html=True)
    run_btn = st.button("Run Assessment")


# ── Results ──
with right_col:
    if run_btn:
        if model is None:
            st.error("Model files not found. Upload best_model_*.pkl and scaler.pkl to the models/ folder in your GitHub repository.")
        else:
            prob, dist, is_night = run_prediction(
                amt, category, hour, dayofweek, month,
                age, gender, city_pop, state,
                lat_n, lon_n, lat_m, lon_m, threshold
            )
            pct = round(prob * 100, 1)
            st.session_state['result'] = {
                'prob':prob,'pct':pct,'dist':dist,'is_night':is_night,
                'amt':amt,'category':category,'hour':hour,'dayofweek':dayofweek,
                'month':month,'age':age,'gender':gender,'city_pop':city_pop,
                'state':state,'threshold':threshold,
            }

    r = st.session_state.get('result')

    if r is None:
        st.markdown("""
        <div class="placeholder-wrap">
          <div class="placeholder-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none"
                 stroke="#4B5563" stroke-width="1.8" stroke-linecap="round">
              <path d="M12 2L3 7v5c0 5 4 9.27 9 10.93C17 21.27 21 17 21 12V7L12 2z"/>
            </svg>
          </div>
          <div class="placeholder-title">No assessment loaded</div>
          <div class="placeholder-sub">Complete the form and run an assessment</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        pct       = r['pct']
        threshold = r['threshold']

        if pct < 30:
            cls='safe';    headline='Low Risk';                 chip='Approved'
            desc=f"Fraud probability of {pct}% is well below the {threshold}% threshold. No anomalous patterns detected."
            mc='#10B981'; mf='linear-gradient(90deg,#D1FAE5,#10B981)'
            rec_text="Transaction presents no significant fraud indicators. Standard processing is appropriate. Continue routine monitoring."
        elif pct < 60:
            cls='caution'; headline='Elevated Risk';            chip='Review Required'
            desc=f"Fraud probability of {pct}% warrants closer review before the {threshold}% threshold is reached."
            mc='#F59E0B'; mf='linear-gradient(90deg,#FEF3C7,#F59E0B)'
            rec_text="Transaction exhibits moderate risk signals. Consider requesting secondary authentication or cardholder verification before approval."
        else:
            cls='fraud';   headline='High Risk — Fraud Indicated'; chip='Block Transaction'
            desc=f"Fraud probability of {pct}% exceeds the {threshold}% threshold. Immediate action recommended."
            mc='#EF4444'; mf='linear-gradient(90deg,#FEE2E2,#EF4444)'
            rec_text="Transaction probability exceeds the fraud threshold. Block transaction, issue a real-time alert to the cardholder, and escalate to the fraud operations team."

        # Verdict Card
        st.markdown(f"""
        <div class="verdict-card {cls}">
          <div class="verdict-eyebrow">Risk Verdict</div>
          <div class="verdict-headline {cls}">{headline}</div>
          <div class="verdict-desc">{desc}</div>
          <div class="verdict-chip {cls}">
            <svg width="10" height="10" viewBox="0 0 24 24" fill="none"
                 stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
              <path d="M12 2L3 7v5c0 5 4 9.27 9 10.93C17 21.27 21 17 21 12V7L12 2z"/>
            </svg>
            {chip}
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Stats row
        is_night_label = "Yes" if r['is_night'] else "No"
        st.markdown(f"""
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-label">Transaction Amount</div>
            <div class="stat-value">${r['amt']:,.2f}</div>
            <div class="stat-sub">{r['category'].replace('_',' ').title()}</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Merchant Distance</div>
            <div class="stat-value">{r['dist']:.0f} km</div>
            <div class="stat-sub">{CAT_RISK.get(r['category'],'—')} risk category</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Transaction Time</div>
            <div class="stat-value">{r['hour']:02d}:00</div>
            <div class="stat-sub">Off-hours: {is_night_label} — {DAYS[r['dayofweek']]}</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Account Holder</div>
            <div class="stat-value">{r['age']} yrs</div>
            <div class="stat-sub">{r['gender']} — {r['state']}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Risk Meter
        st.markdown(f"""
        <div class="meter-card">
          <div class="meter-header">
            <div>
              <div class="meter-title">Fraud Probability Score</div>
            </div>
            <div class="meter-pct" style="color:{mc}">{pct}%</div>
          </div>
          <div class="meter-track">
            <div class="meter-fill" style="width:{pct}%;background:{mf};"></div>
            <div style="position:absolute;left:{threshold}%;top:0;width:2px;height:100%;
                        background:#6B7280;opacity:.4;"></div>
          </div>
          <div class="meter-zones">
            <div class="meter-zone-s"></div>
            <div class="meter-zone-m"></div>
            <div class="meter-zone-h"></div>
          </div>
          <div class="meter-scale">
            <span>0%</span><span>Low</span>
            <span style="color:#9CA3AF">Threshold: {threshold}%</span>
            <span>High</span><span>100%</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Detail tables
        d1, d2 = st.columns(2)
        with d1:
            st.markdown(f"""
            <div class="dt-wrap">
              <div class="dt-head">Transaction</div>
              <table class="data-table">
                <tr><td>Amount</td><td>${r['amt']:,.2f}</td></tr>
                <tr><td>Category</td><td>{r['category'].replace('_',' ').title()}</td></tr>
                <tr><td>Category Risk</td><td>{CAT_RISK.get(r['category'],'—')}</td></tr>
                <tr><td>Hour</td><td>{r['hour']:02d}:00</td></tr>
                <tr><td>Day</td><td>{DAYS[r['dayofweek']]}</td></tr>
                <tr><td>Off-Hours</td><td>{'Yes' if r['is_night'] else 'No'}</td></tr>
              </table>
            </div>""", unsafe_allow_html=True)
        with d2:
            st.markdown(f"""
            <div class="dt-wrap">
              <div class="dt-head">Account &amp; Location</div>
              <table class="data-table">
                <tr><td>Age</td><td>{r['age']} yrs</td></tr>
                <tr><td>Gender</td><td>{r['gender']}</td></tr>
                <tr><td>State</td><td>{r['state']}</td></tr>
                <tr><td>City Pop.</td><td>{r['city_pop']:,}</td></tr>
                <tr><td>Distance</td><td>{r['dist']:.1f} km</td></tr>
                <tr><td>Month</td><td>{r['month']}</td></tr>
              </table>
            </div>""", unsafe_allow_html=True)

        # Factor Breakdown
        factors = risk_factors(r['amt'],r['hour'],r['dist'],r['age'],r['is_night'],r['category'])
        max_abs = max(abs(v) for v in factors.values()) if factors else 1

        st.markdown('<div class="factor-wrap"><div class="factor-head">Risk Factor Breakdown</div>', unsafe_allow_html=True)
        for name, score in sorted(factors.items(), key=lambda x: -abs(x[1])):
            bar_pct = int(abs(score)/max_abs*100)
            dot_c   = "#EF4444" if score > 0 else "#10B981"
            bar_c   = "#EF4444" if score > 0 else "#10B981"
            cls2    = "f-pos" if score > 0 else "f-neg"
            sign    = "+" if score > 0 else ""
            st.markdown(f"""
            <div class="factor-row">
              <div class="factor-dot" style="background:{dot_c}"></div>
              <span class="factor-name">{name}</span>
              <div class="factor-bar-track">
                <div class="factor-bar-fill" style="width:{bar_pct}%;background:{bar_c};"></div>
              </div>
              <span class="factor-score {cls2}">{sign}{score}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Recommendation
        st.markdown(f"""
        <div class="rec-card {cls}">
          <div class="rec-card-label">{'Immediate Action Required' if cls=='fraud' else 'Recommended Action'}</div>
          <div class="rec-card-text">{rec_text}</div>
        </div>""", unsafe_allow_html=True)
