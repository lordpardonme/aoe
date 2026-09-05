import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

OUT = Path("Job Hunt/resumes/Mohd_Hayaat_Ali_GetYourGuide_Cover_Letter.pdf")

INK = colors.HexColor("#1A1A1A")
MUTED = colors.HexColor("#555555")
ACCENT = colors.HexColor("#FF5533") # GetYourGuide brand orange/red
RULE = colors.HexColor("#E5E5E5")
LINK = colors.HexColor("#FF5533")

base = getSampleStyleSheet()
styles = {
    "name": ParagraphStyle(
        "Name",
        parent=base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=INK,
        spaceAfter=2,
    ),
    "role": ParagraphStyle(
        "Role",
        parent=base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        textColor=ACCENT,
        spaceAfter=6,
    ),
    "contact": ParagraphStyle(
        "Contact",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=8.8,
        leading=12.5,
        textColor=MUTED,
        spaceAfter=2,
    ),
    "body": ParagraphStyle(
        "Body",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=9.4,
        leading=14.2,
        textColor=INK,
        spaceAfter=8,
    ),
    "subheading": ParagraphStyle(
        "Subheading",
        parent=base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        textColor=INK,
        spaceBefore=8,
        spaceAfter=4,
    ),
    "bullet": ParagraphStyle(
        "Bullet",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=9.1,
        leading=13.6,
        textColor=INK,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=4,
    ),
}

def linked(label, url):
    return f'<link href="{url}" color="#FF5533"><u>{label}</u></link>'

story = [
    Paragraph("Mohd Hayaat Ali", styles["name"]),
    Paragraph("SOCIAL VIDEO PRODUCER & CREATIVE DIRECTOR", styles["role"]),
    Paragraph(
        f'{linked("mohdhayaat1@outlook.com", "mailto:mohdhayaat1@outlook.com")}  |  '
        f'{linked("+91-7905194153", "tel:+917905194153")}  |  Delhi NCR, India (Available for Berlin Relocation)',
        styles["contact"],
    ),
    Paragraph(
        f'{linked("Portfolio: workofhayaat.framer.website", "https://workofhayaat.framer.website")}  |  '
        f'{linked("Creative Showreel (Google Drive)", "https://drive.google.com/drive/folders/1maf7S6y-WwfE3cdVNO8SvmM7H6slgpZW")}',
        styles["contact"],
    ),
    Paragraph("Target Role: Social Video Producer (Vertical Video) — GetYourGuide | Berlin, Germany", styles["contact"]),
    HRFlowable(width="100%", thickness=1, color=RULE, spaceBefore=4, spaceAfter=10),
    
    Paragraph("Dear GetYourGuide Editorial & Brand Marketing Team,", styles["body"]),
    
    Paragraph(
        "Great travel content isn't just about showing an iconic landmark—it’s about capturing the visceral feeling of "
        "stepping into an unfamiliar alleyway in Rome or tasting a local dish for the first time. On TikTok, Reels, and Shorts, "
        "that emotion has to land within the first two seconds, with platform-native pacing, sound design, and genuine human "
        "perspective that never feels like a commercial ad.",
        styles["body"],
    ),
    Paragraph(
        "I am a Video Producer, Director, and Visual Storyteller with 6+ years of hands-on experience owning full-cycle "
        "video production—from concepting, storyboarding, and on-location shooting to editing, sound design, and color grading "
        "in Premiere Pro and DaVinci Resolve.",
        styles["body"],
    ),
    
    Paragraph("<b>What I Bring to GetYourGuide’s Vertical Video Engine:</b>", styles["subheading"]),
    
    Paragraph(
        "-&nbsp;&nbsp;<b>Platform-Native Formats & Viral Retention (1M+ Views Shipped):</b> Conceptualized, shot, and edited "
        "campaign videos and vertical reels generating <b>10,00,000+ views</b> across digital channels. I understand the distinct "
        "grammar of each platform: authentic discovery hooks on TikTok, aesthetic cinematic immersion on Reels, and narrative curiosity on Shorts.",
        styles["bullet"],
    ),
    Paragraph(
        "-&nbsp;&nbsp;<b>Full End-to-End Production & Location Agility:</b> Fully self-sufficient on-camera—experienced operating "
        "mirrorless/cinema camera rigs, designing portable lighting setups, directing on-screen talent, and capturing spatial ambient audio. "
        "Comfortable managing European shoot logistics and scouting authentic local creators at pace.",
        styles["bullet"],
    ),
    Paragraph(
        "-&nbsp;&nbsp;<b>Repeatable Frameworks & Scalable Output:</b> Built scalable visual and content templates at Crevia across "
        "200+ product assets and brand video campaigns, establishing repeatable editing rhythms that allowed always-on publishing "
        "without sacrificing aesthetic polish. Passionate about establishing episodic, repeatable travel series for GYG.",
        styles["bullet"],
    ),
    Paragraph(
        "-&nbsp;&nbsp;<b>AI-Augmented Workflow & Data-Informed Craft:</b> Actively leverage modern AI tools for voice clean-up, "
        "automated caption timing, and rapid ideation. My cross-disciplinary UI/UX background gives me a rigorous, data-driven eye for "
        "audience drop-off points, pacing, and retention curves.",
        styles["bullet"],
    ),
    
    Paragraph("<b>Availability & Relocation:</b>", styles["subheading"]),
    Paragraph(
        "I am immediately available (0-day notice period), hold full qualification for the German EU Blue Card "
        "(<i>Fachkräfteeinwanderungsgesetz</i>), and am ready to relocate to Berlin and travel across Europe for productions. "
        "You can view my creative showreel and live work via the links above.",
        styles["body"],
    ),
    Paragraph(
        "I would welcome the opportunity to connect and discuss how we can scale GetYourGuide’s vertical video presence into "
        "the most inspiring travel engine on social.",
        styles["body"],
    ),
    Spacer(1, 6),
    Paragraph("Best regards,<br/><br/><b>Mohd Hayaat Ali</b>", styles["body"]),
]

doc = SimpleDocTemplate(
    str(OUT),
    pagesize=A4,
    leftMargin=0.7 * inch,
    rightMargin=0.7 * inch,
    topMargin=0.6 * inch,
    bottomMargin=0.6 * inch,
    title="Mohd Hayaat Ali - GetYourGuide Cover Letter",
    author="Mohd Hayaat Ali",
)
doc.build(story)
print(f"Cover Letter PDF generated: {OUT}")
