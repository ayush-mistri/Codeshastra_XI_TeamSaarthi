import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from scipy.stats import zscore
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense


def preprocess_for_anomaly(df):
    """Preprocess timestamp columns to ensure they are in datetime format."""
    time_cols = [col for col in df.columns if 'TIMESTAMP' in col.upper()]
    for col in time_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    print("Timestamp preprocessing for anomaly detection completed.")
    return df


def rule_based_anomalies(df):
    """Detect anomalies using predefined rules."""
    anomalies = []

    for col in ['Sub_Total', 'Final_Total', 'Price']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            if (df[col] < 0).any():
                anomalies.append({
                    'type': 'Rule-Based',
                    'column': col,
                    'issue': 'Negative value',
                    'count': (df[col] < 0).sum()
                })

    current_date = pd.to_datetime("2025-04-05")
    for col in df.columns:
        if 'TIMESTAMP' in col.upper():
            if df[col].dtype == 'datetime64[ns]' and (df[col] > current_date).any():
                anomalies.append({
                    'type': 'Rule-Based',
                    'column': col,
                    'issue': 'Future timestamp',
                    'count': (df[col] > current_date).sum()
                })

    print(f"Rule-based anomaly detection completed. Found {len(anomalies)} anomalies.")
    return anomalies


def statistical_anomalies(df):
    """Detect anomalies using statistical methods."""
    anomalies = []
    num_cols = ['Price', 'Qty_', 'Sub_Total', 'Final_Total', 'Tax']

    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            z_scores = zscore(df[col].fillna(df[col].median()))
            outliers = df[np.abs(z_scores) > 3]
            if not outliers.empty:
                anomalies.append({
                    'type': 'Statistical',
                    'column': col,
                    'issue': 'Outlier (z-score > 3)',
                    'count': len(outliers)
                })

    print(f"Statistical anomaly detection completed. Found {len(anomalies)} anomalies.")
    return anomalies


def isolation_forest_anomalies(df):
    """Detect anomalies using Isolation Forest."""
    num_cols = ['Price', 'Qty_', 'Sub_Total', 'Final_Total', 'Tax']
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    X = df[num_cols].fillna(0)

    model = IsolationForest(contamination=0.005, random_state=42)  # Reduced to 0.5% for precision
    preds = model.fit_predict(X)

    anomalies = df[preds == -1].copy()
    anomalies['type'] = 'Isolation Forest'
    anomalies['issue'] = 'Unusual pattern'

    print(f"Isolation Forest anomaly detection completed. Found {len(anomalies)} anomalies.")
    return anomalies


def lstm_anomalies(df):
    """Detect time-series anomalies using LSTM."""
    time_cols = ['Timestamp']
    num_cols = ['Final_Total']
    df['Final_Total'] = pd.to_numeric(df['Final_Total'], errors='coerce')
    df_time = df[time_cols + num_cols].sort_values('Timestamp').dropna()

    X = df_time['Final_Total'].values.reshape(-1, 1, 1)
    model = Sequential([
        LSTM(20, activation='relu', input_shape=(1, 1)),  # Reduced units for speed
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    model.fit(X[:-1], X[1:], epochs=1, batch_size=64, verbose=0)  # Single epoch, larger batch

    preds = model.predict(X[:-1], verbose=0)
    errors = np.abs(preds.flatten() - X[1:].flatten())
    threshold = np.percentile(errors, 99)  # Very strict threshold

    anomalies = df_time.iloc[1:][errors > threshold].copy()
    anomalies['type'] = 'LSTM'
    anomalies['issue'] = 'Temporal anomaly'

    print(f"LSTM anomaly detection completed. Found {len(anomalies)} anomalies.")
    return anomalies


def detect_all_anomalies(df):
    """Combine all anomaly detection methods."""
    df = preprocess_for_anomaly(df)
    rule_anoms = rule_based_anomalies(df)
    stat_anoms = statistical_anomalies(df)
    iso_anoms = isolation_forest_anomalies(df)
    lstm_anoms = lstm_anomalies(df)

    print("All anomaly detection methods completed.")
    return rule_anoms + stat_anoms, iso_anoms, lstm_anoms