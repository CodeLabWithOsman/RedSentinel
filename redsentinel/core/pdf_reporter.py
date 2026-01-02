import os
from weasyprint import HTML, CSS


def generate_pdf_report(html_path: str):
    """
    Convert an HTML report into a professional PDF using WeasyPrint
    """

    if not os.path.exists(html_path):
        raise FileNotFoundError(f"HTML report not found: {html_path}")

    pdf_path = html_path.replace(".html", ".pdf")

    print("[*] Converting HTML report to PDF...")

    css = CSS(string="""
        @page {
            size: A4;
            margin: 20mm;
        }

        body {
            font-family: Arial, sans-serif;
        }

        h1, h2, h3 {
            color: #c0392b;
        }

        table {
            page-break-inside: avoid;
        }

        img {
            max-width: 100%;
        }
    """)

    HTML(filename=html_path).write_pdf(
        pdf_path,
        stylesheets=[css]
    )

    print(f"[+] PDF report generated: {pdf_path}")

    return pdf_path

