import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.ensemble import IsolationForest
from scipy.stats import zscore
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import json
import os

# Data Preprocessing Functions
def load_data(file_path):
    """Load CSV data with low_memory=False to handle mixed types."""
    df = pd.read_csv(file_path, low_memory=False)
    print(f"Data loaded successfully from {file_path}. Shape: {df.shape}")
    return df
def validate_schema(df, schema):
    """Validate data against schema constraints."""
    anomalies = []
    if isinstance(schema, pd.DataFrame):
        schema = schema.to_dict(orient='records')
    elif not isinstance(schema, list):
        raise ValueError("Schema must be a list of dictionaries or a DataFrame convertible to such.")

    for col in schema:
        col_name = col['name']
        col_type = col['type']
        col_desc = col['description']
        if col_name not in df.columns:
            continue
        if df[col_name].isnull().sum() > 0:
            anomalies.append({'column': col_name, 'issue': 'Missing values', 'count': df[col_name].isnull().sum(), 'description': col_desc})
        if col_type == 'FLOAT' and col_name in df.columns:
            df[col_name] = pd.to_numeric(df[col_name], errors='coerce')
            if df[col_name].dtype not in [np.float64, np.float32]:
                anomalies.append({'column': col_name, 'issue': 'Invalid type (expected FLOAT)', 'description': col_desc})
            if df[col_name].min() < 0 and 'Price' in col_name:
                anomalies.append({'column': col_name, 'issue': 'Negative price detected', 'count': (df[col_name] < 0).sum(), 'description': col_desc})
        elif col_type == 'TIMESTAMP' and col_name in df.columns:
            try:
                pd.to_datetime(df[col_name])
            except:
                anomalies.append({'column': col_name, 'issue': 'Invalid timestamp format', 'description': col_desc})
    print(f"Schema validation completed. Found {len(anomalies)} anomalies.")
    return anomalies

def preprocess_data(df):
    """Clean and preprocess data."""
    time_cols = [col for col in df.columns if 'TIMESTAMP' in col.upper()]
    for col in time_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    num_cols = df.select_dtypes(include=[np.number]).columns
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())
    cat_cols = df.select_dtypes(include=['object']).columns
    df[cat_cols] = df[cat_cols].fillna('Unknown')
    print("Data preprocessing completed.")
    return df

# Anomaly Detection Functions
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
                anomalies.append({'type': 'Rule-Based', 'column': col, 'issue': 'Negative value', 'count': (df[col] < 0).sum()})
    current_date = pd.to_datetime("2025-04-05")
    for col in df.columns:
        if 'TIMESTAMP' in col.upper():
            if df[col].dtype == 'datetime64[ns]' and (df[col] > current_date).any():
                anomalies.append({'type': 'Rule-Based', 'column': col, 'issue': 'Future timestamp', 'count': (df[col] > current_date).sum()})
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
                anomalies.append({'type': 'Statistical', 'column': col, 'issue': 'Outlier (z-score > 3)', 'count': len(outliers)})
    print(f"Statistical anomaly detection completed. Found {len(anomalies)} anomalies.")
    return anomalies

def isolation_forest_anomalies(df):
    """Detect anomalies using Isolation Forest."""
    num_cols = ['Price', 'Qty_', 'Sub_Total', 'Final_Total', 'Tax']
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    X = df[num_cols].fillna(0)
    model = IsolationForest(contamination=0.005, random_state=42)
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
    model = Sequential([LSTM(20, activation='relu', input_shape=(1, 1)), Dense(1)])
    model.compile(optimizer='adam', loss='mse')
    model.fit(X[:-1], X[1:], epochs=1, batch_size=64, verbose=0)
    preds = model.predict(X[:-1], verbose=0)
    errors = np.abs(preds.flatten() - X[1:].flatten())
    threshold = np.percentile(errors, 99)
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

# Severity Scoring Functions
def calculate_severity(anomaly, df):
    """Assign severity score with balanced differentiation."""
    severity = 0
    if 'column' in anomaly:
        col = anomaly['column']
        count = anomaly.get('count', 1)
        if col in ['Final_Total', 'Sub_Total', 'Price']:
            severity += 25
            if 'Negative' in anomaly['issue']:
                severity += 40
            elif 'Outlier' in anomaly['issue']:
                severity += 15
                if col in df.columns and not df[col].dropna().empty:
                    max_val = df[col].max()
                    median = df[col].median()
                    severity += min(15, (max_val / median - 1) * 3)
            severity += min(count / 200, 10)
        elif col in ['Timestamp', 'Date']:
            severity += 20
            if 'Future' in anomaly['issue']:
                severity += 30
            severity += min(count / 300, 5)
    elif 'type' in anomaly and anomaly['type'] in ['Isolation Forest', 'LSTM']:
        severity += 20
        if 'Final_Total' in anomaly:
            value = anomaly['Final_Total']
            median = df['Final_Total'].median()
            std = df['Final_Total'].std()
            if value > median + 3 * std:
                severity += 30
            elif value > median * 2:
                severity += 15
            elif value < median * 0.5:
                severity += 10
        if anomaly['type'] == 'LSTM':
            time_diff = (anomaly['Timestamp'] - df['Timestamp'].min()).days
            severity += min(time_diff / 60, 10)
    severity = min(severity, 100)
    print(f"Calculated severity for {anomaly.get('column', anomaly.get('type', 'N/A'))}: {severity}")
    return severity

def score_anomalies(rule_stat_anoms, iso_anoms, lstm_anoms, df):
    """Score all detected anomalies."""
    scored_anoms = []
    for anom in rule_stat_anoms:
        anom['severity'] = calculate_severity(anom, df)
        scored_anoms.append(anom)
    for idx, row in iso_anoms.iterrows():
        anom = row.to_dict()
        anom['line_number'] = idx
        anom['severity'] = calculate_severity(anom, df)
        scored_anoms.append(anom)
    for idx, row in lstm_anoms.iterrows():
        anom = row.to_dict()
        anom['line_number'] = idx
        anom['severity'] = calculate_severity(anom, df)
        scored_anoms.append(anom)
    scored_anoms = sorted(scored_anoms, key=lambda x: x['severity'], reverse=True)
    print(f"Severity scoring completed. Total anomalies scored: {len(scored_anoms)}")
    return scored_anoms

# RAG Pipeline Functions
def make_json_serializable(obj):
    """Convert non-JSON-serializable objects to serializable formats."""
    if isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif pd.isna(obj):
        return None
    elif isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_serializable(item) for item in obj]
    return obj

def generate_explanation(anomaly, schema, df):
    """Generate detailed explanation."""
    schema_context = [s for s in schema if s['name'] == anomaly.get('column', anomaly.get('type', ''))]
    col_or_type = anomaly.get('column', anomaly.get('type', 'N/A'))
    issue = anomaly['issue']
    line = anomaly.get('line_number', 'N/A')
    severity = anomaly['severity']
    if 'column' in anomaly:
        col = anomaly['column']
        count = anomaly.get('count', 1)
        if col in df.select_dtypes(include=[np.number]).columns and not df[col].dropna().empty:
            median = df[col].median()
            value = df[col].min() if 'Negative' in issue else df[col].max()
            explanation = f"Line {line}: {col} - {issue} (Count: {count}, Value: {value}, Median: {median:.2f}). " \
                          f"{'Negative values indicate revenue loss' if 'Negative' in issue else 'Outliers suggest unusual sales'}. " \
                          f"Impact: {'Critical' if severity > 75 else 'High' if severity > 50 else 'Moderate'} (Severity: {severity}). " \
                          f"Action: Validate data entry."
        else:
            explanation = f"Line {line}: {col} - {issue} (Count: {count}). Non-numeric or empty data detected. " \
                          f"Impact: {'Critical' if severity > 75 else 'High' if severity > 50 else 'Moderate'} (Severity: {severity}). " \
                          f"Action: Check data consistency."
    else:
        value = anomaly.get('Final_Total', 'N/A')
        if value != 'N/A' and not df['Final_Total'].dropna().empty:
            median = df['Final_Total'].median()
            std = df['Final_Total'].std()
            explanation = f"Line {line}: {col_or_type} - {issue} (Final_Total: {value}, Median: {median:.2f}, Std: {std:.2f}). " \
                          f"{'Extreme value' if abs(value - median) > 3 * std else 'Significant deviation'} in {col_or_type}. " \
                          f"Impact: {'Critical' if severity > 75 else 'High' if severity > 50 else 'Moderate'} (Severity: {severity}). " \
                          f"Action: Review order for fraud or error."
        else:
            explanation = f"Line {line}: {col_or_type} - {issue}. No valid numeric data available. " \
                          f"Impact: {'Critical' if severity > 75 else 'High' if severity > 50 else 'Moderate'} (Severity: {severity}). " \
                          f"Action: Investigate anomaly source."
    return explanation

def rag_explain_anomalies(anomalies, schema, df):
    """Add explanations to all anomalies."""
    if isinstance(schema, pd.DataFrame):
        schema = schema.to_dict(orient='records')
    for anom in anomalies:
        anom['explanation'] = generate_explanation(anom, schema, df)
    print(f"RAG explanations added to {len(anomalies)} anomalies.")
    return anomalies

# JSON Report Generation Function
def generate_json_report(anomalies, output_path="output/anomaly_report.json"):
    """Generate a JSON report of all anomalies."""
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # Prepare summary data
    total_anomalies = len(anomalies)
    type_counts = pd.Series([anom.get('type', 'Unknown') for anom in anomalies]).value_counts().to_dict()
    high_priority = sum(1 for a in anomalies if a.get('severity', 0) > 75)
    
    # Make anomalies JSON-serializable
    serializable_anomalies = [make_json_serializable(anom) for anom in anomalies]
    
    # Structure the report
    report = {
        "metadata": {
            "generated_on": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "total_anomalies": total_anomalies,
            "high_priority_count": high_priority,
            "anomaly_types": type_counts,
            "recommendation": "Prioritize high-severity anomalies for immediate action"
        },
        "anomalies": serializable_anomalies
    }
    
    # Write to JSON file
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=4)
    print(f"JSON report generated and saved to {output_path}")
    
    
    

# Main Processing Function
def process_data(file_path, schema_path):
    """Main function to process data and generate JSON report."""
    df = load_data(file_path)
    with open(schema_path, "r") as f:
        schema = pd.read_json(f)
    print("Schema loaded successfully.")
    schema_anoms = validate_schema(df, schema)
    print("Schema anomalies:", schema_anoms)
    df_cleaned = preprocess_data(df)
    rule_stat_anoms, iso_anoms, lstm_anoms = detect_all_anomalies(df_cleaned)
    print(f"Rule/Stat anomalies: {len(rule_stat_anoms)}, Isolation Forest anomalies: {len(iso_anoms)}, LSTM anomalies: {len(lstm_anoms)}")
    scored_anoms = score_anomalies(rule_stat_anoms + schema_anoms, iso_anoms, lstm_anoms, df_cleaned)
    print("Scored anomalies sample:", scored_anoms[:5])
    explained_anoms = rag_explain_anomalies(scored_anoms, schema, df_cleaned)
    print("Explained anomalies sample:", explained_anoms[:5])
    generate_json_report(explained_anoms)
    print(f"Process completed. Total anomalies detected and reported: {len(explained_anoms)}")
    return explained_anoms

import sys

if __name__ == "__main__":
    try:
        if len(sys.argv) != 3:
            raise ValueError("Usage: python anomaly_utils.py <file_path> <schema_path>")
        file_path = sys.argv[1]
        schema_path = sys.argv[2]
        anomalies = process_data(file_path, schema_path)
        print("Execution completed successfully.")
    except Exception as e:
        print(f"Error in main execution: {e}")
