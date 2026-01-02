# ============================================================
# src/redsentinel/core/html_reporter.py
# ============================================================

import os
from datetime import datetime
from statistics import mean


# =========================
# Executive Risk Scoring
# =========================

def calculate_executive_risk_score(findings: dict) -> float:
    """
    Produces a single executive-friendly risk score (0–10)
    based on CVSS scores and confidence.
    """
    scores = []

    for tool_findings in findings.values():
        for f in tool_findings:
            cvss = f.get("cvss", 0)
            confidence = f.get("confidence", 0.5)
            scores.append(cvss * confidence)

    if not scores:
        return 0.0

    return round(min(10.0, mean(scores)), 2)


# =========================
# CVSS Vector Generator
# =========================

def generate_cvss_vector(severity: str) -> str:
    """
    Simplified CVSS v3.1 vectors (educational but auditor-friendly)
    """
    vectors = {
        "CRITICAL": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",
        "HIGH":     "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L",
        "MEDIUM":   "CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:L/I:L/A:N",
        "LOW":      "CVSS:3.1/AV:L/AC:H/PR:H/UI:R/S:U/C:N/I:L/A:N",
        "INFO":     "CVSS:3.1/AV:L/AC:H/PR:H/UI:R/S:U/C:N/I:N/A:N",
    }
    return vectors.get(severity.upper(), "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:N")


# =========================
# HTML Report Generator
# =========================

def generate_html_report(
    target: str,
    findings: dict,
    normalized_findings: dict,
    remediation_roadmap: str,
    heatmap_path: str | None = None,
    output_dir: str = "reports",
) -> str:

    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    filename = f"report_{target.replace('.', '_')}.html"
    output_path = os.path.join(output_dir, filename)

    exec_risk_score = calculate_executive_risk_score(findings)

    # -------------------------
    # HTML CONTENT
    # -------------------------

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>RedSentinel Security Assessment</title>
<style>
body {{
    font-family: Arial, sans-serif;
    margin: 40px;
    color: #222;
}}
h1, h2, h3 {{
    color: #8b0000;
}}
table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 15px;
}}
th, td {{
    border: 1px solid #ccc;
    padding: 8px;
}}
th {{
    background-color: #f4f4f4;
}}
.sev-CRITICAL {{ color: darkred; font-weight: bold; }}
.sev-HIGH {{ color: red; font-weight: bold; }}
.sev-MEDIUM {{ color: orange; }}
.sev-LOW {{ color: green; }}
.sev-INFO {{ color: gray; }}
.footer {{
    margin-top: 60px;
    font-size: 0.9em;
    color: #555;
}}
.watermark {{
    position: fixed;
    top: 40%;
    left: 20%;
    font-size: 80px;
    color: rgba(200, 200, 200, 0.1);
    transform: rotate(-30deg);
    z-index: -1;
}}
</style>
</head>

<body>

<div class="watermark">RedSentinel</div>

<h1>Security Assessment Report</h1>

<p><strong>Target:</strong> {target}<br>
<strong>Generated:</strong> {timestamp}</p>

<hr>

<h2>Executive Summary</h2>

<p>
This report presents the results of a non-intrusive security assessment
conducted using automated discovery and analysis tools.
The goal is to identify exposed services, observable technologies,
and common security weaknesses.
</p>

<p>
<strong>Executive Risk Score:</strong>
<span class="sev-HIGH">{exec_risk_score} / 10</span>
</p>

<p>
The Executive Risk Score represents the overall security posture of the target,
considering severity, likelihood, and confidence of findings.
Scores above <strong>7.0</strong> indicate a high priority for remediation.
</p>

<hr>

<h2>Risk Heatmap</h2>
"""

    if heatmap_path:
        html += f'<img src="{heatmap_path}" width="600">'

    html += """
<hr>

<h2>Technical Findings</h2>
"""

    for category, items in normalized_findings.items():
        html += f"<h3>{category}</h3>"
        html += """
<table>
<tr>
<th>Finding</th>
<th>Severity</th>
<th>CVSS</th>
<th>CVSS Vector</th>
<th>Confidence</th>
<th>Evidence</th>
<th>Recommendation</th>
</tr>
"""
        for f in items:
            sev = f["severity"]
            vector = generate_cvss_vector(sev)

            html += f"""
<tr>
<td>{f['title']}</td>
<td class="sev-{sev}">{sev}</td>
<td>{f['cvss']}</td>
<td><code>{vector}</code></td>
<td>{f['confidence']}</td>
<td>{f['evidence']}</td>
<td>{f['recommendation']}</td>
</tr>
"""
        html += "</table>"

    html += f"""
<hr>

<h2>AI-Generated Remediation Roadmap</h2>

<p>
The following remediation guidance was generated to assist technical
and non-technical stakeholders in prioritizing corrective actions.
</p>

<pre>{remediation_roadmap}</pre>

<hr>

<h2>Risk Acceptance</h2>

<p>
Any risks not immediately remediated should be formally accepted
by business stakeholders after evaluating operational impact,
likelihood of exploitation, and regulatory requirements.
</p>

<hr>

<h2>Consultant Sign-Off</h2>

<p>
This assessment was conducted for educational and defensive purposes
using RedSentinel.
</p>

<p>
<strong>Assessor:</strong> ___________________________<br>
<strong>Date:</strong> ___________________________
</p>

<div class="footer">
Generated by RedSentinel – AI-Assisted Security Analysis
</div>

</body>
</html>
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return output_path

