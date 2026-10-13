
import re
from pathlib import Path


def analyze_log(log_text: str) -> dict:
    """Extract basic error, warning, and failure information."""
    lines = log_text.splitlines()

    errors = []
    warnings = []
    failures = []

    for line_number, line in enumerate(lines, start=1):
        if re.search(r"\b(error|fatal)\b", line, re.IGNORECASE):
            errors.append({"line": line_number, "text": line.strip()})

        if re.search(r"\bwarning\b", line, re.IGNORECASE):
            warnings.append({"line": line_number, "text": line.strip()})

        if re.search(
            r"\b(fail|failed|failure|assertion failed)\b",
            line,
            re.IGNORECASE,
        ):
            failures.append({"line": line_number, "text": line.strip()})

    return {
        "total_lines": len(lines),
        "errors": errors,
        "warnings": warnings,
        "failures": failures,
    }


def analyze_file(file_path: str) -> dict:
    """Read a log file and analyze its contents."""
    path = Path(file_path)
    return analyze_log(path.read_text(encoding="utf-8", errors="replace"))


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="RTL simulation log parser")
    parser.add_argument("log_file", help="Path to a simulation log file")
    args = parser.parse_args()

    result = analyze_file(args.log_file)
    print(json.dumps(result, indent=2))
