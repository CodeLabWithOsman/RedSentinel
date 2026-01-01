import os
import sys

# Ensure core modules are accessible
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from core.exploit_engine import simulate
from core.analyzer import analyze_file
from core.planner import generate_plan


def clear():
    os.system("clear" if os.name == "posix" else "cls")


def banner():
    print(r"""
██████╗ ███████╗██████╗ ███████╗███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗
██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██║
██████╔╝█████╗  ██║  ██║███████╗█████╗  █████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██║
██╔══██╗██╔══╝  ██║  ██║╚════██║██╔══╝  ██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║
██║  ██║███████╗██████╔╝███████║███████╗███████╗██║ ╚████║   ██║   ██║██║ ╚████║███████╗███████╗
╚═╝  ╚═╝╚══════╝╚═════╝ ╚══════╝╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝

        AI-Assisted Red Team Framework
	++++Hackura++++
    """)


def pause():
    input("\nPress Enter to continue...")


def launch_menu():
    while True:
        clear()
        banner()

        print("""
[1] Initialize Project
[2] Analyze Scan / Logs
[3] Generate Red Team Plan
[4] Simulate Exploit (SAFE)
[5] Exit
""")

        choice = input("RedSentinel > ").strip()

        # ---------------- INIT ----------------
        if choice == "1":
            clear()
            print("[+] Initializing RedSentinel project...\n")
            print("Directories created:")
            print(" - reports/")
            print(" - evidence/")
            print(" - logs/")
            pause()

        # ---------------- ANALYZE ----------------
        elif choice == "2":
            clear()
            file_path = input("Enter scan/log file path: ").strip()

            if not os.path.exists(file_path):
                print("\n[!] File not found")
            else:
                analyze_file(file_path)

            pause()

        # ---------------- PLAN ----------------
        elif choice == "3":
            clear()
            target = input("Enter target name (e.g example.com): ").strip()
            generate_plan(target)
            pause()

        # ---------------- SIMULATE ----------------
        elif choice == "4":
            clear()
            print("Available exploit simulations:\n")
            print(" - missing_x_frame_options")
            print(" - missing_x_content_type_options")

            vuln = input("\nEnter simulation key: ").strip()
            simulate(vuln)
            pause()

        # ---------------- EXIT ----------------
        elif choice == "5":
            print("\nExiting RedSentinel...")
            sys.exit(0)

        else:
            print("\n[!] Invalid option")
            pause()
