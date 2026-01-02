# ============================================================
# RedSentinel Finding Normalizer
# ============================================================

from typing import Dict, List
from redsentinel.core.compliance_map import map_compliance


def normalize_findings(raw_findings: Dict[str, List[dict]]) -> Dict[str, List[dict]]:
    """
    Converts raw tool output into auditor-ready findings.
    Filters low-confidence noise and enriches data.
    """

    normalized: Dict[str, List[dict]] = {}

    for tool, findings in raw_findings.items():
        for f in findings:
            confidence = f.get("confidence", 0)

            # ---- Confidence-based filtering ----
            if confidence < 0.5:
                continue

            title = generate_title(f["data"])
            evidence = f["data"]
            severity = f["severity"]
            cvss = f["cvss"]

            normalized_finding = {
                "tool": tool,
                "title": title,
                "severity": severity,
                "cvss": cvss,
                "confidence": confidence,
                "evidence": evidence,
                "recommendation": generate_recommendation(title),
                "compliance": map_compliance(title)
            }

            category = severity.capitalize()

            normalized.setdefault(category, []).append(normalized_finding)

    return normalized


# =========================
# Helpers
# =========================

def generate_title(raw_text: str) -> str:
    text = raw_text.lower()

    if "open port" in text or "/tcp open" in text:
        return "Unrestricted Open Network Port Detected"

    if "x-frame-options" in text:
        return "Missing Clickjacking Protection Header"

    if "x-content-type-options" in text:
        return "Missing MIME Type Protection Header"

    if "ssl" in text or "tls" in text:
        return "Weak or Deprecated TLS Configuration"

    if "http" in text and "200" in text:
        return "Publicly Accessible HTTP Service Detected"

    return "General Security Observation"


def generate_recommendation(title: str) -> str:
    if "Open Network Port" in title:
        return (
            "Restrict exposed ports using firewall rules. "
            "Close any ports that are not strictly required."
        )

    if "Clickjacking" in title:
        return (
            "Implement the X-Frame-Options or Content-Security-Policy "
            "frame-ancestors directive to prevent UI redressing attacks."
        )

    if "MIME" in title:
        return (
            "Enable the X-Content-Type-Options header with the value 'nosniff' "
            "to prevent content-type confusion attacks."
        )

    if "TLS" in title:
        return (
            "Disable weak TLS protocols and ciphers. "
            "Enforce TLS 1.2 or higher with strong cipher suites."
        )

    return (
        "Review this finding and apply security best practices "
        "appropriate to the affected component."
    )

