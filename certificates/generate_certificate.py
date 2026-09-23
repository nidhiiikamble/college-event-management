from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
import os


def generate_certificate(student_name, event_name, event_date):

    # Certificate folder
    certificate_folder = os.path.dirname(os.path.abspath(__file__))

    # File name
    safe_name = student_name.replace(" ", "_")
    output_path = os.path.join(
        certificate_folder,
        f"{safe_name}_Certificate.pdf"
    )

    # Page setup
    page_width, page_height = landscape(A4)

    pdf = canvas.Canvas(
        output_path,
        pagesize=(page_width, page_height)
    )

    # Background
    pdf.setFillColor(colors.whitesmoke)
    pdf.rect(
        0,
        0,
        page_width,
        page_height,
        fill=1,
        stroke=0
    )

    # Outer border
    pdf.setStrokeColor(colors.HexColor("#5143c7"))
    pdf.setLineWidth(6)
    pdf.rect(
        25,
        25,
        page_width - 50,
        page_height - 50,
        fill=0,
        stroke=1
    )

    # Inner border
    pdf.setStrokeColor(colors.HexColor("#6b5ce7"))
    pdf.setLineWidth(2)
    pdf.rect(
        40,
        40,
        page_width - 80,
        page_height - 80,
        fill=0,
        stroke=1
    )

    # Title
    pdf.setFillColor(colors.HexColor("#5143c7"))
    pdf.setFont("Helvetica-Bold", 32)

    pdf.drawCentredString(
        page_width / 2,
        page_height - 100,
        "CERTIFICATE OF PARTICIPATION"
    )

    # Subtitle
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica", 16)

    pdf.drawCentredString(
        page_width / 2,
        page_height - 140,
        "This certificate is proudly presented to"
    )

    # Student name
    pdf.setFillColor(colors.HexColor("#5143c7"))
    pdf.setFont("Helvetica-Bold", 28)

    pdf.drawCentredString(
        page_width / 2,
        page_height - 195,
        student_name
    )

    # Line under name
    pdf.setStrokeColor(colors.HexColor("#6b5ce7"))
    pdf.setLineWidth(1)

    pdf.line(
        180,
        page_height - 210,
        page_width - 180,
        page_height - 210
    )

    # Participation text
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica", 15)

    pdf.drawCentredString(
        page_width / 2,
        page_height - 250,
        "for successfully participating in"
    )

    # Event name
    pdf.setFillColor(colors.HexColor("#5143c7"))
    pdf.setFont("Helvetica-Bold", 22)

    pdf.drawCentredString(
        page_width / 2,
        page_height - 285,
        event_name
    )

    # Date
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica", 13)

    pdf.drawCentredString(
        page_width / 2,
        page_height - 325,
        f"Date: {event_date}"
    )

    # Signature section
    pdf.setFont("Helvetica", 12)

    pdf.line(150, 100, 320, 100)
    pdf.drawCentredString(235, 80, "Event Coordinator")

    pdf.line(page_width - 320, 100, page_width - 150, 100)
    pdf.drawCentredString(
        page_width - 235,
        80,
        "College Administration"
    )

    # Footer
    pdf.setFont("Helvetica-Oblique", 10)
    pdf.setFillColor(colors.grey)

    pdf.drawCentredString(
        page_width / 2,
        55,
        "College Event Management System"
    )

    # Save PDF
    pdf.save()

    print("Certificate generated successfully!")
    print(f"Saved at: {output_path}")


# ==============================
# SAMPLE CERTIFICATE
# ==============================

generate_certificate(
    student_name="Nidhi Kamble",
    event_name="AI Workshop",
    event_date="26 September 2026"
)