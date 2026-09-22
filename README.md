# 🛡️ Machine Learning-Based IoT Network Intrusion Detection System (NIDS)

An end-to-end cybersecurity project featuring a synthetic network traffic engine, a multi-class Random Forest classifier, and an interactive Streamlit Security Operations Center (SOC) dashboard.

---

## 📌 Executive Summary

Internet of Things (IoT) ecosystems are uniquely vulnerable to automated botnet recruitment, volumetric Denial of Service (DoS), and packet spoofing due to hardware constraints and default credential proliferation. Traditional signature-based detection systems often fail against novel zero-day vectors or encrypted flow metadata.

This project implements a **behavioral anomaly detection system** trained on network flow metadata. By analyzing non-payload features—such as TCP control flags, packet length distributions, and byte throughput—the system classifies real-time network traffic into **five distinct threat vectors**:

1. **Benign:** Normal, expected IoT device telemetry and background traffic.
2. **DDoS (Distributed Denial of Service):** High-volumetric, distributed flood traffic.
3. **DoS (Denial of Service):** Single-source resource exhaustion attacks.
4. **Mirai Botnet:** Automated port scanning and exploitation sweeps.
5. **IP/Header Spoofing:** Low-volume, forged packet headers attempting access control evasion.

---

## 🏗️ System Architecture

```
[ Synthetic Flow Generator ]
             │
             ▼
[ Traffic Metadata CSV ] ──► [ Model Training Pipeline ]
                                       │
                                       ▼
                             [ Trained Model Artifact (.pkl) ]
                                       │
                                       ▼
                            [ Streamlit SOC Dashboard ] ◄── [ Security Analyst Input ]
```

### Component Breakdown

* **`01_generate_dataset.py` (Traffic Generator):** Simulates 10,000 traffic flows adhering to stochastic distributions derived from real-world network protocol behavior.
* **`02_train_models.py` (ML Pipeline):** Splits data into 80/20 train/test sets, trains a Random Forest Classifier, and evaluates performance across Precision, Recall, and F1-score.
* **`app.py` (Streamlit Dashboard):** Interactive analyst UI with input sliders, real-time threat detection, and classification probability distribution charts.

---

## 📊 Dataset & Feature Engineering

Because raw payload inspection (Deep Packet Inspection) is computationally expensive and ineffective against encrypted channels, this system operates strictly on **Layer 3 / Layer 4 flow metadata**:

| Feature Name | Description | Threat Relevance |
| :--- | :--- | :--- |
| `flow_duration` | Total duration of the TCP/UDP flow (seconds) | Distinguishes short-lived scans (Mirai) from sustained streams. |
| `tot_pkts` | Total packet count in the flow | Identifies high-volume floods (DDoS/DoS). |
| `pkt_len_mean` | Average packet size (bytes) | Highlights small payload sweeps vs. large data transfers. |
| `syn_flag_cnt` | Binary count of TCP SYN initiation flags | Core indicator of TCP SYN flooding and port scans. |
| `rst_flag_cnt` | Binary count of TCP Connection Reset flags | Indicates closed port probes typical of botnet scanners. |
| `flow_byts_s` | Calculated throughput ($(\text{tot\_pkts} \times \text{pkt\_len\_mean}) / \text{flow\_duration}$) | Quantitative measure of network link saturation. |

---

## 📈 Model Performance & Results

The Random Forest Classifier was evaluated on a held-out test set of 2,000 flows ($20\%$ test split):

```text
--- Classification Report ---
              precision    recall  f1-score   support

      Benign       0.95      0.96      0.96       812
        DDoS       1.00      1.00      1.00       410
         DoS       1.00      1.00      1.00       296
       Mirai       0.99      0.99      0.99       290
    Spoofing       0.85      0.79      0.82       192

    accuracy                           0.96      2000
   macro avg       0.96      0.95      0.95      2000
weighted avg       0.96      0.96      0.96      2000
```

### Analytical Takeaways
* **Volumetric Attacks (DDoS/DoS):** Achieved **1.00 F1-score**. High throughput and uniform packet structures make volumetric floods statistically unmistakable.
* **Botnet Scans (Mirai):** Achieved **0.99 F1-score**. Rapid connection bursts coupled with elevated `SYN`/`RST` flag ratios provide a clean signature boundary.
* **Spoofing vs. Benign:** Spoofing traffic shares lower-volume feature ranges with legitimate background traffic, resulting in an expected drop to **0.82 F1-score**. This reflects real-world decision boundary overlap where low-volume anomaly detection requires secondary evaluation.

---

## 🚀 Quickstart & Reproduction

### Prerequisites
* Python 3.10+
* Linux / macOS / WSL (Windows)

### 1. Clone & Setup Environment
```bash
git clone https://github.com/YOUR_USERNAME/iot-ids-ml.git
cd iot-ids-ml

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Generate Synthetic Dataset
```bash
python3 01_generate_dataset.py
```
*Outputs: `synthetic_iot_traffic.csv` (10,000 samples)*

### 3. Train Model Artifact
```bash
python3 02_train_models.py
```
*Outputs: `ids_model.pkl` (Serialized Random Forest model)*

### 4. Launch SOC Interactive Dashboard
```bash
streamlit run app.py
```
*Opens interactive UI in browser at `http://localhost:8501`*

---

## 🔬 Future Extensions

1. **PCAP Live Capture:** Integrate `scapy` or `tshark` to stream real live network interface traffic directly into the inference engine.
2. **Adversarial ML Robustness:** Test model degradation against perturbed feature inputs (e.g., packet padding or rate pacing designed to evade tree splits).
3. **Model Compression:** Quantize model trees or benchmark lightweight algorithms (e.g., XGBoost / LightGBM) for edge deployment on Raspberry Pi / ESP32 nodes.

---
```