import joblib
import numpy as np
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="IoT Intrusion Detection System",
    page_icon="🛡️",
    layout="wide"
)

# Load Model
@st.cache_resource
def load_model():
    return joblib.load("ids_model.pkl")

model = load_model()

# Header
st.title("🛡️ IoT Network Intrusion Detection Dashboard")
st.markdown("""
This system analyzes real-time network flow statistics to detect anomalies and classify network attacks across **5 classes**:
`Benign`, `DDoS`, `DoS`, `Mirai Botnet`, and `Spoofing`.
""")

st.divider()

# Sidebar: Flow Parameter Inputs
st.sidebar.header("⚙️ Flow Parameter Controls")

flow_duration = st.sidebar.number_input("Flow Duration (seconds)", min_value=0.001, max_value=20.0, value=0.5, step=0.1)
tot_pkts = st.sidebar.slider("Total Packets Sent", min_value=1, max_value=5000, value=150)
pkt_len_mean = st.sidebar.slider("Mean Packet Length (Bytes)", min_value=10.0, max_value=1500.0, value=250.0)
syn_flag_cnt = st.sidebar.selectbox("SYN Flag Present (1 = Yes, 0 = No)", [0, 1], index=0)
rst_flag_cnt = st.sidebar.selectbox("RST Flag Present (1 = Yes, 0 = No)", [0, 1], index=0)

# Calculated Metric
flow_byts_s = (tot_pkts * pkt_len_mean) / max(0.001, flow_duration)

st.sidebar.metric("Calculated Flow Bytes/sec", f"{flow_byts_s:,.2f} B/s")

# Main Layout: 2 Columns
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 Flow Input Summary")
    input_data = pd.DataFrame({
        "Metric": ["Flow Duration", "Total Packets", "Mean Packet Length", "SYN Flag", "RST Flag", "Throughput (B/s)"],
        "Value": [f"{flow_duration:.3f} s", tot_pkts, f"{pkt_len_mean:.1f} B", syn_flag_cnt, rst_flag_cnt, f"{flow_byts_s:,.1f}"]
    })
    st.table(input_data)

with col2:
    st.subheader("🔎 Live Inference & Threat Assessment")

    if st.button("🚀 Analyze Traffic Flow", type="primary", use_container_width=True):
        features = np.array([[
            flow_duration, tot_pkts, pkt_len_mean,
            syn_flag_cnt, rst_flag_cnt, flow_byts_s
        ]])

        prediction = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]
        confidence = np.max(probabilities)

        st.write("---")

        if prediction == "Benign":
            st.success(f"### ✅ Normal Activity Detected (`{prediction}`)")
            st.info(f"Model Confidence: **{confidence:.2%}**")
        else:
            st.error(f"### 🚨 THREAT ALERT: `{prediction}` Attack Identified!")
            st.warning(f"Confidence Score: **{confidence:.2%}**")

        # Probability Breakdown Chart
        st.markdown("#### Prediction Probability Distribution")
        classes = model.classes_
        prob_df = pd.DataFrame({
            "Attack Category": classes,
            "Probability": probabilities
        }).sort_values(by="Probability", ascending=False)

        st.bar_chart(prob_df.set_index("Attack Category"))
