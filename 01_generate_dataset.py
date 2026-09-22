import numpy as np
import pandas as pd

np.random.seed(42)
n_samples = 10000

classes = ['Benign', 'DDoS', 'DoS', 'Mirai', 'Spoofing']
class_probs = [0.4, 0.2, 0.15, 0.15, 0.10]
labels = np.random.choice(classes, size=n_samples, p=class_probs)

data = []
for label in labels:
    if label == 'Benign':
        flow_duration = np.random.exponential(scale=5.0)
        tot_pkts = np.random.randint(1, 50)
        pkt_len_mean = np.random.normal(loc=200, scale=50)
        syn_flag_cnt = np.random.binomial(1, 0.1)
        rst_flag_cnt = np.random.binomial(1, 0.05)
    elif label == 'DDoS':
        flow_duration = np.random.exponential(scale=0.5)
        tot_pkts = np.random.randint(500, 5000)
        pkt_len_mean = np.random.normal(loc=64, scale=10)
        syn_flag_cnt = np.random.binomial(1, 0.9)
        rst_flag_cnt = 0
    elif label == 'DoS':
        flow_duration = np.random.exponential(scale=2.0)
        tot_pkts = np.random.randint(200, 1500)
        pkt_len_mean = np.random.normal(loc=500, scale=100)
        syn_flag_cnt = np.random.binomial(1, 0.8)
        rst_flag_cnt = 0
    elif label == 'Mirai':
        flow_duration = np.random.exponential(scale=0.1)
        tot_pkts = np.random.randint(10, 100)
        pkt_len_mean = np.random.normal(loc=128, scale=20)
        syn_flag_cnt = np.random.binomial(1, 0.95)
        rst_flag_cnt = np.random.binomial(1, 0.3)
    else:  # Spoofing
        flow_duration = np.random.exponential(scale=1.0)
        tot_pkts = np.random.randint(5, 30)
        pkt_len_mean = np.random.normal(loc=300, scale=80)
        syn_flag_cnt = np.random.binomial(1, 0.5)
        rst_flag_cnt = np.random.binomial(1, 0.4)

    flow_byts_s = (tot_pkts * max(10, pkt_len_mean)) / max(0.001, flow_duration)
    data.append([
        max(0.001, flow_duration), tot_pkts, max(10, pkt_len_mean),
        syn_flag_cnt, rst_flag_cnt, flow_byts_s, label
    ])

columns = [
    'flow_duration', 'tot_pkts', 'pkt_len_mean',
    'syn_flag_cnt', 'rst_flag_cnt', 'flow_byts_s', 'label'
]
df = pd.DataFrame(data, columns=columns)
df.to_csv('synthetic_iot_traffic.csv', index=False)
print("✅ Created synthetic_iot_traffic.csv with 10,000 samples!")
