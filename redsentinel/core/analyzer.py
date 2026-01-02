from redsentinel.core.state import STATE


def analyze_file(filepath: str):
    """
    Analyze scan, log, or security tool output and extract findings.
    Supports generic logs, auth logs, Nikto output, and headers.
    """

    print(f"\n[+] Analyzing file: {filepath}\n")

    findings = set()

    try:
        with open(filepath, "r", errors="ignore") as f:
            for line in f:
                l = line.lower()

                # ---------------- AUTH LOG SIGNALS ----------------
                if "failed password" in l:
                    findings.add("Failed authentication attempts detected")

                if "invalid user" in l:
                    findings.add("Invalid user login attempts detected")

                if "authentication failure" in l:
                    findings.add("Authentication failure events detected")

                # ---------------- WEB / HEADER SIGNALS ----------------
                if "x-frame-options" in l and "not present" in l:
                    findings.add("Missing X-Frame-Options header")

                if "x-content-type-options" in l and "not set" in l:
                    findings.add("Missing X-Content-Type-Options header")

                if "content-security-policy" in l and "not present" in l:
                    findings.add("Missing Content-Security-Policy header")

                if "x-powered-by" in l:
                    findings.add("X-Powered-By header disclosed")

                if "server:" in l:
                    findings.add("Server banner disclosed")

                # ---------------- REDIRECTS ----------------
                if "uncommon header" in l and "refresh" in l:
                    findings.add("Client-side redirect via Refresh header")

    except Exception as e:
        print(f"[!] Error reading file: {e}")
        return

    if not findings:
        print("[+] No significant findings detected")
        return

    STATE["findings"] = sorted(findings)

    print("[+] Findings identified:")
    for f in STATE["findings"]:
        print(f" - {f}")

