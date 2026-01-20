import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
import os


def run_aadhaar_intelligence_model():
    """
    UIDAI Data Hackathon 2026: Predictive Anomaly Engine
    Precision Engineering for High-Fidelity Demographic Analysis
    """
    print("\n" + "=" * 60)
    print("🚀 STARTING AADHAAR PREDICTIVE INTELLIGENCE ENGINE")
    print("=" * 60)

    # --- 1. DATA LOADING (Updated File Paths) ---
    files = [
        "api_data_aadhar_demographic/api_data_aadhar_demographic_0_500000.csv",
        "api_data_aadhar_demographic/api_data_aadhar_demographic_500000_1000000.csv",
        "api_data_aadhar_demographic/api_data_aadhar_demographic_1000000_1500000.csv",
        "api_data_aadhar_demographic/api_data_aadhar_demographic_1500000_2000000.csv",
        "api_data_aadhar_demographic/api_data_aadhar_demographic_2000000_2071700.csv",
    ]

    raw_data = []
    for f in files:
        if os.path.exists(f):
            print(f"📦 Ingesting: {f}...")
            raw_data.append(pd.read_csv(f))
        else:
            print(f"⚠️ Warning: File not found at {f}")

    if not raw_data:
        print("❌ Error: Demographic source files not found. Check your file paths.")
        return

    df = pd.concat(raw_data, ignore_index=True)
    print(f"✅ Dataset Loaded: {len(df):,} administrative records.")

    # --- 2. HIGH-FIDELITY PREPROCESSING ---
    print("\n🛠️  Executing Fixation Pipeline & Feature Engineering...")

    # Standardize Date
    df["date"] = pd.to_datetime(df["date"], dayfirst=True)

    # MANDATORY KPI CREATION: Resolves potential KeyErrors
    # total_enrolments = age_5_17 (Students) + age_17_ (Adults)
    df["total_enrolments"] = df["demo_age_5_17"] + df["demo_age_17_"]

    # Categorical Signal Encoding: Converting States/Districts into numeric vectors
    # This creates the 'Administrative Signal' the ML model learns from.
    le_state = LabelEncoder()
    le_dist = LabelEncoder()
    df["state_id"] = le_state.fit_transform(df["state"].astype(str))
    df["dist_id"] = le_dist.fit_transform(df["district"].astype(str))

    # Temporal Signals: Day of the week and month are vital for surge detection.
    df["day_of_week"] = df["date"].dt.dayofweek
    df["month_num"] = df["date"].dt.month

    # --- 3. ML FEATURE AGGREGATION ---
    print("🧠 Aggregating Features for Anomaly Detection...")

    ml_df = (
        df.groupby(["date", "state", "state_id"])
        .agg(
            {
                "total_enrolments": "sum",
                "demo_age_5_17": "sum",
                "demo_age_17_": "sum",
                "day_of_week": "first",
                "month_num": "first",
            }
        )
        .reset_index()
    )

    # --- 4. MODEL TRAINING: ISOLATION FOREST ---
    print("📊 Training Isolation Forest (Unsupervised ML Outlier Detection)...")

    # The model identifies anomalies by isolating 'Flash Drives' in the data stream.
    model = IsolationForest(
        n_estimators=200,
        contamination=0.04,  # Target top 4% of statistical anomalies
        random_state=42,
    )

    features = [
        "state_id",
        "total_enrolments",
        "demo_age_5_17",
        "demo_age_17_",
        "day_of_week",
    ]
    ml_df["anomaly_signal"] = model.fit_predict(ml_df[features])

    # -1 = Anomaly (Statistical Outlier), 1 = Normal Operating Pulse
    anomalies = ml_df[ml_df["anomaly_signal"] == -1]

    # --- 5. PREDICTIVE ALERT SYSTEM (Z-SCORE LOGIC) ---
    print("📡 Calibrating Predictive Alert Thresholds...")

    national_pulse = ml_df.groupby("date")["total_enrolments"].sum().reset_index()
    national_pulse["rolling_avg"] = (
        national_pulse["total_enrolments"].rolling(window=14).mean()
    )
    national_pulse["rolling_std"] = (
        national_pulse["total_enrolments"].rolling(window=14).std()
    )

    # Alert Level = Mean + 2.5 Standard Deviations (Predictive Surge Threshold)
    national_pulse["alert_threshold"] = national_pulse["rolling_avg"] + (
        2.5 * national_pulse["rolling_std"]
    )

    # --- 6. CLI SUMMARY REPORT ---
    print("\n" + "=" * 60)
    print("📈 FINAL ML AUDIT REPORT")
    print("=" * 60)
    print(f"✅ Total Processed Volume : {df['total_enrolments'].sum():,}")
    print(f"🚨 Anomalies Detected     : {len(anomalies)} regional spikes")
    print(f"🎯 State with most Spikes : {anomalies['state'].value_counts().idxmax()}")
    print(
        f"⚠️  Predictive Alert Level : {int(national_pulse['alert_threshold'].iloc[-1]):,} units/day"
    )
    print("=" * 60)

    # Visualization Dashboard
    plt.figure(figsize=(14, 7))
    plt.plot(
        national_pulse["date"],
        national_pulse["total_enrolments"],
        label="Actual Daily Volume",
        alpha=0.5,
        color="blue",
    )
    plt.plot(
        national_pulse["date"],
        national_pulse["alert_threshold"],
        "--",
        label="Predictive Surge Threshold (Alert Level)",
        color="orange",
    )

    # Overlay ML-detected regional anomalies on the national trend
    plt.scatter(
        anomalies["date"],
        anomalies["total_enrolments"],
        color="red",
        marker="x",
        label="ML Flagged Anomaly (Flash Drive)",
    )

    plt.title(
        "Aadhaar Intelligence: Predictive Anomaly & Operational Pulse Dashboard",
        fontsize=15,
    )
    plt.xlabel("Timeline (2025)")
    plt.ylabel("Total Enrolment Activity")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    run_aadhaar_intelligence_model()
