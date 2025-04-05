import pandas as pd
from data_preprocessing import load_data, validate_schema, preprocess_data
from anomaly_detection import detect_all_anomalies
from severity_scoring import score_anomalies
from rag_pipeline import rag_explain_anomalies
from report_generation import generate_pdf_report


def process_data(file_path, schema_path):
    """Main function to process data and generate report."""
    df = load_data(file_path)
    with open(schema_path, "r") as f:
        schema = pd.read_json(f)
    print("Schema loaded successfully.")

    schema_anoms = validate_schema(df, schema)
    print("Schema anomalies:", schema_anoms)

    df_cleaned = preprocess_data(df)

    rule_stat_anoms, iso_anoms, lstm_anoms = detect_all_anomalies(df_cleaned)
    print(
        f"Rule/Stat anomalies: {len(rule_stat_anoms)}, Isolation Forest anomalies: {len(iso_anoms)}, LSTM anomalies: {len(lstm_anoms)}")

    scored_anoms = score_anomalies(rule_stat_anoms + schema_anoms, iso_anoms, lstm_anoms, df_cleaned)
    print("Scored anomalies sample:", scored_anoms[:5])

    explained_anoms = rag_explain_anomalies(scored_anoms, schema, df_cleaned)
    print("Explained anomalies sample:", explained_anoms[:5])

    generate_pdf_report(explained_anoms)

    print(f"Process completed. Total anomalies detected and reported: {len(explained_anoms)}")
    return explained_anoms


if __name__ == "__main__":
    try:
        anomalies = process_data("Data.csv", "Schema.json")
        print("Execution completed successfully.")
    except Exception as e:
        print(f"Error in main execution: {e}")