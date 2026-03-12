# Content Quality Review Scripts

This folder contains scripts for DITA content quality validation, combining structural checks with Microsoft Writing Style Guide compliance.

---

## Generic Review Script (Portable — Recommended)

### content_review.py

A standalone, path-independent script that runs on any folder of DITA/XML files. No configuration required.

**Requirements**:
```powershell
pip install lxml
```

**Usage**:
```powershell
# Review any folder
python content_review.py <path_to_folder>

# Specify a custom output folder for reports
python content_review.py <path_to_folder> --output <path_to_reports>

# JSON report only (no HTML)
python content_review.py <path_to_folder> --json-only
```

**Examples**:
```powershell
# Review a local project
python content_review.py C:/projects/my_docs

# Review with custom report output
python content_review.py ./dita_files --output ./reports
```

**Output** (saved to `<folder>/content_review_reports/` by default):
- `content_review_YYYYMMDD_HHMMSS.html` — Visual report with highlighted issues
- `content_review_YYYYMMDD_HHMMSS.json` — Machine-readable results

**What it checks:**

| Category | Check | Severity |
|---|---|---|
| Structure | Empty required elements (`<title>`, `<shortdesc>`) | Error |
| Structure | Deprecated DITA elements | Error |
| Structure | Malformed or broken cross-references | Error |
| Structure | Hard-coded URLs (use keys/reltables instead) | Info |
| Structure | Malformed conref attributes | Warning |
| Style Guide | Avoid "please", "simply", "just", "obviously" | Warning |
| Style Guide | Avoid "utilize", "leverage", "robust", "seamless" | Warning |
| Style Guide | Replace "e.g.", "i.e.", "etc." with full phrases | Warning |
| Style Guide | Use "and" instead of "&" outside code/UI | Warning |
| Style Guide | Use "select" or "click" (not "click on") | Warning |
| Style Guide | Passive voice indicators | Info |
| Style Guide | Refer to reader as "you" (not "the user") | Info |
| Style Guide | Simplify "in order to" → "to" | Info |
| Style Guide | Replace "via" with "through" or "by using" | Info |

---

## Original Project-Specific Script (Legacy Reference)

> **Note**: The scripts below are tied to a specific workspace path (`c:\id_campuslogic`). Use `content_review.py` above for portable use.

## Initial Setup (First-Time Users)

### 1. Verify Python Installation

Check if Python 3.7+ is installed:
```powershell
python --version
```

If not installed, download from: https://www.python.org/downloads/

**Important**: During installation, check "Add Python to PATH"

### 2. Install Required Python Packages

```powershell
# Navigate to the workspace root
cd c:\id_campuslogic

# Install required packages
pip install python-docx pandas openpyxl
```

### 3. Verify Installation

Test that the script can be found:
```powershell
python code_quality_review\code_quality_review_v3.py --help
```

If you see "can't open file" error, ensure you're in the `c:\id_campuslogic` directory.

### 4. Test Run

Run a test validation on a small product folder:
```powershell
python code_quality_review\code_quality_review_v3.py student_forms
```

## Main Scripts

### code_quality_review_v3.py (Current Version)
**Purpose**: Validates DITA coding standards for documentation quality

**Features**:
- Validates keywords against common master file
- Checks for empty elements
- Validates cross-references (xrefs, conrefs, keyrefs)
- Checks semantic integrity
- Detects block nesting violations
- Identifies hard links vs relationship tables
- Flags deprecated table types
- Fixed false positive: ul/ol allowed in p tag with introductory text

**Usage**:
```powershell
cd c:\id_campuslogic
python code_quality_review\code_quality_review_v3.py [folder_path]
```

**Output**:
- HTML report: `[folder]/code_quality_reports/code_quality_review_v3_YYYYMMDD_HHMMSS.html`
- JSON report: `[folder]/code_quality_reports/code_quality_review_v3_YYYYMMDD_HHMMSS.json`
- Excel report: `[folder]/code_quality_reports/code_quality_review_v3_YYYYMMDD_HHMMSS.xlsx`

### Legacy Versions

#### code_quality_review_v2.py
Earlier version with fewer validations. Use V3 for best results.

#### code_quality_review_v1.py
Original version. Kept for reference only.

## Supporting Files

- **code_quality_html_template.py** - HTML report generation templates

## Documentation

- **CODE_QUALITY_REVIEW_EXPLANATION.txt** - Detailed explanation of quality checks
- **CODE_QUALITY_REVIEW_V2_CHANGES.md** - Changes from V1 to V2
- **CODE_QUALITY_REVIEW_V3_CHANGES.md** - Changes from V2 to V3
- **CODE_QUALITY_REVIEW_V3_DELIVERABLES.md** - V3 deliverables summary
- **CODE_QUALITY_REVIEW_V3_FINAL_SUMMARY.md** - V3 final implementation summary
- **CODE_QUALITY_REVIEW_V3_IMPLEMENTATION_SUMMARY.md** - V3 implementation details
- **CODE_QUALITY_REVIEW_V3_QUICK_REFERENCE.md** - Quick reference guide for V3
- **CODE_QUALITY_REVIEW_V3_TOOLS_AND_STANDARDS.md** - Tools and standards documentation

## Common Validation Checks

### Error-Level Issues
- Broken cross-references (xref, conref, conkeyref, keyref)
- Empty required elements
- Invalid element nesting
- Deprecated elements

### Warning-Level Issues
- Empty optional elements
- Hard-coded links (should use relationship tables)
- Deprecated table types
- Potential semantic issues

## Example Validation Run

```powershell
# Validate Student Forms product
cd c:\id_campuslogic
python code_quality_review\code_quality_review_v3.py student_forms

# Expected output:
# - Loaded 303 keys from common master
# - Found 319 key definitions
# - Found 376 conref targets
# - Validated 369 DITA files
# - Generated HTML/JSON/Excel reports
```

## Script Requirements

```powershell
pip install python-docx pandas openpyxl
```

## Output Exclusions

All output folders (`code_quality_reports/`) are excluded from version control via `.gitignore`.

---

## Troubleshooting

### "python is not recognized as an internal or external command"
**Solution**: Python is not in your PATH. Either:
- Reinstall Python and check "Add Python to PATH"
- Or use full path: `C:\Users\YourName\AppData\Local\Programs\Python\Python3XX\python.exe`

### "No module named 'docx'" or similar import errors
**Solution**: Install missing packages:
```powershell
pip install python-docx pandas openpyxl
```

### "can't open file 'code_quality_review_v3.py'"
**Solution**: You're not in the correct directory. Run:
```powershell
cd c:\id_campuslogic
python code_quality_review\code_quality_review_v3.py student_forms
```

### "Cannot find path" when validating a folder
**Solution**: Use full path to the folder:
```powershell
python code_quality_review\code_quality_review_v3.py c:\id_campuslogic\student_forms
```

### Script runs but no output files generated
**Solution**: Check that the product folder has a `code_quality_reports` directory. The script will create it if it doesn't exist.

### "Access Denied" when opening reports
**Solution**: Close any open reports in your browser and try again. Or open manually from File Explorer.

---

## Quick Reference Card

```powershell
# Standard validation workflow
cd c:\id_campuslogic
python code_quality_review\code_quality_review_v3.py student_forms

# Validate specific product by full path
python code_quality_review\code_quality_review_v3.py c:\id_campuslogic\raise_me

# Find today's reports
Get-ChildItem student_forms\code_quality_reports -Filter "*$(Get-Date -Format 'yyyyMMdd')*.html"
```
