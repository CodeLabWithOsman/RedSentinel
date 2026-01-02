import os
from datetime import datetime
import matplotlib.pyplot as plt
from collections import Counter


# ===============================
# Intelligence helpers
# ===============================

def infer_severity(f):
    f = f.lower()
    if any(x in f for x in ["rce", "critical", "sql"]):
        return "High"
    if any(x in f for x in ["xss", "csrf", "open port"]):
        return "Medium"
    return "Low"


def infer_cvss(f):
    return {"High": 8.6, "Medium": 5.4, "Low": 2.3}[infer_severity(f)]


def infer_mitre(f):
    f = f.lower()
    if "xss" in f:
        return "T1059"
    if "open port" in f:
        return "T1046"
    return "T1082"


def infer_owasp(f):
    f = f.lower()
    if "xss" in f:
        return "A03:2021 – Injection"
    if "header" in f or "open port" in f:
        return "A05:2021 – Security Misconfiguration"
    return "A09:2021 – Logging & Monitoring"


def remediation_for(f):
    f = f.lower()
    if "x-frame-options" in f:
        return "Implement X-Frame-Options to mitigate clickjacking."
    if "content-type-options" in f:
        return "Add X-Content-Type-Options: nosniff."
    if "open port" in f:
        return "Restrict exposed ports via firewall rules."
    return "Apply OWASP hardening best practices."


# ===============================
# Charts
# ===============================

def generate_charts(findings, assets_dir):
    severities = [f["severity"] for f in findings]
    cvss = [f["cvss"] for f in findings]

    os.makedirs(assets_dir, exist_ok=True)

    sev_counts = Counter(severities)
    plt.figure()
    plt.bar(sev_counts.keys(), sev_counts.values())
    plt.title("Severity Distribution")
    sev_path = os.path.join(assets_dir, "severity_chart.png")
    plt.savefig(sev_path)
    plt.close()

    plt.figure()
    plt.hist(cvss, bins=5)
    plt.title("CVSS Score Distribution")
    cvss_path = os.path.join(assets_dir, "cvss_histogram.png")
    plt.savefig(cvss_path)
    plt.close()

    return sev_path, cvss_path


# ===============================
# Executive Summary
# ===============================

def executive_summary(target, findings):
    h = len([f for f in findings if f["severity"] == "High"])
    m = len([f for f in findings if f["severity"] == "Medium"])

    return f"""
RedSentinel conducted a security assessment of {target} to identify
potential vulnerabilities and misconfigurations.

The assessment identified {h} high-risk and {m} medium-risk issues.
High-risk findings may allow unauthorized access or compromise
and should be prioritized for remediation.

This report provides a risk-based overview to support informed
security and business decisions.
"""


# ===============================
# Core Report Generator
# ===============================

def normalize_findings(results):
    out = []
    for category, items in results.items():
        for f in items:
            out.append({
                "category": category,
                "title": f,
                "severity": infer_severity(f),
                "cvss": infer_cvss(f),
                "mitre": infer_mitre(f),
                "owasp": infer_owasp(f),
                "remediation": remediation_for(f)
            })
    return out


def generate_html_report(STATE):
    target = STATE["target"]
    results = STATE["simulation"]
    heatmap = STATE.get("heatmap")

    findings = normalize_findings(results)
    findings_sorted = sorted(findings, key=lambda x: x["cvss"], reverse=True)
    top5 = findings_sorted[:5]

    assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
    sev_chart, cvss_chart = generate_charts(findings, assets_dir)

    logo = os.path.join(assets_dir, "logo.png")
    logo_html = f'<img src="{logo}" width="120">' if os.path.exists(logo) else ""

    filename = f"RedSentinel_Report_{target.replace('.', '_')}.html"
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    def row(f):
        color = {"High":"#c0392b","Medium":"#f39c12","Low":"#27ae60"}[f["severity"]]
        return f"""
        <tr>
        <td>{f["category"]}</td>
        <td>{f["title"]}</td>
        <td style="background:{color};color:white">{f["severity"]}</td>
        <td>{f["cvss"]}</td>
        <td>{f["owasp"]}</td>
        <td>{f["mitre"]}</td>
        <td>{f["remediation"]}</td>
        </tr>
        """

    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>RedSentinel Report</title>
<style>
body {{ font-family: Arial; margin:40px }}
h1 {{ color:#b30000 }}
table {{ border-collapse:collapse; width:100% }}
th,td {{ border:1px solid #ccc; padding:8px }}
th {{ background:#eee }}
.pagebreak {{ page-break-before: always }}
</style>
</head>

<body>

<!-- COVER PAGE -->
<center>
{logo_html}
<h1>RedSentinel</h1>
<h3>Security Assessment Report</h3>
<p><b>Target:</b> {target}</p>
<p><b>Consultant:</b> Hackura Project</p>
<p><b>Date:</b> {now}</p>
</center>

<p style="margin-top:60px">
<b>Disclaimer:</b> This report contains results from real automated security
testing and is provided for educational and risk assessment purposes.
</p>

<div class="pagebreak"></div>

<h2>Executive Summary</h2>
<p>{executive_summary(target, findings)}</p>

<div class="pagebreak"></div>

<h2>Top 5 Risks</h2>
<table>
<tr><th>Category</th><th>Finding</th><th>Severity</th><th>CVSS</th><th>OWASP</th><th>MITRE</th><th>Remediation</th></tr>
{"".join(row(f) for f in top5)}
</table>

<div class="pagebreak"></div>

<h2>Risk Acceptance & Management Sign-Off</h2>

<p>
Management acknowledges the security risks identified in this report and
accepts responsibility for remediation decisions based on business priorities,
risk appetite, and operational constraints.
</p>

<p>
Any accepted risks should be formally documented, reviewed periodically, and
reassessed following significant system changes.
</p>

<table>
<tr><th>Risk Acceptance Decision</th><th>Justification</th></tr>
<tr><td>☐ Accepted ☐ Mitigated ☐ Deferred</td><td>&nbsp;</td></tr>
</table>

<br>

<table>
<tr><th>Management Representative</th><th>Details</th></tr>
<tr><td>Name</td><td>&nbsp;</td></tr>
<tr><td>Role / Title</td><td>&nbsp;</td></tr>
<tr><td>Signature</td><td>&nbsp;</td></tr>
<tr><td>Date</td><td>&nbsp;</td></tr>
</table>

<div class="pagebreak"></div>

<h2>Risk Visualization</h2>
<img src="{sev_chart}" width="45%">
<img src="{cvss_chart}" width="45%">

<div class="pagebreak"></div>

<h2>All Findings</h2>
<table>
<tr><th>Category</th><th>Finding</th><th>Severity</th><th>CVSS</th><th>OWASP</th><th>MITRE</th><th>Remediation</th></tr>
{"".join(row(f) for f in findings_sorted)}
</table>

</body>
</html>
"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[+] HTML report generated: {filename}")
    return filename

