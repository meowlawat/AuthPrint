import streamlit as st
import numpy as np
from data import USERS
from engine import get_stylometry, get_fingerprint_similarity, evaluate_anomaly

# ==========================================
# UI CONFIG & AESTHETICS (PASTEL THEME)
# ==========================================
# ==========================================
# UI CONFIG & AESTHETICS (GREEN FINTECH THEME)
# ==========================================
st.set_page_config(page_title="AuthPrint Engine", layout="wide", initial_sidebar_state="expanded")

# Inject Custom CSS for Premium Green SaaS Look
st.markdown("""
<style>
    /* Main background - Soft mint/off-white */
    .stApp {
        background-color: #f4f9f5;
    }
    /* Sidebar background - Soft sage green */
    [data-testid="stSidebar"] {
        background-color: #e6efe9;
        border-right: 1px solid #d1e0d7;
    }
    /* Typography adjustments - Dark forest green for contrast */
    h1, h2, h3, p, label {
        color: #2a3d33 !important;
        font-family: 'Inter', sans-serif;
    }
    /* Style the main submit button - Solid Sage */
    .stButton>button {
        background-color: #9abfa9 !important; 
        color: #1a2920 !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 24px !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #84a893 !important;
        transform: translateY(-2px);
    }
    
    /* Metric Cards */
    [data-testid="stMetricValue"] {
        color: #3b5747;
    }
    /* Make the established fingerprint boxes match the green theme */
    div[data-testid="stAlert"] {
        background-color: #dbe8df !important;
        color: #2a3d33 !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# MAIN APP LAYOUT
# ==========================================
st.title("✨ AuthPrint")
st.markdown("*Identity Mismatch Engine for First Dollar Moderation*")
st.markdown("---")

# Sidebar
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/6596/6596121.png", width=50) # Small aesthetic icon
st.sidebar.title("1. Target Profile")
selected_user = st.sidebar.selectbox("Select Baseline Identity:", list(USERS.keys()))
history = USERS[selected_user]

st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.subheader("Established Fingerprint")
for tweet in history:
    st.sidebar.info(f"📝 {tweet}") # Added emojis for better visual breaking

# Main Content
st.subheader("2. Analyze New Submission")
new_tweet = st.text_area("Paste the new First Dollar bounty submission below:", height=150, placeholder="e.g., Just found out about this amazing new tool...")

if st.button("Run Identity Check"):
    if not new_tweet.strip():
        st.warning("⚠️ Please paste a submission to analyze.")
    else:
        with st.spinner("Analyzing stylometric variance and N-Gram footprints..."):
            # Calculate metrics
            hist_stats_list = [get_stylometry(t) for t in history]
            avg_hist_stats = {
                "avg_word_len": round(np.mean([s["avg_word_len"] for s in hist_stats_list]), 2),
                "punct_ratio": round(np.mean([s["punct_ratio"] for s in hist_stats_list]), 3),
                "upper_ratio": round(np.mean([s["upper_ratio"] for s in hist_stats_list]), 3)
            }
            new_stats = get_stylometry(new_tweet)
            sim_score = get_fingerprint_similarity(history, new_tweet)
            
            # Engine verdict
            verdict = evaluate_anomaly(avg_hist_stats, new_stats, sim_score)
            
            st.markdown("### Analysis Results")
            st.markdown("---")
            
            # Metrics Row
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="N-Gram Match", value=f"{sim_score} / 1.0")
            with col2:
                st.metric(label="Stylometry", value="Deviated" if abs(sim_score) < 0.4 else "Stable")
            with col3:
                st.metric(label="Anomaly Score", value=f"{verdict.get('anomaly_score', 0)} / 100")
            
            # Verdict Box
            st.markdown("<br>", unsafe_allow_html=True)
            if verdict.get("flagged"):
                st.error("🚨 **FLAG: IDENTITY MISMATCH DETECTED**")
            else:
                st.success("✅ **PASS: BEHAVIORAL FINGERPRINT MATCHES**")
                
            st.caption(f"**Diagnostic Details:** {verdict.get('reasoning', '')}")