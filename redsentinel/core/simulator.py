import subprocess
from redsentinel.core.state import STATE


def run_command(cmd: list):
    """Run external command safely and return output"""
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=300
        )
        return result.stdout
    except Exception as e:
        return f"ERROR: {e}"


def simulate_scan(target: str):
    """
    Simulate vulnerability discovery using common recon tools:
    - nmap
    - whatweb
    - nikto
    """

    print(f"\n[+] Starting vulnerability simulation for: {target}\n")

    results = {}

    # ---------------- NMAP ----------------
    print("[*] Running nmap (safe scan)...")
    nmap_cmd = ["nmap", "-sT", "-Pn", "-T4", target]
    nmap_out = run_command(nmap_cmd)
    results["nmap"] = parse_nmap(nmap_out)

    # ---------------- WHATWEB ----------------
    print("[*] Running whatweb...")
    whatweb_cmd = ["whatweb", target]
    whatweb_out = run_command(whatweb_cmd)
    results["whatweb"] = parse_whatweb(whatweb_out)

    # ---------------- NIKTO ----------------
    print("[*] Running nikto (non-intrusive)...")
    nikto_cmd = ["nikto", "-h", target]
    nikto_out = run_command(nikto_cmd)
    results["nikto"] = parse_nikto(nikto_out)

    STATE["simulation"] = results

    print("\n[+] Simulation completed")
    display_results(results)


# ================= PARSERS =================

def parse_nmap(output: str):
    findings = []

    for line in output.splitlines():
        if "/tcp" in line and "open" in line:
            findings.append(f"Open port detected: {line.strip()}")

        if "Service Info:" in line:
            findings.append(line.strip())

    return findings


def parse_whatweb(output: str):
    findings = []

    if "Apache" in output:
        findings.append("Apache web server detected")

    if "nginx" in output.lower():
        findings.append("Nginx web server detected")

    if "PHP" in output:
        findings.append("PHP detected")

    if "WordPress" in output:
        findings.append("WordPress detected")

    return findings


def parse_nikto(output: str):
    findings = []

    for line in output.splitlines():
        l = line.lower()

        if "x-frame-options" in l:
            findings.append("Missing X-Frame-Options header")

        if "x-content-type-options" in l:
            findings.append("Missing X-Content-Type-Options header")

        if "server leaks" in l or "server:" in l:
            findings.append("Server version disclosure")

        if "allowed http methods" in l:
            findings.append("Dangerous HTTP methods enabled")

    return findings


def display_results(results: dict):
    print("\n========== SIMULATION FINDINGS ==========\n")

    for tool, findings in results.items():
        print(f"[{tool.upper()}]")
        if not findings:
            print("  No significant findings\n")
            continue

        for f in findings:
            print(f"  - {f}")
        print()

