import pandas as pd
import numpy as np


def calculate_severity(anomaly, df):
    """Assign severity score with balanced differentiation."""
    severity = 0

    if 'column' in anomaly:
        col = anomaly['column']
        count = anomaly.get('count', 1)
        if col in ['Final_Total', 'Sub_Total', 'Price']:
            severity += 25  # Base for revenue-related
            if 'Negative' in anomaly['issue']:
                severity += 40  # Critical for negative values
            elif 'Outlier' in anomaly['issue']:
                severity += 15
                if col in df.columns and not df[col].dropna().empty:
                    max_val = df[col].max()
                    median = df[col].median()
                    severity += min(15, (max_val / median - 1) * 3)  # Adjusted scaling
            severity += min(count / 200, 10)  # Further cap count impact
        elif col in ['Timestamp', 'Date']:
            severity += 20
            if 'Future' in anomaly['issue']:
                severity += 30
            severity += min(count / 300, 5)

    elif 'type' in anomaly and anomaly['type'] in ['Isolation Forest', 'LSTM']:
        severity += 20  # Base for AI-detected
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
            severity += min(time_diff / 60, 10)  # Reduced temporal impact

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