import pandas as pd
import numpy as np
from datetime import datetime


def load_data(file_path):
    """Load CSV data with low_memory=False to handle mixed types."""
    df = pd.read_csv(file_path, low_memory=False)
    print(f"Data loaded successfully from {file_path}. Shape: {df.shape}")
    return df


def validate_schema(df, schema):
    """Validate data against schema constraints."""
    anomalies = []

    # Ensure schema is a list of dictionaries
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

        # Check for missing values
        if df[col_name].isnull().sum() > 0:
            anomalies.append({
                'column': col_name,
                'issue': 'Missing values',
                'count': df[col_name].isnull().sum(),
                'description': col_desc
            })

        # Type-specific checks
        if col_type == 'FLOAT' and col_name in df.columns:
            df[col_name] = pd.to_numeric(df[col_name], errors='coerce')
            if df[col_name].dtype not in [np.float64, np.float32]:
                anomalies.append({
                    'column': col_name,
                    'issue': 'Invalid type (expected FLOAT)',
                    'description': col_desc
                })
            if df[col_name].min() < 0 and 'Price' in col_name:
                anomalies.append({
                    'column': col_name,
                    'issue': 'Negative price detected',
                    'count': (df[col_name] < 0).sum(),
                    'description': col_desc
                })
        elif col_type == 'TIMESTAMP' and col_name in df.columns:
            try:
                pd.to_datetime(df[col_name])
            except:
                anomalies.append({
                    'column': col_name,
                    'issue': 'Invalid timestamp format',
                    'description': col_desc
                })

    print(f"Schema validation completed. Found {len(anomalies)} anomalies.")
    return anomalies


def preprocess_data(df):
    """Clean and preprocess data."""
    # Convert timestamps
    time_cols = [col for col in df.columns if 'TIMESTAMP' in col.upper()]
    for col in time_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    # Fill missing numerical values with median
    num_cols = df.select_dtypes(include=[np.number]).columns
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())

    # Fill missing categorical values with 'Unknown'
    cat_cols = df.select_dtypes(include=['object']).columns
    df[cat_cols] = df[cat_cols].fillna('Unknown')

    print("Data preprocessing completed.")
    return df


if __name__ == "__main__":
    try:
        df = load_data("Data.csv")
        with open("Schema.json", "r") as f:
            schema = pd.read_json(f)

        anomalies = validate_schema(df, schema)
        df_cleaned = preprocess_data(df)

        print("Schema Validation Anomalies:", anomalies)
    except Exception as e:
        print(f"Error in preprocessing: {e}")