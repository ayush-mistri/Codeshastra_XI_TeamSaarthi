from langchain.prompts import PromptTemplate
import json
import pandas as pd
import numpy as np


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
    """Generate detailed explanation using Grok (simulated)."""
    schema_context = [s for s in schema if s['name'] == anomaly.get('column', anomaly.get('type', ''))]
    serializable_anomaly = make_json_serializable(anomaly)
    context = json.dumps(schema_context) + "\nAnomaly Details: " + json.dumps(serializable_anomaly)

    prompt = PromptTemplate(
        input_variables=["context"],
        template="Provide a detailed explanation of this anomaly, including line number, value, statistical context, and business impact:\n{context}"
    )

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