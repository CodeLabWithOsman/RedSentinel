import sys
from redsentinel.menu import launch_menu


def check_venv():
    if sys.prefix == sys.base_prefix:
        print("""
[!] WARNING: You are NOT running inside a Python virtual environment.

PDF reporting requires third-party libraries (reportlab).
On Kali Linux, installing them system-wide is blocked.

RECOMMENDED FIX:
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

RedSentinel will continue, but PDF generation may fail.
""")


def main():
    check_venv()
    launch_menu()


if __name__ == "__main__":
    main()

