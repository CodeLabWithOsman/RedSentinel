import os
from datetime import datetime


REPORT_DIR = "reports"


def ensure_report_dir():
    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)


def generate_report(
    target: str,
    analysis_results: list,
    simulations: list,
    plan: list
):
    """
    Generate a professional Markdown red team report.
    """

    ensure_report_dir()

    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{REPORT_DIR}/RedSentinel_Report_{target}_{timestamp}.md"

    with open(filename, "w") as f:
        # ---------------- HEADER ----------------
        f.write(f"# Red Team Assessment Report\n\n")
        f.write(f"**Target:** {target}\n\n")
        f.write(f"**Date:** {datetime.utcnow().strftime('%Y-%m-%d')}\n")
        f.write(f"**Framework:** RedSentinel (AI-Assisted)\n\n")
        f.write("---\n\n")

        # ---------------- EXEC SUMMARY ----------------
        f.write("## Executive Summary\n\n")
        f.write(
            "This assessment identifies security weaknesses based on "
            "static analysis and safe exploit simulations. No active "
            "exploitation was performed.\n\n"
        )

        # ---------------- FINDINGS ----------------
        f.write("## Findings\n\n")
        if not analysis_results:
            f.write("- No findings provided\n\n")
        else:
            for item in analysis_results:
                f.write(f"- {item}\n")
            f.write("\n")

        # ---------------- EXPLOIT SIMULATIONS ----------------
        f.write("## Exploit Simulations (Safe)\n\n")
        if not simulations:
            f.write("- No simulations executed\n\n")
        else:
            for sim in simulations:
                f.write(f"- {sim}\n")
            f.write("\n")

        # ---------------- ATTACK PLAN ----------------
        f.write("## Red Team Attack Plan (Theoretical)\n\n")
        if not plan:
            f.write("- No attack plan generated\n\n")
        else:
            for step in plan:
                f.write(f"- {step}\n")
            f.write("\n")

        # ---------------- REMEDIATION ----------------
        f.write("## Remediation Summary\n\n")
        f.write(
            "- Implement missing security headers\n"
            "- Monitor authentication failures\n"
            "- Improve logging and alerting\n"
            "- Perform periodic security testing\n\n"
        )

        # ---------------- DISCLAIMER ----------------
        f.write("---\n\n")
        f.write(
            "**Disclaimer:** This report is for educational and authorized "
            "security testing purposes only. No exploitation was performed.\n"
        )

    return filename

