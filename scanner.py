import subprocess
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()
REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)


def run_bandit(target_path):
    output_file = REPORTS_DIR / "bandit_report.json"

    command = [
        "bandit",
        "-r",
        target_path,
        "-f",
        "json",
        "-o",
        str(output_file)
    ]

    subprocess.run(command, capture_output=True, text=True)

    if not output_file.exists():
        return []

    with open(output_file, "r") as file:
        data = json.load(file)

    return data.get("results", [])


def run_pip_audit():
    output_file = REPORTS_DIR / "pip_audit_report.json"

    command = [
        "pip-audit",
        "-f",
        "json",
        "-o",
        str(output_file)
    ]

    subprocess.run(command, capture_output=True, text=True)

    if not output_file.exists():
        return []

    with open(output_file, "r") as file:
        data = json.load(file)

    return data.get("dependencies", [])


def display_bandit_results(results):
    table = Table(title="Bandit Code Security Findings")

    table.add_column("Severity")
    table.add_column("Issue")
    table.add_column("File")
    table.add_column("Line")

    if not results:
        console.print("[green]No Bandit issues found.[/green]")
        return

    for issue in results:
        table.add_row(
            issue.get("issue_severity", "N/A"),
            issue.get("issue_text", "N/A"),
            issue.get("filename", "N/A"),
            str(issue.get("line_number", "N/A"))
        )

    console.print(table)


def display_dependency_results(results):
    table = Table(title="Dependency Vulnerability Findings")

    table.add_column("Package")
    table.add_column("Version")
    table.add_column("Vulnerabilities")

    if not results:
        console.print("[green]No dependency vulnerabilities found.[/green]")
        return

    for dep in results:
        vulns = dep.get("vulns", [])
        if vulns:
            table.add_row(
                dep.get("name", "N/A"),
                dep.get("version", "N/A"),
                str(len(vulns))
            )

    console.print(table)

def save_scan_summary(bandit_results, dependency_results):
    summary_file = REPORTS_DIR / "scan_summary.json"

    summary = {
        "bandit_results": bandit_results,
        "dependency_results": dependency_results
    }

    with open(summary_file, "w") as file:
        json.dump(summary, file, indent=2)

    console.print(f"[green]Scan summary saved to {summary_file}[/green]")



def main():
    console.print("[bold cyan]AI Security Scanner for Python[/bold cyan]")

    target_path = input("Enter folder or file to scan: ").strip()

    if not target_path:
        target_path = "samples"

    bandit_results = run_bandit(target_path)
    dependency_results = run_pip_audit()

    display_bandit_results(bandit_results)
    display_dependency_results(dependency_results)
    save_scan_summary(bandit_results, dependency_results)

    console.print("[bold green]Security scan complete.[/bold green]")


if __name__ == "__main__":
    main()