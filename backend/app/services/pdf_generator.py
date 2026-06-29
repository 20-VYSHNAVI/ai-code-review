from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import io

def generate_pdf_report(review_data: dict, username: str) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    title = Paragraph("AI Code Review Report", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 0.2*inch))

    info = Paragraph(f"Reviewed by: {username} | File: {review_data.get('filename', 'code.py')}", styles['Normal'])
    story.append(info)
    story.append(Spacer(1, 0.2*inch))

    scores = review_data.get('scores', {})
    score_data = [
        ['Metric', 'Score'],
        ['Quality', str(scores.get('quality', 0))],
        ['Security', str(scores.get('security', 0))],
        ['Readability', str(scores.get('readability', 0))],
        ['Overall', str(scores.get('overall', 0))],
    ]
    score_table = Table(score_data, colWidths=[3*inch, 2*inch])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 0.2*inch))

    severity = review_data.get('severity', 'Unknown')
    sev_para = Paragraph(f"Severity Level: {severity}", styles['Heading2'])
    story.append(sev_para)
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("Issues Found", styles['Heading2']))
    for issue in review_data.get('issues', []):
        story.append(Paragraph(f"• {issue}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("Suggestions", styles['Heading2']))
    for suggestion in review_data.get('suggestions', []):
        story.append(Paragraph(f"• {suggestion}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("Learning Tips", styles['Heading2']))
    for tip in review_data.get('learning_tips', []):
        story.append(Paragraph(f"• {tip}", styles['Normal']))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()