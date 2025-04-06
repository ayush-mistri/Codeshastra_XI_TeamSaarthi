# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# import subprocess
# import threading
# from anomaly_utils import load_data, validate_schema, preprocess_data, detect_all_anomalies, score_anomalies
# from pymongo import MongoClient
# from datetime import datetime

# app = Flask(__name__)
# CORS(app, origins=["http://localhost:5173"])

# # MongoDB configuration
# client = MongoClient("mongodb://localhost:27017/")  # Change this to your connection string if hosted
# db = client["saarthiDB"]
# collection = db["Anamoly"]

# OUTPUT_FOLDER = 'output'
# OUTPUT_FILE = 'anomalies.json'
# app = Flask(__name__)

# # Allow CORS only from localhost:5173 (your frontend)
# CORS(app, origins=["http://localhost:5173"])

# # Define the upload folder and create it if it doesn't exist
# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # Endpoint to check if the API is running
# @app.route('/')
# def index():
#     return "Anomaly Detection API is running."

# def run_anomalies_script(file_path):
#     """Run anomalies.py script asynchronously after file upload."""
#     try:
#         # Assuming anomalies.py is in the same directory as app.py
#         command = ['python', 'anomaly_utils.py']
#         subprocess.run(command, check=True)
#         print(f"Anomalies detection completed for file: {file_path}")
#     except subprocess.CalledProcessError as e:
#         print(f"Error during anomaly detection: {str(e)}")

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     try:
#         # Ensure 'file' is included in the request
#         if 'file' not in request.files:
#             return jsonify({'error': 'CSV file is required.'}), 400  # Return error if no file is found

#         file = request.files['file']

#         # Check if file is selected
#         if file.filename == '':
#             return jsonify({'error': 'No file selected.'}), 400  # Return error if file is empty

#         # Save the file to the server
#         file_path = os.path.join(UPLOAD_FOLDER, file.filename)
#         file.save(file_path)

#         # Start anomaly detection in a separate thread (without blocking Flask app)
#         anomaly_thread = threading.Thread(target=run_anomalies_script, args=(file_path,))
#         anomaly_thread.start()

#         # Return the immediate success response
#         return jsonify({'message': 'File uploaded successfully. Anomaly detection is being processed in the background.'})

#     except Exception as e:
#         print(f"Error occurred: {str(e)}")
#         return jsonify({'error': 'Internal server error.'}), 500


# @app.route('/upload-to-mongo', methods=['POST'])
# def upload_to_mongodb():
#     try:
#         output_path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILE)

#         if not os.path.exists(output_path):
#             return jsonify({'error': 'Anomalies output file not found.'}), 404

#         # Load JSON content
#         with open(output_path, 'r') as f:
#             data = json.load(f)

#         # Optional: Add metadata like generated_on timestamp
#         metadata = {
#             "generated_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "total_anomalies": len(data.get("anomalies", [])),
#             "high_priority_count": sum(1 for a in data["anomalies"] if a.get("severity", 0) > 75),
#             "anomaly_types": {},  # To be computed
#             "recommendation": "Prioritize high-severity anomalies for immediate action"
#         }

#         # Count anomaly types
#         for a in data["anomalies"]:
#             a_type = a.get("type", "Unknown")
#             metadata["anomaly_types"][a_type] = metadata["anomaly_types"].get(a_type, 0) + 1

#         # Final structure
#         document = {
#             "metadata": metadata,
#             "anomalies": data["anomalies"]
#         }

#         # Insert into MongoDB
#         result = collection.insert_one(document)

#         return jsonify({
#             'message': 'Data uploaded to MongoDB successfully.',
#             'document_id': str(result.inserted_id)
#         })

#     except Exception as e:
#         print(f"Error uploading to MongoDB: {str(e)}")
#         return jsonify({'error': 'Internal server error.'}), 500


# if __name__ == '__main__':
#     app.run(debug=True, port=5001)

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import subprocess
import threading
import json
from datetime import datetime
from pymongo import MongoClient
import time

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

# MongoDB configuration
client = MongoClient("mongodb://localhost:27017/")
db = client["saarthiDB"]
collection = db["Anamoly"]

OUTPUT_FOLDER = 'output'
OUTPUT_FILE = 'anomaly_report.json'  # Match the filename from anomaly_utils.py
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return "Anomaly Detection API is running."

def run_anomalies_script(file_path):
    """Run anomalies.py script asynchronously after file upload."""
    try:
        schema_path = "./Schema.json"  # Adjust this path as needed
        command = ['python', 'anomaly_utils.py', file_path, schema_path]
        subprocess.run(command, check=True)
        print(f"Anomalies detection completed for file: {file_path}")
        upload_to_mongodb()
    except subprocess.CalledProcessError as e:
        print(f"Error during anomaly detection: {str(e)}")

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'CSV file is required.'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected.'}), 400
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        anomaly_thread = threading.Thread(target=run_anomalies_script, args=(file_path,))
        anomaly_thread.start()
        return jsonify({'message': 'File uploaded successfully. Anomaly detection is being processed in the background.'})
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({'error': 'Internal server error.'}), 500

def upload_to_mongodb():
    """Upload the anomalies output to MongoDB."""
    try:
        output_path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILE)
        max_attempts = 10
        attempt = 0
        while not os.path.exists(output_path) and attempt < max_attempts:
            print(f"Waiting for output file... Attempt {attempt + 1}/{max_attempts}")
            time.sleep(1)
            attempt += 1

        if not os.path.exists(output_path):
            print({'error': 'Anomalies output file not found after waiting.'})
            return

        with open(output_path, 'r') as f:
            data = json.load(f)

        metadata = {
            "generated_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_anomalies": len(data.get("anomalies", [])),
            "high_priority_count": sum(1 for a in data["anomalies"] if a.get("severity", 0) > 75),
            "anomaly_types": {},
            "recommendation": "Prioritize high-severity anomalies for immediate action"
        }

        for a in data["anomalies"]:
            a_type = a.get("type", "Unknown")
            metadata["anomaly_types"][a_type] = metadata["anomaly_types"].get(a_type, 0) + 1

        document = {
            "metadata": metadata,
            "anomalies": data["anomalies"]
        }

        result = collection.insert_one(document)
        print({
            'message': 'Data uploaded to MongoDB successfully.',
            'document_id': str(result.inserted_id)
        })

    except Exception as e:
        print(f"Error uploading to MongoDB: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True, port=5001)