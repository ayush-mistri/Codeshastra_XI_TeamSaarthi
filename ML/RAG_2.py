# import os
# import pandas as pd
# import numpy as np
# import json
# import joblib
# import time
# import logging
# from datetime import datetime
# import io
# import traceback
# from typing import List, Dict, Any, Optional
# import warnings
# warnings.filterwarnings('ignore')
# from fpdf import FPDF

# # Import Google Gemini API
# from google.generativeai import GenerativeModel
# import google.generativeai as genai

# # Setup logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     filename='anomaly_pipeline.log'
# )
# logger = logging.getLogger("anomaly_pipeline")

# # Configure Gemini API
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyChEDlxhCiE0GCl0p8S4e-TZ2JHfe-iC-I")
# genai.configure(api_key=GEMINI_API_KEY)

# # Load model
# MODEL_PATH = 'anomaly_detection_models.pkl'
# try:
#     models = joblib.load(MODEL_PATH)
#     logger.info(f"Loaded models from {MODEL_PATH}")
# except Exception as e:
#     logger.error(f"Error loading models: {str(e)}")
#     models = None

# # Simulated knowledge base for retrieval (in practice, use a vector DB like FAISS)
# KNOWLEDGE_BASE = {
#     "Tax Calculation Error": [
#         "Past audits show tax errors often stem from manual entry mistakes. Recommendation: Automate tax calculations.",
#         "Compliance risk: Incorrect tax reporting may lead to penalties from tax authorities."
#     ],
#     "Price Quantity Mismatch": [
#         "Historical data indicates this anomaly is common during peak hours. Check staff training.",
#         "Financial risk: Overcharging or undercharging affects revenue."
#     ],
#     "Significant Price Reduction": [
#         "Previous cases linked to unauthorized manager overrides. Review approval processes.",
#         "Operational risk: Large reductions may indicate fraud or system glitches."
#     ],
#     "High Discount": [
#         "Frequent high discounts detected in Q3 2024 audits. Suggest discount policy review.",
#         "Financial risk: Excessive discounts reduce profit margins."
#     ],
#     "Cancelled with Charges": [
#         "Past incidents tied to system sync issues with payment gateways. Verify integrations.",
#         "Compliance risk: Charging for cancelled orders may violate consumer laws."
#     ],
#     "Zomato Status Mismatch": [
#         "Noted in prior audits due to API delays. Recommend real-time status checks.",
#         "Operational risk: Mismatches confuse delivery staff and customers."
#     ],
#     "Swiggy Status Mismatch": [
#         "Similar to Zomato issues, often due to network latency. Enhance sync protocols.",
#         "Customer satisfaction risk: Incorrect statuses lead to complaints."
#     ],
#     "Delivery Time Anomaly": [
#         "Historical outliers linked to traffic or staffing shortages. Analyze logistics.",
#         "Operational risk: Delays impact customer experience."
#     ],
#     "Payment Type Anomaly": [
#         "Unusual payment methods flagged in fraud cases. Investigate transaction logs.",
#         "Financial risk: Potential fraudulent payments."
#     ],
#     "Order Modification": [
#         "Frequent modifications seen in high-value orders. Audit modification logs.",
#         "Operational risk: Excessive changes may indicate process inefficiencies."
#     ]
# }

# # Pre-existing anomaly explanations
# ANOMALY_EXPLANATIONS = {
#     "Tax Calculation Error": "The tax amount doesn't match the sum of individual tax components (CGST, SGST, VAT, Service Charge).",
#     "Price Quantity Mismatch": "The subtotal doesn't match the product of price and quantity.",
#     "Significant Price Reduction": "The invoice amount was reduced significantly after initial creation.",
#     "High Discount": "Unusually high discount percentage applied to the order.",
#     "Cancelled with Charges": "Order was cancelled but customer was still charged.",
#     "Zomato Status Mismatch": "Order status in restaurant system doesn't match Zomato's system.",
#     "Swiggy Status Mismatch": "Order status in restaurant system doesn't match Swiggy's system.",
#     "Delivery Time Anomaly": "Delivery time is either unusually short or long.",
#     "Payment Type Anomaly": "Unusual payment method for this order type or amount.",
#     "Order Modification": "Order was modified after initial processing."
# }

# def preprocess_data(df):
#     # (Unchanged from your original code)
#     logger.info(f"Preprocessing data with shape {df.shape}")
#     date_columns = [col for col in df.columns if 'Date' in col or 'Time' in col or 'Timestamp' in col]
#     for col in date_columns:
#         if col in df.columns:
#             try:
#                 df[col] = pd.to_datetime(df[col])
#                 logger.info(f"Converted {col} to datetime")
#             except Exception as e:
#                 logger.warning(f"Could not convert {col} to datetime: {e}")
#     try:
#         if all(col in df.columns for col in ['Discount', 'Sub_Total']):
#             df['discount_percentage'] = (df['Discount'] / df['Sub_Total']) * 100
#             df.loc[df['Sub_Total'] == 0, 'discount_percentage'] = 0
#         if all(col in df.columns for col in ['Price', 'Qty_', 'Sub_Total']):
#             df['price_qty_match'] = np.isclose(df['Price'] * df['Qty_'], df['Sub_Total'], rtol=0.01)
#         if all(col in df.columns for col in ['Sub_Total', 'Discount', 'Tax', 'Final_Total']):
#             df['formula_match'] = np.isclose(df['Sub_Total'] - df['Discount'] + df['Tax'], df['Final_Total'], rtol=0.01)
#         tax_components = ['CGST_Amount', 'SGST_Amount', 'VAT_Amount', 'Service_Charge_Amount']
#         available_components = [col for col in tax_components if col in df.columns]
#         if available_components and 'Tax' in df.columns:
#             df['calculated_tax'] = df[available_components].sum(axis=1)
#             df['tax_matches'] = np.isclose(df['calculated_tax'], df['Tax'], rtol=0.01)
#         if all(col in df.columns for col in ['amount_from', 'amount_to']):
#             df['invoice_modified'] = (~df['amount_from'].isna()) & (~df['amount_to'].isna())
#             df.loc[df['invoice_modified'], 'modification_amount'] = df.loc[df['invoice_modified'], 'amount_to'] - df.loc[df['invoice_modified'], 'amount_from']
#         if all(col in df.columns for col in ['Status', 'Status_z']):
#             df['status_z_mismatch'] = (~df['Status_z'].isna()) & (df['Status'] != df['Status_z'])
#         if all(col in df.columns for col in ['Status', 'Status_s']):
#             df['status_s_mismatch'] = (~df['Status_s'].isna()) & (df['Status'] != df['Status_s'])
#         if 'Status' in df.columns and 'Final_Total' in df.columns:
#             df['cancelled_with_charges'] = (df['Status'] == 'Cancelled') & (df['Final_Total'] > 0)
#         if 'discount_percentage' in df.columns:
#             df['high_discount'] = df['discount_percentage'] > 50
#         if 'modification_amount' in df.columns:
#             df['significant_price_reduction'] = (df['invoice_modified']) & (df['modification_amount'] < -10)
#     except Exception as e:
#         logger.error(f"Error in feature engineering: {str(e)}")
#         logger.error(traceback.format_exc())
#     return df

# def detect_anomalies(df):
#     # (Unchanged from your original code)
#     logger.info(f"Detecting anomalies in data with shape {df.shape}")
#     start_time = datetime.now()
#     try:
#         if models is not None:
#             preprocessor = models['preprocessor']
#             supervised_model = models['supervised_model']
#             numeric_cols = models['numeric_cols']
#             categorical_cols = models['categorical_cols']
#             feature_cols = numeric_cols + categorical_cols
#             available_cols = [col for col in feature_cols if col in df.columns]
#             missing_cols = [col for col in feature_cols if col not in df.columns]
#             if missing_cols:
#                 logger.warning(f"Missing columns for model: {missing_cols}")
#                 for col in missing_cols:
#                     if col in numeric_cols:
#                         df[col] = 0
#                     else:
#                         df[col] = "Unknown"
#             features_df = df[feature_cols].copy()
#             for col in numeric_cols:
#                 features_df[col] = features_df[col].fillna(features_df[col].median())
#             for col in categorical_cols:
#                 features_df[col] = features_df[col].fillna(features_df[col].mode()[0])
#             X_transformed = preprocessor.transform(features_df)
#             anomaly_probs = supervised_model.predict_proba(X_transformed)[:, 1]
#             anomaly_preds = supervised_model.predict(X_transformed)
#             threshold = 0.6
#             high_prob_anomalies = anomaly_probs >= threshold
#             anomaly_indices = np.where(high_prob_anomalies)[0]
#             if len(anomaly_indices) == 0:
#                 anomaly_indices = np.where(anomaly_preds == 1)[0]
#             logger.info(f"Detected {len(anomaly_indices)} anomalies")
#             anomalies = []
#             for idx in anomaly_indices:
#                 row = df.iloc[idx]
#                 anomaly_type = "Unknown Anomaly"
#                 if hasattr(row, 'tax_matches') and not row.get('tax_matches', True):
#                     anomaly_type = "Tax Calculation Error"
#                 elif hasattr(row, 'price_qty_match') and not row.get('price_qty_match', True):
#                     anomaly_type = "Price Quantity Mismatch"
#                 elif hasattr(row, 'significant_price_reduction') and row.get('significant_price_reduction', False):
#                     anomaly_type = "Significant Price Reduction"
#                 elif hasattr(row, 'high_discount') and row.get('high_discount', False):
#                     anomaly_type = "High Discount"
#                 elif hasattr(row, 'cancelled_with_charges') and row.get('cancelled_with_charges', False):
#                     anomaly_type = "Cancelled with Charges"
#                 elif hasattr(row, 'status_z_mismatch') and row.get('status_z_mismatch', False):
#                     anomaly_type = "Zomato Status Mismatch"
#                 elif hasattr(row, 'status_s_mismatch') and row.get('status_s_mismatch', False):
#                     anomaly_type = "Swiggy Status Mismatch"
#                 severity_score = float(anomaly_probs[idx])
#                 severity = "High" if severity_score >= 0.8 else "Medium" if severity_score >= 0.6 else "Low"
#                 fields = {}
#                 important_fields = ['Invoice_No_', 'Date', 'Timestamp', 'Status', 'Payment_Type', 'Order_Type', 'Area', 'Price', 'Qty_', 'Sub_Total', 'Discount', 'Tax', 'Final_Total', 'discount_percentage']
#                 for field in important_fields:
#                     if field in row and not pd.isna(row[field]):
#                         value = row[field]
#                         if isinstance(value, (np.integer, np.floating)):
#                             value = float(value)
#                         elif isinstance(value, (pd.Timestamp, np.datetime64)):
#                             value = str(value)
#                         fields[field] = value
#                 if anomaly_type == "Significant Price Reduction" and all(f in row for f in ['amount_from', 'amount_to']):
#                     fields['original_amount'] = float(row['amount_from'])
#                     fields['modified_amount'] = float(row['amount_to'])
#                     fields['modification_amount'] = float(row['modification_amount'])
#                     if 'modified_by' in row and not pd.isna(row['modified_by']):
#                         fields['modified_by'] = row['modified_by']
#                 if anomaly_type == "Zomato Status Mismatch":
#                     fields['restaurant_status'] = row.get('Status', 'Unknown')
#                     fields['zomato_status'] = row.get('Status_z', 'Unknown')
#                 if anomaly_type == "Swiggy Status Mismatch":
#                     fields['restaurant_status'] = row.get('Status', 'Unknown')
#                     fields['swiggy_status'] = row.get('Status_s', 'Unknown')
#                 explanation = ANOMALY_EXPLANATIONS.get(anomaly_type, "Unusual pattern detected in transaction data.")
#                 anomaly = {
#                     "invoice_id": str(row.get('Invoice_No_', f"ID-{idx}")),
#                     "timestamp": str(row.get('Timestamp', '')),
#                     "anomaly_type": anomaly_type,
#                     "severity": severity,
#                     "severity_score": severity_score,
#                     "fields": fields,
#                     "explanation": explanation
#                 }
#                 anomalies.append(anomaly)
#             anomalies = sorted(anomalies, key=lambda x: x['severity_score'], reverse=True)
#             if len(anomalies) > 1000:
#                 logger.info(f"Limiting output to top 1000 anomalies out of {len(anomalies)}")
#                 anomalies = anomalies[:1000]
#             end_time = datetime.now()
#             execution_time = (end_time - start_time).total_seconds()
#             return {
#                 "status": "success",
#                 "message": "Anomaly detection completed successfully",
#                 "total_records": len(df),
#                 "anomaly_count": len(anomalies),
#                 "anomaly_percentage": (len(anomalies) / len(df)) * 100 if len(df) > 0 else 0,
#                 "anomalies": anomalies,
#                 "execution_time": execution_time
#             }
#         else:
#             logger.warning("Models not loaded, falling back to rule-based detection")
#             return rule_based_detection(df)
#     except Exception as e:
#         logger.error(f"Error during anomaly detection: {str(e)}")
#         logger.error(traceback.format_exc())
#         return {"status": "error", "message": f"Error during anomaly detection: {str(e)}", "anomalies": []}

# def rule_based_detection(df):
#     # (Unchanged from your original code)
#     logger.info("Using rule-based anomaly detection")
#     try:
#         anomalies = []
#         rules = []
#         if 'price_qty_match' in df.columns:
#             rules.append(('price_qty_mismatch', ~df['price_qty_match'], "Price Quantity Mismatch"))
#         if 'formula_match' in df.columns:
#             rules.append(('total_calculation_error', ~df['formula_match'], "Total Calculation Error"))
#         if 'tax_matches' in df.columns:
#             rules.append(('tax_calculation_error', ~df['tax_matches'], "Tax Calculation Error"))
#         if 'high_discount' in df.columns:
#             rules.append(('high_discount', df['high_discount'], "High Discount"))
#         if 'significant_price_reduction' in df.columns:
#             rules.append(('significant_price_reduction', df['significant_price_reduction'], "Significant Price Reduction"))
#         if 'cancelled_with_charges' in df.columns:
#             rules.append(('cancelled_with_charges', df['cancelled_with_charges'], "Cancelled with Charges"))
#         if 'status_z_mismatch' in df.columns:
#             rules.append(('zomato_status_mismatch', df['status_z_mismatch'], "Zomato Status Mismatch"))
#         if 'status_s_mismatch' in df.columns:
#             rules.append(('swiggy_status_mismatch', df['status_s_mismatch'], "Swiggy Status Mismatch"))
#         for rule_name, condition, anomaly_type in rules:
#             anomaly_rows = df[condition]
#             logger.info(f"Rule-based detection found {len(anomaly_rows)} {rule_name} anomalies")
#             for idx, row in anomaly_rows.iterrows():
#                 if rule_name in ['tax_calculation_error', 'significant_price_reduction', 'cancelled_with_charges']:
#                     severity = "High"
#                     severity_score = 0.9
#                 elif rule_name in ['price_qty_mismatch', 'total_calculation_error', 'high_discount']:
#                     severity = "Medium"
#                     severity_score = 0.7
#                 else:
#                     severity = "Low"
#                     severity_score = 0.5
#                 fields = {}
#                 important_fields = ['Invoice_No_', 'Date', 'Timestamp', 'Status', 'Payment_Type', 'Order_Type', 'Area', 'Price', 'Qty_', 'Sub_Total', 'Discount', 'Tax', 'Final_Total', 'discount_percentage']
#                 for field in important_fields:
#                     if field in row and not pd.isna(row[field]):
#                         value = row[field]
#                         if isinstance(value, (np.integer, np.floating)):
#                             value = float(value)
#                         elif isinstance(value, (pd.Timestamp, np.datetime64)):
#                             value = str(value)
#                         fields[field] = value
#                 anomaly = {
#                     "invoice_id": str(row.get('Invoice_No_', f"ID-{idx}")),
#                     "timestamp": str(row.get('Timestamp', '')),
#                     "anomaly_type": anomaly_type,
#                     "severity": severity,
#                     "severity_score": severity_score,
#                     "fields": fields,
#                     "explanation": ANOMALY_EXPLANATIONS.get(anomaly_type, "Anomaly detected by rule-based system.")
#                 }
#                 anomalies.append(anomaly)
#         anomalies = sorted(anomalies, key=lambda x: x['severity_score'], reverse=True)
#         return {
#             "status": "success",
#             "message": "Rule-based anomaly detection completed",
#             "total_records": len(df),
#             "anomaly_count": len(anomalies),
#             "anomaly_percentage": (len(anomalies) / len(df)) * 100 if len(df) > 0 else 0,
#             "anomalies": anomalies,
#             "execution_time": 0.0
#         }
#     except Exception as e:
#         logger.error(f"Error during rule-based detection: {str(e)}")
#         return {"status": "error", "message": f"Error during rule-based detection: {str(e)}", "anomalies": []}

# def retrieve_context(anomaly_type: str) -> List[str]:
#     """Retrieve relevant context from the knowledge base"""
#     logger.info(f"Retrieving context for anomaly type: {anomaly_type}")
#     return KNOWLEDGE_BASE.get(anomaly_type, ["No additional context available."])

# def generate_rag_report(anomaly_results):
#     """Generate a report using a RAG pipeline with Gemini"""
#     logger.info("Generating RAG-based report")
    
#     anomalies = anomaly_results.get("anomalies", [])
#     total_records = anomaly_results.get("total_records", 0)
#     execution_time = anomaly_results.get("execution_time", 0)
    
#     if not GEMINI_API_KEY:
#         logger.warning("Gemini API key not found, falling back to simplified report")
#         return generate_simplified_report(anomaly_results)
    
#     try:
#         # Initialize Gemini model
#         model = GenerativeModel('gemini-2.0-flash')
        
#         # Count anomalies by severity and type
#         severity_counts = {"High": 0, "Medium": 0, "Low": 0}
#         anomaly_types = {}
#         for anomaly in anomalies:
#             severity = anomaly.get("severity", "Medium")
#             severity_counts[severity] += 1
#             anomaly_type = anomaly.get("anomaly_type", "Unknown")
#             anomaly_types[anomaly_type] = anomaly_types.get(anomaly_type, 0) + 1
        
#         total_anomalies = len(anomalies)
#         anomaly_percentage = (total_anomalies / total_records) * 100 if total_records > 0 else 0
        
#         # Generate executive summary with retrieved context
#         top_anomaly_types = sorted(anomaly_types.items(), key=lambda x: x[1], reverse=True)[:5]
#         retrieved_context = {atype: retrieve_context(atype) for atype, _ in top_anomaly_types}
#         summary_prompt = f"""
#         You are an expert financial auditor preparing an executive summary for restaurant management.
        
#         AUDIT DATA:
#         - Total records: {total_records}
#         - Anomalies detected: {total_anomalies}
#         - Anomaly percentage: {anomaly_percentage:.2f}%
#         - High severity: {severity_counts['High']}
#         - Medium severity: {severity_counts['Medium']}
#         - Low severity: {severity_counts['Low']}
        
#         Top anomaly types and retrieved context:
#         {', '.join([f'{k}: {v} - {"; ".join(retrieved_context[k])}' for k, v in top_anomaly_types])}
        
#         Provide a 300-400 word executive summary that:
#         1. Summarizes data quality and compliance
#         2. Highlights critical issues using retrieved context
#         3. Identifies risks (financial, operational, compliance) based on context
#         4. Provides recommendations informed by retrieved insights
#         """
#         summary_response = model.generate_content(summary_prompt)
#         executive_summary = summary_response.text
        
#         # Process top anomalies with RAG
#         anomalies_with_explanations = []
#         for i, anomaly in enumerate(anomalies[:20]):
#             anomaly_type = anomaly['anomaly_type']
#             retrieved_context = retrieve_context(anomaly_type)
#             explanation_prompt = f"""
#             Analyze this anomaly as a financial auditor:
#             Invoice ID: {anomaly['invoice_id']}
#             Timestamp: {anomaly['timestamp']}
#             Type: {anomaly['anomaly_type']}
#             Severity: {anomaly['severity']}
#             Fields: {json.dumps(anomaly['fields'], indent=2)}
#             Retrieved Context: {"; ".join(retrieved_context)}
            
#             Provide detailed explanation including:
#             1. Likely cause (use retrieved context)
#             2. Business risks (use retrieved context)
#             3. Investigation steps
#             4. Corrective actions (use retrieved context)
#             """
#             explanation_response = model.generate_content(explanation_prompt)
#             anomaly_with_explanation = anomaly.copy()
#             anomaly_with_explanation["detailed_explanation"] = explanation_response.text
#             anomalies_with_explanations.append(anomaly_with_explanation)
        
#         # Add basic explanations for remaining
#         for anomaly in anomalies[20:]:
#             anomaly_with_explanation = anomaly.copy()
#             anomaly_with_explanation["detailed_explanation"] = anomaly["explanation"]
#             anomalies_with_explanations.append(anomaly_with_explanation)
        
#         # Generate report
#         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         report = {
#             "report_title": "Restaurant Sales Data Audit Report (RAG)",
#             "generated_at": timestamp,
#             "executive_summary": executive_summary,
#             "audit_metrics": {
#                 "total_records_analyzed": total_records,
#                 "total_anomalies_detected": total_anomalies,
#                 "anomaly_percentage": f"{anomaly_percentage:.2f}%",
#                 "execution_time": execution_time,
#             },
#             "severity_breakdown": severity_counts,
#             "anomaly_type_breakdown": anomaly_types,
#             "detailed_findings": anomalies_with_explanations,
#         }
#         return report
    
#     except Exception as e:
#         logger.error(f"Error in RAG processing: {str(e)}")
#         return generate_simplified_report(anomaly_results)

# def generate_simplified_report(anomaly_results):
#     # (Unchanged from your updated code)
#     logger.info("Generating simplified report")
#     anomalies = anomaly_results.get("anomalies", [])
#     total_records = anomaly_results.get("total_records", 0)
#     execution_time = anomaly_results.get("execution_time", 0)
#     severity_counts = {"High": 0, "Medium": 0, "Low": 0}
#     anomaly_types = {}
#     for anomaly in anomalies:
#         severity = anomaly.get("severity", "Medium")
#         severity_counts[severity] += 1
#         anomaly_type = anomaly.get("anomaly_type", "Unknown")
#         anomaly_types[anomaly_type] = anomaly_types.get(anomaly_type, 0) + 1
#     total_anomalies = len(anomalies)
#     anomaly_percentage = (total_anomalies / total_records) * 100 if total_records > 0 else 0
#     executive_summary = (
#         f"This audit analyzed {total_records} records and detected {total_anomalies} anomalies, "
#         f"representing {anomaly_percentage:.2f}% of the total data. The severity breakdown is as follows: "
#         f"High: {severity_counts['High']}, Medium: {severity_counts['Medium']}, Low: {severity_counts['Low']}. "
#         f"The most common anomaly types include {', '.join([f'{k} ({v})' for k, v in sorted(anomaly_types.items(), key=lambda x: x[1], reverse=True)[:3]])}. "
#         "Critical issues may include tax calculation errors, significant price reductions, or cancelled orders with charges, "
#         "posing financial and operational risks. It is recommended to investigate high-severity anomalies first, "
#         "review discount policies, and ensure system synchronization with third-party platforms like Zomato and Swiggy."
#     )
#     anomalies_with_explanations = []
#     for anomaly in anomalies:
#         anomaly_with_explanation = anomaly.copy()
#         anomaly_with_explanation["detailed_explanation"] = anomaly["explanation"]
#         anomalies_with_explanations.append(anomaly_with_explanation)
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     report = {
#         "report_title": "Restaurant Sales Data Audit Report (Simplified)",
#         "generated_at": timestamp,
#         "executive_summary": executive_summary,
#         "audit_metrics": {
#             "total_records_analyzed": total_records,
#             "total_anomalies_detected": total_anomalies,
#             "anomaly_percentage": f"{anomaly_percentage:.2f}%",
#             "execution_time": execution_time,
#         },
#         "severity_breakdown": severity_counts,
#         "anomaly_type_breakdown": anomaly_types,
#         "detailed_findings": anomalies_with_explanations,
#     }
#     return report

# def save_report(report, output_format="pdf"):
#     # (Unchanged from your updated code)
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     output_dir = "reports"
#     os.makedirs(output_dir, exist_ok=True)
#     if output_format.lower() == "json":
#         filename = f"{output_dir}/anomaly_report_{timestamp}.json"
#         with open(filename, 'w') as f:
#             json.dump(report, f, indent=2)
#         logger.info(f"Saved JSON report to {filename}")
#         return filename
#     elif output_format.lower() == "pdf":
#         filename = f"{output_dir}/anomaly_report_{timestamp}.pdf"
#         pdf = FPDF()
#         pdf.set_auto_page_break(auto=True, margin=15)
#         pdf.add_page()
#         pdf.set_font("Arial", "B", 16)
#         pdf.cell(0, 10, report["report_title"], ln=True, align="C")
#         pdf.set_font("Arial", "", 12)
#         pdf.cell(0, 10, f"Generated at: {report['generated_at']}", ln=True, align="C")
#         pdf.ln(10)
#         pdf.set_font("Arial", "B", 14)
#         pdf.cell(0, 10, "Executive Summary", ln=True)
#         pdf.set_font("Arial", "", 12)
#         pdf.multi_cell(0, 10, report["executive_summary"])
#         pdf.ln(10)
#         pdf.set_font("Arial", "B", 14)
#         pdf.cell(0, 10, "Audit Metrics", ln=True)
#         pdf.set_font("Arial", "", 12)
#         metrics = report["audit_metrics"]
#         pdf.cell(0, 10, f"Total Records Analyzed: {metrics['total_records_analyzed']}", ln=True)
#         pdf.cell(0, 10, f"Total Anomalies Detected: {metrics['total_anomalies_detected']}", ln=True)
#         pdf.cell(0, 10, f"Anomaly Percentage: {metrics['anomaly_percentage']}", ln=True)
#         pdf.cell(0, 10, f"Execution Time: {metrics['execution_time']} seconds", ln=True)
#         pdf.ln(10)
#         pdf.set_font("Arial", "B", 14)
#         pdf.cell(0, 10, "Severity Breakdown", ln=True)
#         pdf.set_font("Arial", "", 12)
#         for severity, count in report["severity_breakdown"].items():
#             pdf.cell(0, 10, f"{severity}: {count}", ln=True)
#         pdf.ln(10)
#         pdf.set_font("Arial", "B", 14)
#         pdf.cell(0, 10, "Anomaly Type Breakdown", ln=True)
#         pdf.set_font("Arial", "", 12)
#         for anomaly_type, count in report["anomaly_type_breakdown"].items():
#             pdf.cell(0, 10, f"{anomaly_type}: {count}", ln=True)
#         pdf.ln(10)
#         pdf.set_font("Arial", "B", 14)
#         pdf.cell(0, 10, "Detailed Findings (Top 10)", ln=True)
#         pdf.set_font("Arial", "", 12)
#         for i, anomaly in enumerate(report["detailed_findings"][:10], 1):
#             pdf.set_font("Arial", "B", 12)
#             pdf.cell(0, 10, f"Anomaly {i}: {anomaly['anomaly_type']} (Severity: {anomaly['severity']})", ln=True)
#             pdf.set_font("Arial", "", 12)
#             pdf.cell(0, 10, f"Invoice ID: {anomaly['invoice_id']}", ln=True)
#             pdf.cell(0, 10, f"Timestamp: {anomaly['timestamp']}", ln=True)
#             pdf.multi_cell(0, 10, f"Explanation: {anomaly['detailed_explanation']}")
#             pdf.ln(5)
#         pdf.output(filename)
#         logger.info(f"Saved PDF report to {filename}")
#         return filename
#     else:
#         logger.error(f"Unsupported output format: {output_format}")
#         raise ValueError(f"Unsupported output format: {output_format}")

# def main(input_file: str):
#     """Main execution function with RAG pipeline"""
#     try:
#         df = pd.read_csv(input_file)
#         logger.info(f"Loaded data from {input_file}")
#         preprocessed_df = preprocess_data(df)
#         anomaly_results = detect_anomalies(preprocessed_df)
#         report = generate_rag_report(anomaly_results)  # Use RAG report
#         pdf_file = save_report(report, output_format="pdf")
#         logger.info("Pipeline completed successfully")
#         return pdf_file
#     except Exception as e:
#         logger.error(f"Pipeline failed: {str(e)}")
#         raise

# if __name__ == "__main__":
#     input_file = "./Hackathon_Dataset.csv"
#     pdf_file = main(input_file)
#     print(f"Generated PDF report at: {pdf_file}")


import os
import pandas as pd
import numpy as np
import json
import joblib
import time
import logging
from datetime import datetime
import io
import traceback
from typing import List, Dict, Any, Optional
import warnings
warnings.filterwarnings('ignore')
from fpdf import FPDF
import matplotlib.pyplot as plt
from google.generativeai import GenerativeModel
import google.generativeai as genai

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='anomaly_pipeline.log'
)
logger = logging.getLogger("anomaly_pipeline")

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyChEDlxhCiE0GCl0p8S4e-TZ2JHfe-iC-I")
genai.configure(api_key=GEMINI_API_KEY)

# Load model
MODEL_PATH = 'anomaly_detection_models.pkl'
try:
    models = joblib.load(MODEL_PATH)
    logger.info(f"Loaded models from {MODEL_PATH}")
except Exception as e:
    logger.error(f"Error loading models: {str(e)}")
    models = None

# Simulated knowledge base for retrieval
KNOWLEDGE_BASE = {
    "Tax Calculation Error": ["Past audits show tax errors often stem from manual entry mistakes. Recommendation: Automate tax calculations.", "Compliance risk: Incorrect tax reporting may lead to penalties."],
    "Price Quantity Mismatch": ["Historical data indicates this anomaly is common during peak hours. Check staff training.", "Financial risk: Overcharging or undercharging affects revenue."],
    "Significant Price Reduction": ["Previous cases linked to unauthorized manager overrides. Review approval processes.", "Operational risk: Large reductions may indicate fraud or glitches."],
    "High Discount": ["Frequent high discounts detected in Q3 2024 audits. Suggest discount policy review.", "Financial risk: Excessive discounts reduce profit margins."],
    "Cancelled with Charges": ["Past incidents tied to system sync issues with payment gateways. Verify integrations.", "Compliance risk: Charging for cancelled orders may violate consumer laws."]
}

ANOMALY_EXPLANATIONS = {
    "Tax Calculation Error": "The tax amount doesn't match the sum of individual tax components (CGST, SGST, VAT, Service Charge).",
    "Price Quantity Mismatch": "The subtotal doesn't match the product of price and quantity.",
    "Significant Price Reduction": "The invoice amount was reduced significantly after initial creation.",
    "High Discount": "Unusually high discount percentage applied to the order.",
    "Cancelled with Charges": "Order was cancelled but customer was still charged.",
    "Zomato Status Mismatch": "Order status in restaurant system doesn't match Zomato's system.",
    "Swiggy Status Mismatch": "Order status in restaurant system doesn't match Swiggy's system.",
    "Delivery Time Anomaly": "Delivery time is either unusually short or long.",
    "Payment Type Anomaly": "Unusual payment method for this order type or amount.",
    "Order Modification": "Order was modified after initial processing."
}

def preprocess_data(df):
    # (Unchanged)
    logger.info(f"Preprocessing data with shape {df.shape}")
    date_columns = [col for col in df.columns if 'Date' in col or 'Time' in col or 'Timestamp' in col]
    for col in date_columns:
        if col in df.columns:
            try:
                df[col] = pd.to_datetime(df[col])
                logger.info(f"Converted {col} to datetime")
            except Exception as e:
                logger.warning(f"Could not convert {col} to datetime: {e}")
    try:
        if all(col in df.columns for col in ['Discount', 'Sub_Total']):
            df['discount_percentage'] = (df['Discount'] / df['Sub_Total']) * 100
            df.loc[df['Sub_Total'] == 0, 'discount_percentage'] = 0
        if all(col in df.columns for col in ['Price', 'Qty_', 'Sub_Total']):
            df['price_qty_match'] = np.isclose(df['Price'] * df['Qty_'], df['Sub_Total'], rtol=0.01)
        if all(col in df.columns for col in ['Sub_Total', 'Discount', 'Tax', 'Final_Total']):
            df['formula_match'] = np.isclose(df['Sub_Total'] - df['Discount'] + df['Tax'], df['Final_Total'], rtol=0.01)
        tax_components = ['CGST_Amount', 'SGST_Amount', 'VAT_Amount', 'Service_Charge_Amount']
        available_components = [col for col in tax_components if col in df.columns]
        if available_components and 'Tax' in df.columns:
            df['calculated_tax'] = df[available_components].sum(axis=1)
            df['tax_matches'] = np.isclose(df['calculated_tax'], df['Tax'], rtol=0.01)
        if all(col in df.columns for col in ['amount_from', 'amount_to']):
            df['invoice_modified'] = (~df['amount_from'].isna()) & (~df['amount_to'].isna())
            df.loc[df['invoice_modified'], 'modification_amount'] = df.loc[df['invoice_modified'], 'amount_to'] - df.loc[df['invoice_modified'], 'amount_from']
        if all(col in df.columns for col in ['Status', 'Status_z']):
            df['status_z_mismatch'] = (~df['Status_z'].isna()) & (df['Status'] != df['Status_z'])
        if all(col in df.columns for col in ['Status', 'Status_s']):
            df['status_s_mismatch'] = (~df['Status_s'].isna()) & (df['Status'] != df['Status_s'])
        if 'Status' in df.columns and 'Final_Total' in df.columns:
            df['cancelled_with_charges'] = (df['Status'] == 'Cancelled') & (df['Final_Total'] > 0)
        if 'discount_percentage' in df.columns:
            df['high_discount'] = df['discount_percentage'] > 50
        if 'modification_amount' in df.columns:
            df['significant_price_reduction'] = (df['invoice_modified']) & (df['modification_amount'] < -10)
    except Exception as e:
        logger.error(f"Error in feature engineering: {str(e)}")
        logger.error(traceback.format_exc())
    return df

def detect_anomalies(df):
    # (Unchanged)
    logger.info(f"Detecting anomalies in data with shape {df.shape}")
    start_time = datetime.now()
    try:
        if models is not None:
            preprocessor = models['preprocessor']
            supervised_model = models['supervised_model']
            numeric_cols = models['numeric_cols']
            categorical_cols = models['categorical_cols']
            feature_cols = numeric_cols + categorical_cols
            available_cols = [col for col in feature_cols if col in df.columns]
            missing_cols = [col for col in feature_cols if col not in df.columns]
            if missing_cols:
                logger.warning(f"Missing columns for model: {missing_cols}")
                for col in missing_cols:
                    if col in numeric_cols:
                        df[col] = 0
                    else:
                        df[col] = "Unknown"
            features_df = df[feature_cols].copy()
            for col in numeric_cols:
                features_df[col] = features_df[col].fillna(features_df[col].median())
            for col in categorical_cols:
                features_df[col] = features_df[col].fillna(features_df[col].mode()[0])
            X_transformed = preprocessor.transform(features_df)
            anomaly_probs = supervised_model.predict_proba(X_transformed)[:, 1]
            anomaly_preds = supervised_model.predict(X_transformed)
            threshold = 0.6
            high_prob_anomalies = anomaly_probs >= threshold
            anomaly_indices = np.where(high_prob_anomalies)[0]
            if len(anomaly_indices) == 0:
                anomaly_indices = np.where(anomaly_preds == 1)[0]
            logger.info(f"Detected {len(anomaly_indices)} anomalies")
            anomalies = []
            for idx in anomaly_indices:
                row = df.iloc[idx]
                anomaly_type = "Unknown Anomaly"
                if hasattr(row, 'tax_matches') and not row.get('tax_matches', True):
                    anomaly_type = "Tax Calculation Error"
                elif hasattr(row, 'price_qty_match') and not row.get('price_qty_match', True):
                    anomaly_type = "Price Quantity Mismatch"
                elif hasattr(row, 'significant_price_reduction') and row.get('significant_price_reduction', False):
                    anomaly_type = "Significant Price Reduction"
                elif hasattr(row, 'high_discount') and row.get('high_discount', False):
                    anomaly_type = "High Discount"
                elif hasattr(row, 'cancelled_with_charges') and row.get('cancelled_with_charges', False):
                    anomaly_type = "Cancelled with Charges"
                elif hasattr(row, 'status_z_mismatch') and row.get('status_z_mismatch', False):
                    anomaly_type = "Zomato Status Mismatch"
                elif hasattr(row, 'status_s_mismatch') and row.get('status_s_mismatch', False):
                    anomaly_type = "Swiggy Status Mismatch"
                severity_score = float(anomaly_probs[idx])
                severity = "High" if severity_score >= 0.8 else "Medium" if severity_score >= 0.6 else "Low"
                fields = {}
                important_fields = ['Invoice_No_', 'Date', 'Timestamp', 'Status', 'Payment_Type', 'Order_Type', 'Area', 'Price', 'Qty_', 'Sub_Total', 'Discount', 'Tax', 'Final_Total', 'discount_percentage']
                for field in important_fields:
                    if field in row and not pd.isna(row[field]):
                        value = row[field]
                        if isinstance(value, (np.integer, np.floating)):
                            value = float(value)
                        elif isinstance(value, (pd.Timestamp, np.datetime64)):
                            value = str(value)
                        fields[field] = value
                if anomaly_type == "Significant Price Reduction" and all(f in row for f in ['amount_from', 'amount_to']):
                    fields['original_amount'] = float(row['amount_from'])
                    fields['modified_amount'] = float(row['amount_to'])
                    fields['modification_amount'] = float(row['modification_amount'])
                    if 'modified_by' in row and not pd.isna(row['modified_by']):
                        fields['modified_by'] = row['modified_by']
                if anomaly_type == "Zomato Status Mismatch":
                    fields['restaurant_status'] = row.get('Status', 'Unknown')
                    fields['zomato_status'] = row.get('Status_z', 'Unknown')
                if anomaly_type == "Swiggy Status Mismatch":
                    fields['restaurant_status'] = row.get('Status', 'Unknown')
                    fields['swiggy_status'] = row.get('Status_s', 'Unknown')
                explanation = ANOMALY_EXPLANATIONS.get(anomaly_type, "Unusual pattern detected in transaction data.")
                anomaly = {
                    "invoice_id": str(row.get('Invoice_No_', f"ID-{idx}")),
                    "timestamp": str(row.get('Timestamp', '')),
                    "anomaly_type": anomaly_type,
                    "severity": severity,
                    "severity_score": severity_score,
                    "fields": fields,
                    "explanation": explanation
                }
                anomalies.append(anomaly)
            anomalies = sorted(anomalies, key=lambda x: x['severity_score'], reverse=True)
            if len(anomalies) > 1000:
                logger.info(f"Limiting output to top 1000 anomalies out of {len(anomalies)}")
                anomalies = anomalies[:1000]
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            return {
                "status": "success",
                "message": "Anomaly detection completed successfully",
                "total_records": len(df),
                "anomaly_count": len(anomalies),
                "anomaly_percentage": (len(anomalies) / len(df)) * 100 if len(df) > 0 else 0,
                "anomalies": anomalies,
                "execution_time": execution_time
            }
        else:
            logger.warning("Models not loaded, falling back to rule-based detection")
            return rule_based_detection(df)
    except Exception as e:
        logger.error(f"Error during anomaly detection: {str(e)}")
        logger.error(traceback.format_exc())
        return {"status": "error", "message": f"Error during anomaly detection: {str(e)}", "anomalies": []}

def rule_based_detection(df):
    # (Unchanged)
    logger.info("Using rule-based anomaly detection")
    try:
        anomalies = []
        rules = []
        if 'price_qty_match' in df.columns:
            rules.append(('price_qty_mismatch', ~df['price_qty_match'], "Price Quantity Mismatch"))
        if 'formula_match' in df.columns:
            rules.append(('total_calculation_error', ~df['formula_match'], "Total Calculation Error"))
        if 'tax_matches' in df.columns:
            rules.append(('tax_calculation_error', ~df['tax_matches'], "Tax Calculation Error"))
        if 'high_discount' in df.columns:
            rules.append(('high_discount', df['high_discount'], "High Discount"))
        if 'significant_price_reduction' in df.columns:
            rules.append(('significant_price_reduction', df['significant_price_reduction'], "Significant Price Reduction"))
        if 'cancelled_with_charges' in df.columns:
            rules.append(('cancelled_with_charges', df['cancelled_with_charges'], "Cancelled with Charges"))
        if 'status_z_mismatch' in df.columns:
            rules.append(('zomato_status_mismatch', df['status_z_mismatch'], "Zomato Status Mismatch"))
        if 'status_s_mismatch' in df.columns:
            rules.append(('swiggy_status_mismatch', df['status_s_mismatch'], "Swiggy Status Mismatch"))
        for rule_name, condition, anomaly_type in rules:
            anomaly_rows = df[condition]
            logger.info(f"Rule-based detection found {len(anomaly_rows)} {rule_name} anomalies")
            for idx, row in anomaly_rows.iterrows():
                if rule_name in ['tax_calculation_error', 'significant_price_reduction', 'cancelled_with_charges']:
                    severity = "High"
                    severity_score = 0.9
                elif rule_name in ['price_qty_mismatch', 'total_calculation_error', 'high_discount']:
                    severity = "Medium"
                    severity_score = 0.7
                else:
                    severity = "Low"
                    severity_score = 0.5
                fields = {}
                important_fields = ['Invoice_No_', 'Date', 'Timestamp', 'Status', 'Payment_Type', 'Order_Type', 'Area', 'Price', 'Qty_', 'Sub_Total', 'Discount', 'Tax', 'Final_Total', 'discount_percentage']
                for field in important_fields:
                    if field in row and not pd.isna(row[field]):
                        value = row[field]
                        if isinstance(value, (np.integer, np.floating)):
                            value = float(value)
                        elif isinstance(value, (pd.Timestamp, np.datetime64)):
                            value = str(value)
                        fields[field] = value
                anomaly = {
                    "invoice_id": str(row.get('Invoice_No_', f"ID-{idx}")),
                    "timestamp": str(row.get('Timestamp', '')),
                    "anomaly_type": anomaly_type,
                    "severity": severity,
                    "severity_score": severity_score,
                    "fields": fields,
                    "explanation": ANOMALY_EXPLANATIONS.get(anomaly_type, "Anomaly detected by rule-based system.")
                }
                anomalies.append(anomaly)
        anomalies = sorted(anomalies, key=lambda x: x['severity_score'], reverse=True)
        return {
            "status": "success",
            "message": "Rule-based anomaly detection completed",
            "total_records": len(df),
            "anomaly_count": len(anomalies),
            "anomaly_percentage": (len(anomalies) / len(df)) * 100 if len(df) > 0 else 0,
            "anomalies": anomalies,
            "execution_time": 0.0
        }
    except Exception as e:
        logger.error(f"Error during rule-based detection: {str(e)}")
        return {"status": "error", "message": f"Error during rule-based detection: {str(e)}", "anomalies": []}

def retrieve_context(anomaly_type: str) -> List[str]:
    logger.info(f"Retrieving context for anomaly type: {anomaly_type}")
    return KNOWLEDGE_BASE.get(anomaly_type, ["No additional context available."])

def generate_rag_report(anomaly_results):
    logger.info("Generating RAG-based report")
    anomalies = anomaly_results.get("anomalies", [])
    total_records = anomaly_results.get("total_records", 0)
    execution_time = anomaly_results.get("execution_time", 0)
    
    if not GEMINI_API_KEY:
        logger.warning("Gemini API key not found, falling back to simplified report")
        return generate_simplified_report(anomaly_results)
    
    try:
        model = GenerativeModel('gemini-2.0-flash')
        severity_counts = {"High": 0, "Medium": 0, "Low": 0}
        anomaly_types = {}
        for anomaly in anomalies:
            severity = anomaly.get("severity", "Medium")
            severity_counts[severity] += 1
            anomaly_type = anomaly.get("anomaly_type", "Unknown")
            anomaly_types[anomaly_type] = anomaly_types.get(anomaly_type, 0) + 1
        
        total_anomalies = len(anomalies)
        anomaly_percentage = (total_anomalies / total_records) * 100 if total_records > 0 else 0
        
        top_anomaly_types = sorted(anomaly_types.items(), key=lambda x: x[1], reverse=True)[:5]
        retrieved_context = {atype: retrieve_context(atype) for atype, _ in top_anomaly_types}
        summary_prompt = f"""
        You are an expert financial auditor preparing an executive summary.
        AUDIT DATA:
        - Total records: {total_records}
        - Anomalies detected: {total_anomalies}
        - Anomaly percentage: {anomaly_percentage:.2f}%
        - High severity: {severity_counts['High']}
        - Medium severity: {severity_counts['Medium']}
        - Low severity: {severity_counts['Low']}
        Top anomaly types and context:
        {', '.join([f'{k}: {v} - {"; ".join(retrieved_context[k])}' for k, v in top_anomaly_types])}
        Provide a concise 150-200 word executive summary that:
        1. Summarizes data quality and compliance
        2. Highlights critical issues using retrieved context
        3. Identifies key risks
        4. Provides brief recommendations
        """
        summary_response = model.generate_content(summary_prompt)
        executive_summary = summary_response.text
        
        anomalies_with_explanations = []
        for anomaly in anomalies:
            anomaly_type = anomaly['anomaly_type']
            retrieved_context = retrieve_context(anomaly_type)
            feedback_prompt = f"""
            Provide a short feedback (1-2 sentences) for this anomaly:
            Type: {anomaly_type}
            Severity: {anomaly['severity']}
            Explanation: {anomaly['explanation']}
            Context: {"; ".join(retrieved_context)}
            """
            feedback_response = model.generate_content(feedback_prompt)
            anomaly_with_explanation = anomaly.copy()
            anomaly_with_explanation["detailed_explanation"] = anomaly["explanation"]
            anomaly_with_explanation["feedback"] = feedback_response.text
            anomalies_with_explanations.append(anomaly_with_explanation)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report = {
            "report_title": "Restaurant Sales Data Audit Report (RAG)",
            "generated_at": timestamp,
            "executive_summary": executive_summary,
            "audit_metrics": {
                "total_records_analyzed": total_records,
                "total_anomalies_detected": total_anomalies,
                "anomaly_percentage": f"{anomaly_percentage:.2f}%",
                "execution_time": execution_time,
            },
            "anomaly_type_breakdown": anomaly_types,
            "detailed_findings": anomalies_with_explanations,
        }
        return report
    
    except Exception as e:
        logger.error(f"Error in RAG processing: {str(e)}")
        return generate_simplified_report(anomaly_results)

def generate_simplified_report(anomaly_results):
    logger.info("Generating simplified report")
    anomalies = anomaly_results.get("anomalies", [])
    total_records = anomaly_results.get("total_records", 0)
    execution_time = anomaly_results.get("execution_time", 0)
    severity_counts = {"High": 0, "Medium": 0, "Low": 0}
    anomaly_types = {}
    for anomaly in anomalies:
        severity = anomaly.get("severity", "Medium")
        severity_counts[severity] += 1
        anomaly_type = anomaly.get("anomaly_type", "Unknown")
        anomaly_types[anomaly_type] = anomaly_types.get(anomaly_type, 0) + 1
    total_anomalies = len(anomalies)
    anomaly_percentage = (total_anomalies / total_records) * 100 if total_records > 0 else 0
    executive_summary = (
        f"This audit analyzed {total_records} records, detecting {total_anomalies} anomalies ({anomaly_percentage:.2f}%). "
        f"Severity: High: {severity_counts['High']}, Medium: {severity_counts['Medium']}, Low: {severity_counts['Low']}. "
        f"Top issues: {', '.join([f'{k} ({v})' for k, v in sorted(anomaly_types.items(), key=lambda x: x[1], reverse=True)[:3]])}. "
        "Investigate high-severity anomalies and review system processes."
    )
    anomalies_with_explanations = []
    for anomaly in anomalies:
        anomaly_with_explanation = anomaly.copy()
        anomaly_with_explanation["detailed_explanation"] = anomaly["explanation"]
        anomaly_with_explanation["feedback"] = "Review this anomaly for potential process improvement."
        anomalies_with_explanations.append(anomaly_with_explanation)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = {
        "report_title": "Restaurant Sales Data Audit Report (Simplified)",
        "generated_at": timestamp,
        "executive_summary": executive_summary,
        "audit_metrics": {
            "total_records_analyzed": total_records,
            "total_anomalies_detected": total_anomalies,
            "anomaly_percentage": f"{anomaly_percentage:.2f}%",
            "execution_time": execution_time,
        },
        "anomaly_type_breakdown": anomaly_types,
        "detailed_findings": anomalies_with_explanations,
    }
    return report

def save_report(report, output_format="pdf"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = "reports"
    os.makedirs(output_dir, exist_ok=True)
    
    if output_format.lower() == "json":
        filename = f"{output_dir}/anomaly_report_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        logger.info(f"Saved JSON report to {filename}")
        return filename
    
    elif output_format.lower() == "pdf":
        filename = f"{output_dir}/anomaly_report_{timestamp}.pdf"
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        # Title
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, report["report_title"], ln=True, align="C")
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 8, f"Generated at: {report['generated_at']}", ln=True, align="C")
        pdf.ln(8)
        
        # Executive Summary
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, "Executive Summary", ln=True)
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 6, report["executive_summary"])
        pdf.ln(8)
        
        # Audit Metrics
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, "Audit Metrics", ln=True)
        pdf.set_font("Arial", "", 10)
        metrics = report["audit_metrics"]
        pdf.cell(0, 6, f"Total Records: {metrics['total_records_analyzed']}", ln=True)
        pdf.cell(0, 6, f"Anomalies Detected: {metrics['total_anomalies_detected']}", ln=True)
        pdf.cell(0, 6, f"Anomaly Percentage: {metrics['anomaly_percentage']}", ln=True)
        pdf.cell(0, 6, f"Execution Time: {metrics['execution_time']}s", ln=True)
        pdf.ln(8)
        
        # Charts for Top 5 Anomaly Types
        top_anomalies = sorted(report["anomaly_type_breakdown"].items(), key=lambda x: x[1], reverse=True)[:5]
        anomaly_names, anomaly_counts = zip(*top_anomalies)
        plt.figure(figsize=(6, 3))
        plt.bar(anomaly_names, anomaly_counts, color='skyblue')
        plt.title("Top 5 Anomaly Types", fontsize=10)
        plt.xlabel("Anomaly Type", fontsize=8)
        plt.ylabel("Count", fontsize=8)
        plt.xticks(rotation=45, ha='right', fontsize=6)
        plt.tight_layout()
        chart_file = f"{output_dir}/anomaly_chart_{timestamp}.png"
        plt.savefig(chart_file, dpi=150)
        plt.close()
        
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, "Anomaly Distribution", ln=True)
        pdf.image(chart_file, x=10, y=None, w=190)
        pdf.ln(8)
        
        # Detailed Findings
        pdf.add_page()
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, "Detailed Findings", ln=True)
        pdf.set_font("Arial", "", 8)
        effective_width = pdf.w - 2 * pdf.l_margin  # Use page width minus margins
        for i, anomaly in enumerate(report["detailed_findings"], 1):
            pdf.cell(0, 6, f"{i}. {anomaly['anomaly_type']} (Severity: {anomaly['severity']})", ln=True)
            pdf.cell(0, 6, f"Invoice ID: {anomaly['invoice_id']}", ln=True)
            pdf.cell(0, 6, f"Timestamp: {anomaly['timestamp']}", ln=True)
            pdf.multi_cell(effective_width, 6, f"Description: {anomaly['detailed_explanation']}")
            # Preprocess feedback to ensure it wraps
            feedback = anomaly.get('feedback', 'No feedback available.')[:100]
            feedback = " ".join(feedback.split())  # Normalize spaces
            try:
                pdf.multi_cell(effective_width, 6, f"Feedback: {feedback.strip()}")
            except Exception as e:
                logger.warning(f"Failed to render feedback for anomaly {anomaly['invoice_id']}: {str(e)}")
                pdf.multi_cell(effective_width, 6, "Feedback: [Rendering error]")
            pdf.ln(4)
        
        pdf.output(filename)
        logger.info(f"Saved PDF report to {filename}")
        os.remove(chart_file)  # Clean up temporary chart file
        return filename
    
    else:
        logger.error(f"Unsupported output format: {output_format}")
        raise ValueError(f"Unsupported output format: {output_format}")
def main(input_file: str):
    try:
        df = pd.read_csv(input_file)
        logger.info(f"Loaded data from {input_file}")
        preprocessed_df = preprocess_data(df)
        anomaly_results = detect_anomalies(preprocessed_df)
        report = generate_rag_report(anomaly_results)
        pdf_file = save_report(report, output_format="pdf")
        logger.info("Pipeline completed successfully")
        return pdf_file
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        raise

if __name__ == "__main__":
    input_file = "./Hackathon_Dataset.csv"
    pdf_file = main(input_file)
    print(f"Generated PDF report at: {pdf_file}")