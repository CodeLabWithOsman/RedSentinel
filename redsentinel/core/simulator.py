import subprocess
import os

from redsentinel.core.state import STATE
from redsentinel.core.risk_heatmap import generate_risk_heatmap
from redsentinel.core.html_reporter import generate_html_report


# ---------------- SAFE COMMAND RUNNER ----------------
def run_command(cmd: list, timeout: int = 120):
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=timeout
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return "[!] Scan timed out"
    except KeyboardInterrupt:
        return "[!] Scan interrupted by user"


# ---------------- MAIN SIMULATION ----------------
def simulate_scan(target: str):
    print(f"\n[+] Simulating vulnerability discovery for: {target}\n")

    results = {}

    # ---------- PORT & SERVICE DISCOVERY ----------
    nmap_cmd = ["nmap", "-F", "-Pn", "--open", target]
    nmap_out = run_command(nmap_cmd, timeout=90)
    results["network"] = parse_nmap(nmap_out)

    # ---------- WEB TECHNOLOGY FINGERPRINT ----------
    whatweb_cmd = ["whatweb", "--no-errors", target]
    whatweb_out = run_command(whatweb_cmd, timeout=60)
    results["web_stack"] = parse_whatweb(whatweb_out)

    # ---------- WEB MISCONFIGURATION CHECK ----------
    nikto_cmd = [
        "nikto",
        "-h", target,
        "-Tuning", "x",
        "-nointeractive",
        "-timeout", "10"
    ]
    nikto_out = run_command(nikto_cmd, timeout=120)
    results["web_issues"] = parse_nikto(nikto_out)

    # ---------- SAVE STATE ----------
    STATE["simulation"] = results

    # ---------- RISK HEAT MAP ----------
    all_findings = []
    for category in results.values():
        all_findings.extend(category)

    assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
    heatmap_path = generate_risk_heatmap(all_findings, assets_dir)
    STATE["heatmap"] = heatmap_path

    print("[+] Simulation completed\n")

    # ---------- GENERATE REPORT ----------
    generate_html_report(STATE)


# ================= PARSERS =================

def parse_nmap(output: str):
    findings = []

    if output.startswith("[!]"):
        return [output]

    for line in output.splitlines():
        if "/tcp" in line and "open" in line:
            findings.append(f"Open port detected: {line.strip()}")

    return findings


def parse_whatweb(output: str):
    findings = []
    l = output.lower()

    if "apache" in l:
        findings.append("Apache web server detected")
    if "nginx" in l:
        findings.append("Nginx web server detected")
    if "php" in l:
        findings.append("PHP technology detected")
    if "wordpress" in l:
        findings.append("WordPress CMS detected")
    if "cloudflare" in l:
        findings.append("Cloudflare protection detected")

    return findings


def parse_nikto(output: str):
    findings = []

    if output.startswith("[!]"):
        return [output]

    for line in output.splitlines():
        l = line.lower()

        if "x-frame-options" in l:
            findings.append("Missing X-Frame-Options header")
        if "x-content-type-options" in l:
            findings.append("Missing X-Content-Type-Options header")
        if "content-security-policy" in l:
            findings.append("Missing Content-Security-Policy header")
        if "server:" in l:
            findings.append("Server version disclosure")

    return findings

