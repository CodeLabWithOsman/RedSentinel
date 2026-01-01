import os
import sys

from redsentinel.core.analyzer import analyze_file
from redsentinel.core.planner import generate_plan
from redsentinel.core.exploit_engine import simulate
from redsentinel.core.reporter import generate_report
from redsentinel.core.state import STATE, reset


def clear():
    os.system("clear" if os.name == "posix" else "cls")


def pause():
    input("\nPress Enter to continue...")


def banner():
    print(r"""
██████╗ ███████╗██████╗ ███████╗███████╗███████╗███╗   ██╗████████╗██╗
██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║
██████╔╝█████╗  ██║  ██║███████╗█████╗  █████╗  ██╔██╗ ██║   ██║   ██║
██╔══██╗██╔══╝  ██║  ██║╚════██║██╔══╝  ██╔══╝  ██║╚██╗██║   ██║   ██║
██║  ██║███████╗██████╔╝███████║███████╗███████╗██║ ╚████║   ██║   ██║
╚═╝  ╚═╝╚══════╝╚═════╝ ╚══════╝╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝

 RedSentinel – AI-Assisted Red Team Framework
""")


def launch_menu():
    while True:
        clear()
        banner()

        print("""
[1] New Assessment
[2] Analyze Scan / Logs
[3] Generate Red Team Plan
[4] Simulate Exploit
[5] Generate Report
[6] Exit
""")

        choice = input("RedSentinel > ").strip()

        if choice == "1":
            reset()
            print("[+] Assessment reset")
            pause()

        elif choice == "2":
            file_path = input("Enter scan/log file path: ").strip()
            if os.path.exists(file_path):
                analyze_file(file_path)
            else:
                print("[!] File not found")
            pause()

        elif choice == "3":
            target = input("Enter target: ").strip()
            generate_plan(target)
            pause()

        elif choice == "4":
            target = input("Enter target: ").strip()
            from redsentinel.core.simulator import simulate_scan
            simulate_scan(target)

        elif choice == "5":
            if not STATE["findings"]:
                print("[!] No findings available")
            else:
                report = generate_report()
                print(f"[+] Report generated: {report}")
            pause()

        elif choice == "6":
            sys.exit(0)

        else:
            print("[!] Invalid option")
            pause()

