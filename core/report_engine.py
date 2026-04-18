import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, HRFlowable
)
from config import REPORTS_DIR

# Color scheme
BLUE = colors.HexColor("#2B5CE6")
LIGHT_BLUE = colors.HexColor("#F0F4FF")
DARK = colors.HexColor("#1A1A2E")
GRAY = colors.HexColor("#666666")
GREEN = colors.HexColor("#28A745")
RED = colors.HexColor("#DC3545")
ORANGE = colors.HexColor("#FFC107")
WHITE = colors.white

def get_score_color(score):
    if score >= 8:
        return GREEN
    elif score >= 5:
        return ORANGE
    else:
        return RED

def get_score_label(score):
    if score >= 8:
        return "Excellent"
    elif score >= 6:
        return "Good"
    elif score >= 4:
        return "Average"
    else:
        return "Needs Improvement"

def get_emotion_emoji(emotion):
    emoji_map = {
        "happy": "😊 Happy",
        "sad": "😢 Sad",
        "angry": "😠 Angry",
        "fear": "😨 Nervous",
        "surprise": "😲 Surprised",
        "disgust": "😒 Disgust",
        "neutral": "😐 Neutral",
        "confused": "😕 Confused"
    }
    return emoji_map.get(emotion, "😐 Neutral")

def generate_report(report_data):
    """Generate PDF report from session data."""
    os.makedirs(REPORTS_DIR, exist_ok=True)

    # File name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    domain_clean = report_data["domain"].replace(" ", "_").replace("&", "and")
    filename = f"PrepAI_Report_{domain_clean}_{timestamp}.pdf"
    filepath = os.path.join(REPORTS_DIR, filename)

    # Create document
    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    # Styles
    styles = getSampleStyleSheet()
    style_normal = ParagraphStyle(
        "Normal",
        fontName="Helvetica",
        fontSize=10,
        textColor=DARK,
        leading=14
    )
    style_bold = ParagraphStyle(
        "Bold",
        fontName="Helvetica-Bold",
        fontSize=10,
        textColor=DARK,
        leading=14
    )
    style_heading = ParagraphStyle(
        "Heading",
        fontName="Helvetica-Bold",
        fontSize=13,
        textColor=BLUE,
        leading=18
    )
    style_subheading = ParagraphStyle(
        "Subheading",
        fontName="Helvetica-Bold",
        fontSize=11,
        textColor=DARK,
        leading=16
    )
    style_small = ParagraphStyle(
        "Small",
        fontName="Helvetica",
        fontSize=9,
        textColor=GRAY,
        leading=12
    )

    elements = []

    # ── Header ───────────────────────────────
    header_data = [[
        Paragraph("<font color='#2B5CE6' size='20'><b>PrepAI</b></font>", styles["Normal"]),
        Paragraph(
            "<font color='#666666' size='9'>AI Mock Interview Assistant<br/>by Clonigue</font>",
            styles["Normal"]
        )
    ]]
    header_table = Table(header_data, colWidths=[3*inch, 4.5*inch])
    header_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (0, 0), "LEFT"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    elements.append(header_table)
    elements.append(HRFlowable(width="100%", thickness=2, color=BLUE))
    elements.append(Spacer(1, 15))

    # ── Report Title ─────────────────────────
    elements.append(Paragraph("Interview Performance Report", style_heading))
    elements.append(Spacer(1, 10))

    # ── Session Info ─────────────────────────
    scored_answers = report_data.get("scored_answers", [])
    total = len(scored_answers)
    avg_score = round(
        sum(a["score"] for a in scored_answers) / total, 1
    ) if total > 0 else 0
    dominant_emotion = report_data.get("dominant_emotion", "neutral")
    date_str = datetime.now().strftime("%B %d, %Y  %I:%M %p")

    info_data = [
        ["Domain", report_data["domain"],
         "Date", date_str],
        ["Total Questions", str(total),
         "Average Score", f"{avg_score} / 10"],
        ["Overall Rating", get_score_label(avg_score),
         "Dominant Emotion", get_emotion_emoji(dominant_emotion)],
    ]
    info_table = Table(info_data, colWidths=[1.5*inch, 2.5*inch, 1.5*inch, 2*inch])
    info_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), LIGHT_BLUE),
        ("BACKGROUND", (2, 0), (2, -1), LIGHT_BLUE),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D0D8F0")),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [WHITE, colors.HexColor("#F8F9FF")]),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 20))

    # ── Score Summary Bar ────────────────────
    elements.append(Paragraph("Performance Overview", style_heading))
    elements.append(Spacer(1, 8))

    summary_data = [["Q#", "Question", "Score", "Rating"]]
    for item in scored_answers:
        summary_data.append([
            str(item["question_num"]),
            Paragraph(item["question"][:80] + "..." if len(item["question"]) > 80
                     else item["question"], style_small),
            str(item["score"]) + "/10",
            get_score_label(item["score"])
        ])

    summary_table = Table(
        summary_data,
        colWidths=[0.4*inch, 3.8*inch, 0.8*inch, 1.5*inch]
    )
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLUE),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("ALIGN", (1, 0), (1, -1), "LEFT"),
        ("PADDING", (0, 0), (-1, -1), 7),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D0D8F0")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, colors.HexColor("#F8F9FF")]),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 20))

    # ── Detailed Q&A ─────────────────────────
    elements.append(Paragraph("Detailed Question Analysis", style_heading))
    elements.append(Spacer(1, 8))

    for item in scored_answers:
        # Question header
        q_header = [[
            Paragraph(
                f"<b>Q{item['question_num']}.</b> {item['question']}",
                style_bold
            ),
            Paragraph(
                f"<font color='#2B5CE6'><b>{item['score']}/10</b></font>",
                style_bold
            )
        ]]
        q_table = Table(q_header, colWidths=[5.5*inch, 1*inch])
        q_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BLUE),
            ("PADDING", (0, 0), (-1, -1), 8),
            ("ALIGN", (1, 0), (1, 0), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        elements.append(q_table)

        # Answer
        answer_text = item["answer"] if item["answer"] else "No answer provided"
        detail_data = [
            [Paragraph("<b>Your Answer:</b>", style_bold),
             Paragraph(answer_text, style_normal)],
            [Paragraph("<b>Feedback:</b>", style_bold),
             Paragraph(item["feedback"], style_normal)],
            [Paragraph("<b>Ideal Answer:</b>", style_bold),
             Paragraph(item["ideal_answer"], style_normal)],
        ]
        detail_table = Table(detail_data, colWidths=[1.2*inch, 5.3*inch])
        detail_table.setStyle(TableStyle([
            ("PADDING", (0, 0), (-1, -1), 6),
            ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#E0E8FF")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ROWBACKGROUNDS", (0, 0), (-1, -1),
             [WHITE, colors.HexColor("#FAFBFF"), WHITE]),
        ]))
        elements.append(detail_table)
        elements.append(Spacer(1, 10))

    # ── Emotion Analysis ─────────────────────
    elements.append(HRFlowable(width="100%", thickness=1, color=BLUE))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Emotional Analysis", style_heading))
    elements.append(Spacer(1, 8))

    emotion_log = report_data.get("emotion_log", [])
    if emotion_log:
        emotion_counts = {}
        for entry in emotion_log:
            e = entry["emotion"]
            emotion_counts[e] = emotion_counts.get(e, 0) + 1

        total_frames = sum(emotion_counts.values())
        emotion_data = [["Emotion", "Frequency", "Percentage"]]
        for emotion, count in sorted(
            emotion_counts.items(), key=lambda x: x[1], reverse=True
        ):
            pct = round(count / total_frames * 100, 1)
            emotion_data.append([
                get_emotion_emoji(emotion),
                str(count),
                f"{pct}%"
            ])

        emotion_table = Table(
            emotion_data,
            colWidths=[2.5*inch, 2*inch, 2*inch]
        )
        emotion_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), BLUE),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("PADDING", (0, 0), (-1, -1), 7),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D0D8F0")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [WHITE, colors.HexColor("#F8F9FF")]),
        ]))
        elements.append(emotion_table)
    else:
        elements.append(Paragraph("No emotion data recorded.", style_normal))

    elements.append(Spacer(1, 20))

    # ── Final Recommendation ─────────────────
    elements.append(HRFlowable(width="100%", thickness=1, color=BLUE))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Overall Recommendation", style_heading))
    elements.append(Spacer(1, 8))

    if avg_score >= 8:
        recommendation = (
            "Outstanding performance! You demonstrated excellent knowledge "
            "and communication skills. You are well prepared for this type "
            "of interview. Keep up the great work!"
        )
    elif avg_score >= 6:
        recommendation = (
            "Good performance! You showed solid understanding of the topics. "
            "Focus on providing more detailed answers and concrete examples "
            "to further strengthen your responses."
        )
    elif avg_score >= 4:
        recommendation = (
            "Average performance. You have a basic understanding but need "
            "to deepen your knowledge. Practice more, revisit core concepts "
            "and work on structuring your answers clearly."
        )
    else:
        recommendation = (
            "You need significant improvement in this domain. Don't be "
            "discouraged — focus on studying the fundamentals, practice "
            "regularly with PrepAI and track your progress over time."
        )

    rec_data = [[Paragraph(recommendation, style_normal)]]
    rec_table = Table(rec_data, colWidths=[6.5*inch])
    rec_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BLUE),
        ("PADDING", (0, 0), (-1, -1), 12),
        ("ROUNDEDCORNERS", [8]),
    ]))
    elements.append(rec_table)
    elements.append(Spacer(1, 20))

    # ── Footer ───────────────────────────────
    elements.append(HRFlowable(width="100%", thickness=1,
                               color=colors.HexColor("#D0D8F0")))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(
        f"Generated by PrepAI v1.0 by Clonigue  •  {date_str}",
        style_small
    ))

    # Build PDF
    doc.build(elements)
    return filepath