from flask import Flask, request, jsonify
import os
import pandas as pd
import json
from anomaly_utils import (
    load_data, validate_schema, preprocess_data,
    detect_all_anomalies, score_anomalies, make_json_serializable
)

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return "Anomaly Detection API is running."

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'schema' not in request.form:
        return jsonify({'error': 'CSV file and schema are required.'}), 400

    file = request.files['file']
    schema_json = request.form['schema']
    schema = json.loads(schema_json)

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Load and preprocess data
    df = load_data(file_path)
    anomalies_schema = validate_schema(df, schema)
    df = preprocess_data(df)

    # Detect anomalies
    rule_stat_anoms, iso_anoms, lstm_anoms = detect_all_anomalies(df)

    # Score anomalies
    scored_anomalies = score_anomalies(rule_stat_anoms, iso_anoms, lstm_anoms, df)

    return jsonify(make_json_serializable({
        'schema_violations': anomalies_schema,
        'scored_anomalies': scored_anomalies
    }))

if __name__ == '__main__':
    app.run(debug=True)
