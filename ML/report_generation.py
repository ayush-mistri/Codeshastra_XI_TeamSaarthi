from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime
import matplotlib.pyplot as plt
import io
import pandas as pd


def generate_graphs(anomalies, output_dir="graphs"):
    """Generate graphs for the report."""
    type_counts = pd.Series([anom.get('type', 'Unknown') for anom in anomalies]).value_counts()
    plt.figure(figsize=(8, 4))
    type_counts.plot(kind='bar', color='skyblue')
    plt.title("Anomaly Types Distribution")
    plt.xlabel("Type")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    type_bar_path = f"{output_dir}/anomaly_types.png"
    plt.savefig(type_bar_path, bbox_inches='tight')
    plt.close()

    severities = [anom.get('severity', 0) for anom in anomalies]
    plt.figure(figsize=(8, 4))
    plt.hist(severities, bins=20, color='salmon')
    plt.title("Severity Score Distribution")
    plt.xlabel("Severity")
    plt.ylabel("Frequency")
    severity_hist_path = f"{output_dir}/severity_dist.png"
    plt.savefig(severity_hist_path, bbox_inches='tight')
    plt.close()

    return type_bar_path, severity_hist_path


def generate_pdf_report(anomalies, output_path="audit_report.pdf"):
    """Generate a polished PDF audit report."""
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph("Sales Data Audit Report", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d')}", styles['Normal']))
    elements.append(Spacer(1, 24))

    # Executive Summary
    total_anomalies = len(anomalies)
    type_counts = pd.Series([anom.get('type', 'Unknown') for anom in anomalies]).value_counts().to_dict()
    high_priority = sum(1 for a in anomalies if a.get('severity', 0) > 75)
    summary_text = f"Executive Summary:\n" \
                   f"Total Anomalies: {total_anomalies}\n" \
                   f"High Priority (>75 Severity): {high_priority}\n" \
                   f"Anomaly Types:\n" + "\n".join([f"- {k}: {v}" for k, v in type_counts.items()]) + "\n" \
                                                                                                      f"Recommendation: Prioritize high-severity anomalies for immediate action."
    elements.append(Paragraph(summary_text, styles['Normal']))
    elements.append(Spacer(1, 24))

    # Graphs
    type_bar_path, severity_hist_path = generate_graphs(anomalies)
    elements.append(Paragraph("Visual Analysis", styles['Heading2']))
    elements.append(Image(type_bar_path, width=400, height=200))
    elements.append(Spacer(1, 12))
    elements.append(Image(severity_hist_path, width=400, height=200))
    elements.append(Spacer(1, 24))

    # Detailed Table
    elements.append(Paragraph("Top 25 Anomalies by Severity", styles['Heading2']))
    data = [["Line", "Type", "Column/Method", "Issue", "Count", "Severity", "Explanation"]]
    for anom in anomalies[:25]:
        data.append([
            str(anom.get('line_number', 'N/A')),
            anom.get('type', 'Unknown'),
            anom.get('column', anom.get('type', 'N/A')),
            anom.get('issue', 'Unknown'),
            str(anom.get('count', 1)),
            f"{anom.get('severity', 0):.1f}",
            anom.get('explanation', 'No explanation available')[:150] + "..." if len(
                anom.get('explanation', '')) > 150 else anom.get('explanation', 'No explanation available')
        ])

    table = Table(data, colWidths=[50, 70, 80, 80, 50, 50, 200])
    table.setStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    elements.append(table)

    doc.build(elements)
    print(f"Enhanced PDF report generated and saved to {output_path}")