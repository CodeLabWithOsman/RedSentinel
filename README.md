<p align="center">
  <img src="assets/redsentinel-logo.png" alt="RedSentinel Logo" width="220">
</p>

<h1 align="center">RedSentinel</h1>

<p align="center">
  <strong>AI-Assisted Security Assessment & Reporting Tool</strong>
</p>

<p align="center">
  Educational • Defensive • Auditor-Ready
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg">
  <img src="https://img.shields.io/badge/License-MIT-green.svg">
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20Kali%20%7C%20Termux-lightgrey.svg">
  <img src="https://img.shields.io/badge/Status-Alpha-orange.svg">
  <img src="https://img.shields.io/github/stars/hackura/RedSentinel?style=social">
</p>

---

##  What is RedSentinel?

**RedSentinel** is an **AI-assisted security assessment tool** designed for
**educational, defensive, and research-focused security testing**.

It performs **non-intrusive reconnaissance and analysis**, normalizes raw tool
output, and generates **professional, plain-English security reports** suitable
for:

* SOC analysts
* Security engineers
* Consultants
* Auditors
* Executives

>  **RedSentinel must only be used on systems you own or have explicit authorization to test.**

---

##  Key Features

* Live execution of common security tools:

  * `ping`, `nmap`, `whatweb`, `nikto`, `httpx`, `sslscan`
* Accurate parsing (fixes the classic *“no findings”* issue)
* Confidence-based filtering to reduce noise
* CVSS scoring and CVSS v3.1 vectors
* Executive-level risk score
* OWASP Top 10, ISO 27001, and PCI-DSS mapping
* AI-generated remediation roadmap (plain English)
* HTML, PDF (WeasyPrint), and JSON reporting
* SOC-friendly JSON export
* Termux auto-detection
* `--no-report` CLI flag for terminal-only scans

---

##  Requirements

* **Python 3.10+**
* Linux-based OS (Kali, Debian, Ubuntu, or Termux)
* External tools installed:

  ```bash
  nmap whatweb nikto httpx sslscan
  ```

### System Dependencies (PDF Reports)

**Debian / Kali / Ubuntu**

```bash
sudo apt install -y \
  libcairo2 \
  libpango-1.0-0 \
  libpangocairo-1.0-0 \
  libgdk-pixbuf-2.0-0 \
  libffi-dev \
  shared-mime-info
```

**Termux**

```bash
pkg install cairo pango libffi
```

---

##  Installation

```bash
git clone https://github.com/hackura/RedSentinel.git
cd RedSentinel

python -m venv venv
source venv/bin/activate

pip install .
```

---

##  AI Configuration (Optional)

To enable AI-generated explanations and remediation guidance, create a `.env`
file in the project root:

```env
REDSENTINEL_AI_KEY=your_api_key_here
REDSENTINEL_AI_URL=https://api.openai.com/v1/chat/completions
```

>  Never commit `.env` to GitHub.

---

##  Usage

Run the interactive CLI:

```bash
redsentinel
```

Run a scan without generating reports:

```bash
redsentinel --no-report
```

All reports are saved in the `reports/` directory.

---

##  Output Formats

* **Terminal Output** – Live findings with severity and confidence
* **HTML Report** – Executive-friendly assessment
* **PDF Report** – Audit-ready, printable format
* **JSON Export** – SOC and automation workflows

---

## Contributing

Contributions are **welcome** and **appreciated**.

You can contribute by:

* Improving parsers
* Adding new scanning tools
* Enhancing report templates
* Improving AI prompts
* Fixing bugs or improving documentation

### How to contribute

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a pull request

All contributions must remain **non-intrusive and defensive**.

---

##  Roadmap

Planned future enhancements:

* MITRE ATT&CK mapping
* Compliance scoring per framework
* Historical scan comparison
* Offline / local LLM support
* Plugin architecture for tools
* Docker support
* CI/CD pipelines
* Enhanced SOC integrations

Ideas and feedback are welcome via issues or discussions.

---

##  Support the Project

If RedSentinel helps you learn or work better:

* Star the repository
* Donate: [https://buymeacoffee.com/hackura](BuyMeACoffee)
* Share the project
* Contribute code or documentation

---

##  Connect

* GitHub: [https://github.com/hackura](GitHub)
* Twitter / X: [https://twitter.com/dorpe_karl](X)
* LinkedIn: [https://linkedin.com/in/karlseyramdorpe](LinkedIn)


---

##  Disclaimer

RedSentinel is provided for **educational and defensive security research only**.
The author assumes no responsibility for misuse or unauthorized testing.

---

##  Author

**Karl Seyram**
Hackura Project

