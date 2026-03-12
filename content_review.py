#!/usr/bin/env python3
"""
Content Quality Review Script
Validates DITA XML files against structural standards and
Microsoft Writing Style Guide principles.

Usage:
    python content_review.py <folder_path> [--output <output_folder>]

Examples:
    python content_review.py ./my_dita_project
    python content_review.py C:/projects/docs --output C:/reports
"""

import os
import sys
import re
import json
import argparse
from datetime import datetime
from pathlib import Path
import xml.etree.ElementTree as ET

# ---------------------------------------------------------------------------
# Microsoft Writing Style Guide checks
# Each entry: pattern (str or regex) -> (severity, message, suggestion)
# ---------------------------------------------------------------------------

STYLE_CHECKS = [
    # ---- Filler / condescending words ----
    (r"\bplease\b",         "warning", "Avoid 'please' in instructions.",             "Remove 'please' — it is redundant in procedural content."),
    (r"\bsimply\b",         "warning", "Avoid 'simply'.",                             "Remove 'simply' — it implies the task is trivial and may frustrate users."),
    (r"\bjust\b",           "warning", "Avoid 'just' to minimize steps.",             "Remove 'just' when used to minimize complexity."),
    (r"\beasily\b",         "warning", "Avoid 'easily'.",                             "What is easy for one user may not be for another."),
    (r"\bobviously\b",      "warning", "Avoid 'obviously'.",                          "It may not be obvious to all users."),
    (r"\bbasically\b",      "warning", "Avoid 'basically'.",                          "Vague filler — remove or replace with specific language."),
    (r"\bof course\b",      "warning", "Avoid 'of course'.",                          "Implies the reader should already know — can alienate users."),
    (r"\bnote that\b",      "info",    "Reconsider 'Note that'.",                     "Consider using a <note> element instead, or rewrite to lead with the key information."),

    # ---- Word choice ----
    (r"\butilize\b",        "warning", "Use 'use' instead of 'utilize'.",             "Replace 'utilize' with 'use' per Microsoft Style Guide."),
    (r"\blever age\b",      "warning", "Avoid 'leverage' as a verb.",                 "Replace with 'use' or a more specific verb."),
    (r"\brobust\b",         "warning", "Avoid marketing language: 'robust'.",         "Describe the specific capability instead."),
    (r"\bseamless(ly)?\b",  "warning", "Avoid marketing language: 'seamless'.",       "Use specific, measurable language."),
    (r"\bintuitive\b",      "warning", "Avoid 'intuitive'.",                          "Subjective term — describe the specific behavior instead."),
    (r"\buser-?friendly\b", "warning", "Avoid 'user-friendly'.",                      "Subjective — describe what makes it easy to use."),
    (r"\bdesired\b",        "warning", "Avoid 'desired'.",                            "Replace with 'wanted' or 'required' as appropriate."),
    (r"\bperform\b",        "info",    "Consider replacing 'perform'.",               "Use a more specific verb: 'run', 'complete', 'do'."),
    (r"\ballow(s)? you to\b","info",   "Consider replacing 'allows you to'.",         "Replace with 'lets you' or rewrite: 'You can...'"),
    (r"\bin order to\b",    "info",    "Simplify 'in order to'.",                     "Replace with 'to'."),
    (r"\bvia\b",            "info",    "Consider replacing 'via'.",                   "Replace with 'through', 'by using', or 'with'."),

    # ---- Latin abbreviations ----
    (r"\be\.g\.",           "warning", "Avoid 'e.g.'",                                "Replace with 'for example'."),
    (r"\bi\.e\.",           "warning", "Avoid 'i.e.'",                                "Replace with 'that is'."),
    (r"\betc\.",            "warning", "Avoid 'etc.'",                                "Be specific, or use 'and more' / 'and so on'."),

    # ---- Ampersand ----
    (r"(?<!\w)&(?!\w+;)",   "warning", "Use 'and' instead of '&'.",                  "Use '&' only in UI labels, code, or proper names."),

    # ---- Click vs Select ----
    (r"\bclick on\b",       "warning", "Use 'select' or 'click', not 'click on'.",    "Remove 'on': 'Click the button' or 'Select the option'."),

    # ---- Passive voice indicators ----
    (r"\bwill be\b",        "info",    "Possible future passive voice.",              "Consider rewriting in active, present tense."),
    (r"\bis performed\b",   "info",    "Passive voice detected.",                     "Rewrite in active voice: identify who performs the action."),
    (r"\bare used\b",       "info",    "Possible passive voice.",                     "Rewrite in active voice where possible."),
    (r"\bcan be used\b",    "info",    "Possible passive voice.",                     "Rewrite as 'You can use...' for clearer active voice."),
    (r"\bshould be\b",      "info",    "Possible passive construction.",              "Specify who should do what: 'You should...' or rephrase actively."),

    # ---- Second person ----
    (r"\bthe user(s)?\b",   "info",    "Consider using 'you' instead of 'the user'.", "Address the reader directly with 'you' per Microsoft Style Guide."),
    (r"\bone should\b",     "info",    "Avoid impersonal 'one should'.",              "Use 'you should' or rewrite in active voice."),
]

# ---------------------------------------------------------------------------
# DITA structural checks
# ---------------------------------------------------------------------------

EMPTY_REQUIRED = ["title", "shortdesc"]
DEPRECATED_ELEMENTS = ["object", "shape", "coords", "boolean", "many"]

SEMANTIC_HINTS = {
    # Pattern in text content -> suggested DITA element
    r"C:\\|/[a-z]+/":        ("filepath",   "File paths should use <filepath>"),
    r"\.(xml|dita|md|txt)\b":("filepath",   "File references should use <filepath>"),
    r"\b[A-Z][a-z]+\s[A-Z]": ("uicontrol", "UI element names may need <uicontrol>"),
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def find_dita_files(root_folder: Path) -> list[Path]:
    """Return all .dita and .xml files under root_folder."""
    extensions = {".dita", ".xml", ".ditamap"}
    files = []
    for ext in extensions:
        files.extend(root_folder.rglob(f"*{ext}"))
    return sorted(files)


def extract_text_nodes(element: ET.Element) -> list[tuple[str, str]]:
    """
    Yield (tag, text) pairs for all text content in an element tree,
    including tail text. Returns a flat list.
    """
    results = []
    for elem in element.iter():
        if elem.text and elem.text.strip():
            results.append((elem.tag, elem.text.strip()))
        if elem.tail and elem.tail.strip():
            results.append((elem.tag + "[tail]", elem.tail.strip()))
    return results


def run_style_checks(text: str) -> list[dict]:
    """Run all Microsoft Style Guide checks against a text string."""
    issues = []
    for pattern, severity, message, suggestion in STYLE_CHECKS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            issues.append({
                "severity": severity,
                "matched": match.group(0),
                "message": message,
                "suggestion": suggestion,
                "position": match.start(),
            })
    return issues


def check_structural(root: ET.Element, filepath: Path) -> list[dict]:
    """Check DITA structural rules."""
    issues = []

    # Empty required elements
    for tag in EMPTY_REQUIRED:
        for elem in root.iter(tag):
            content = "".join(elem.itertext()).strip()
            if not content:
                issues.append({
                    "severity": "error",
                    "check": "empty_element",
                    "message": f"Empty required element: <{tag}>",
                    "suggestion": f"Provide content for <{tag}>.",
                })

    # Deprecated elements
    for tag in DEPRECATED_ELEMENTS:
        for _ in root.iter(tag):
            issues.append({
                "severity": "error",
                "check": "deprecated_element",
                "message": f"Deprecated element used: <{tag}>",
                "suggestion": f"Remove or replace <{tag}> with a current DITA element.",
            })

    # Broken internal cross-references (xref with href starting #)
    for xref in root.iter("xref"):
        href = xref.get("href", "")
        if href.startswith("#") and not href[1:]:
            issues.append({
                "severity": "error",
                "check": "broken_xref",
                "message": "Cross-reference has empty anchor: href='#'",
                "suggestion": "Provide a valid topic ID or remove the xref.",
            })

    # conref without valid format
    for elem in root.iter():
        conref = elem.get("conref", "")
        if conref and "#" not in conref:
            issues.append({
                "severity": "warning",
                "check": "malformed_conref",
                "message": f"conref may be missing topic ID: '{conref}'",
                "suggestion": "conref format should be: file.dita#topic-id/element-id",
            })

    # Hard-coded URLs in href (should use keys/relationship tables)
    for elem in root.iter():
        href = elem.get("href", "")
        if re.match(r"https?://", href) and elem.tag == "xref":
            issues.append({
                "severity": "info",
                "check": "hard_link",
                "message": f"Hard-coded URL in xref: '{href}'",
                "suggestion": "Consider using a keyref and relationship table for external links.",
            })

    return issues


# ---------------------------------------------------------------------------
# Per-file review
# ---------------------------------------------------------------------------

def review_file(filepath: Path) -> dict:
    """Run all checks on a single DITA file. Returns a result dict."""
    result = {
        "file": str(filepath),
        "errors": [],
        "warnings": [],
        "info": [],
        "parse_error": None,
    }

    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
    except ET.ParseError as e:
        result["parse_error"] = str(e)
        result["errors"].append({
            "severity": "error",
            "check": "xml_parse",
            "message": f"XML parse error: {e}",
            "suggestion": "Fix XML syntax errors before re-running the review.",
        })
        return result

    # --- Structural checks ---
    for issue in check_structural(root, filepath):
        bucket = result.get(issue["severity"] + "s", result["info"])
        if issue["severity"] == "error":
            result["errors"].append(issue)
        elif issue["severity"] == "warning":
            result["warnings"].append(issue)
        else:
            result["info"].append(issue)

    # --- Style checks (on all text content) ---
    text_nodes = extract_text_nodes(root)
    for tag, text in text_nodes:
        for style_issue in run_style_checks(text):
            entry = {
                "severity": style_issue["severity"],
                "check": "style_guide",
                "element": tag,
                "matched": style_issue["matched"],
                "message": style_issue["message"],
                "suggestion": style_issue["suggestion"],
                "context": text[:120] + ("..." if len(text) > 120 else ""),
            }
            if style_issue["severity"] == "error":
                result["errors"].append(entry)
            elif style_issue["severity"] == "warning":
                result["warnings"].append(entry)
            else:
                result["info"].append(entry)

    return result


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def severity_color(severity: str) -> str:
    return {"error": "#c0392b", "warning": "#e67e22", "info": "#2980b9"}.get(severity, "#555")


def severity_bg(severity: str) -> str:
    return {"error": "#fdf2f2", "warning": "#fef9f0", "info": "#eaf4fb"}.get(severity, "#f9f9f9")


def build_html_report(results: list[dict], folder: Path, output_path: Path) -> None:
    total_errors   = sum(len(r["errors"])   for r in results)
    total_warnings = sum(len(r["warnings"]) for r in results)
    total_info     = sum(len(r["info"])     for r in results)
    files_with_issues = sum(
        1 for r in results if r["errors"] or r["warnings"] or r["info"]
    )

    rows = []
    for r in results:
        rel = Path(r["file"]).relative_to(folder) if folder in Path(r["file"]).parents else Path(r["file"]).name
        all_issues = (
            [(i, "error")   for i in r["errors"]] +
            [(i, "warning") for i in r["warnings"]] +
            [(i, "info")    for i in r["info"]]
        )
        if not all_issues and not r["parse_error"]:
            continue

        rows.append(f'<tr><td colspan="4" style="background:#f0f0f0;font-weight:bold;padding:6px 10px">'
                    f'&#128196; {rel}</td></tr>')
        for issue, sev in all_issues:
            context = issue.get("context", "")
            matched = issue.get("matched", "")
            # Highlight the matched word in context
            if matched and context:
                context_html = context.replace(
                    matched,
                    f'<mark style="background:#ffe08a">{matched}</mark>',
                    1
                )
            else:
                context_html = context

            rows.append(
                f'<tr style="background:{severity_bg(sev)}">'
                f'<td style="padding:5px 10px;color:{severity_color(sev)};font-weight:bold;white-space:nowrap">'
                f'{sev.upper()}</td>'
                f'<td style="padding:5px 10px">{issue.get("check","")}</td>'
                f'<td style="padding:5px 10px">{issue.get("message","")}'
                + (f'<br><small style="color:#555">{context_html}</small>' if context_html else "")
                + '</td>'
                f'<td style="padding:5px 10px;color:#27ae60">{issue.get("suggestion","")}</td>'
                '</tr>'
            )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Content Quality Review — {datetime.now().strftime('%Y-%m-%d %H:%M')}</title>
<style>
  body {{ font-family: Segoe UI, Arial, sans-serif; margin: 0; padding: 20px; color: #222; }}
  h1   {{ color: #1a1a2e; }}
  .summary {{ display: flex; gap: 20px; margin: 20px 0; flex-wrap: wrap; }}
  .card {{ border-radius: 6px; padding: 16px 24px; min-width: 140px; text-align: center; }}
  .card h2 {{ margin: 0; font-size: 2em; }}
  .card p  {{ margin: 4px 0 0; font-size: 0.9em; color: #555; }}
  table {{ border-collapse: collapse; width: 100%; margin-top: 20px; font-size: 0.9em; }}
  th    {{ background: #1a1a2e; color: white; padding: 8px 10px; text-align: left; }}
  td    {{ border-bottom: 1px solid #ddd; vertical-align: top; }}
  mark  {{ border-radius: 3px; padding: 1px 2px; }}
  footer {{ margin-top: 30px; font-size: 0.8em; color: #888; }}
</style>
</head>
<body>
<h1>Content Quality Review Report</h1>
<p>Folder: <code>{folder}</code> &nbsp;|&nbsp; Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

<div class="summary">
  <div class="card" style="background:#fdf2f2">
    <h2 style="color:#c0392b">{total_errors}</h2><p>Errors</p>
  </div>
  <div class="card" style="background:#fef9f0">
    <h2 style="color:#e67e22">{total_warnings}</h2><p>Warnings</p>
  </div>
  <div class="card" style="background:#eaf4fb">
    <h2 style="color:#2980b9">{total_info}</h2><p>Suggestions</p>
  </div>
  <div class="card" style="background:#f4f4f4">
    <h2>{len(results)}</h2><p>Files scanned</p>
  </div>
  <div class="card" style="background:#f4f4f4">
    <h2>{files_with_issues}</h2><p>Files with issues</p>
  </div>
</div>

<table>
<thead>
  <tr>
    <th style="width:80px">Severity</th>
    <th style="width:140px">Check</th>
    <th>Issue</th>
    <th style="width:30%">Suggestion</th>
  </tr>
</thead>
<tbody>
{"".join(rows) if rows else '<tr><td colspan="4" style="padding:20px;text-align:center;color:#27ae60">&#10003; No issues found.</td></tr>'}
</tbody>
</table>

<footer>
  Content Quality Review &nbsp;|&nbsp; Microsoft Writing Style Guide checks &amp; DITA structural validation
</footer>
</body>
</html>"""

    output_path.write_text(html, encoding="utf-8")


def build_json_report(results: list[dict], output_path: Path) -> None:
    output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")


def print_summary(results: list[dict]) -> None:
    total_e = sum(len(r["errors"])   for r in results)
    total_w = sum(len(r["warnings"]) for r in results)
    total_i = sum(len(r["info"])     for r in results)
    print(f"\n{'='*60}")
    print(f"  Files scanned : {len(results)}")
    print(f"  Errors        : {total_e}")
    print(f"  Warnings      : {total_w}")
    print(f"  Suggestions   : {total_i}")
    print(f"{'='*60}\n")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Content Quality Review — DITA + Microsoft Writing Style Guide"
    )
    parser.add_argument(
        "folder",
        help="Path to folder containing DITA/XML files to review",
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Output folder for reports (default: <folder>/content_review_reports)",
    )
    parser.add_argument(
        "--json-only",
        action="store_true",
        help="Only generate JSON report (skip HTML)",
    )
    args = parser.parse_args()

    folder = Path(args.folder).resolve()
    if not folder.exists() or not folder.is_dir():
        print(f"ERROR: Folder not found: {folder}")
        sys.exit(1)

    output_folder = Path(args.output).resolve() if args.output else folder / "content_review_reports"
    output_folder.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Find and review files
    files = find_dita_files(folder)
    if not files:
        print(f"No DITA/XML files found in: {folder}")
        sys.exit(0)

    print(f"\nContent Quality Review")
    print(f"Folder  : {folder}")
    print(f"Files   : {len(files)} DITA/XML files found\n")

    results = []
    for i, filepath in enumerate(files, 1):
        print(f"  [{i:>3}/{len(files)}] {filepath.name}", end=" ... ")
        result = review_file(filepath)
        results.append(result)
        e = len(result["errors"])
        w = len(result["warnings"])
        n = len(result["info"])
        print(f"{e} error(s), {w} warning(s), {n} suggestion(s)")

    print_summary(results)

    # Write reports
    json_path = output_folder / f"content_review_{timestamp}.json"
    build_json_report(results, json_path)
    print(f"JSON report : {json_path}")

    if not args.json_only:
        html_path = output_folder / f"content_review_{timestamp}.html"
        build_html_report(results, folder, html_path)
        print(f"HTML report : {html_path}")

    print()


if __name__ == "__main__":
    main()
