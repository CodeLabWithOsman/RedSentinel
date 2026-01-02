import os
from weasyprint import HTML


def generate_pdf_report(html_path: str) -> str | None:
    """
    Generates PDF from HTML using WeasyPrint
    """

    if not html_path or not os.path.exists(html_path):
        print("[!] Invalid HTML path, skipping PDF generation")
        return None

    pdf_path = html_path.replace(".html", ".pdf")

    try:
        HTML(filename=html_path, base_url=os.getcwd()).write_pdf(pdf_path)
        print(f"[+] PDF report generated: {pdf_path}")
        return pdf_path
    except Exception as e:
        print(f"[!] PDF generation failed: {e}")
        return None

