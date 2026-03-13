# Content Guide

This guide provides an overview of the content repository structure and organization.

## Table of Contents

1. [Repository Overview](#repository-overview)
2. [Content Structure](#content-structure)
3. [File Descriptions](#file-descriptions)
4. [Format Guide](#format-guide)
5. [Maintenance Guidelines](#maintenance-guidelines)

## Repository Overview

This repository serves as a centralized hub for content covering:
- Authentication and security features
- User management and role definitions
- Frequently asked questions
- Process content for key operations
- Automation and content quality tooling

## Content Structure

The repository is organized with paired file formats for accessibility:
- **XML Files (t_/r_/c_ prefixed)**: Structured, version-controlled content
- **ODT Files**: Formatted documents for easy reading and printing
- **Markdown Files**: Human-readable guides and references
- **Python Files**: Automation and content quality scripts

### File Naming Conventions

- **t_** prefix: Topic files (procedural and how-to guides)
- **r_** prefix: Reference files (factual information and FAQs)
- **c_** prefix: Configuration or security-related files

**Two-Step Authentication**
- Files:
  - XML: [c_two_step_authentication.xml](c_two_step_authentication.xml)
  - ODT: [two_step_authentication.odt](two_step_authentication.odt)
  - PDF: [two_step_authentication.pdf](two_step_authentication.pdf)
- Covers: Implementation and usage of two-step authentication via SSO and DSO
- Audience: System administrators, IT security teams

### User Management

**User Roles**
- Files:
  - XML: [r_user_roles.xml](r_user_roles.xml)
  - ODT: [user_roles.odt](user_roles.odt)
  - PDF: [user_roles.pdf](user_roles.pdf)
- Covers: Role definitions, permissions, and responsibilities mapped to real-world job functions
- Key Roles: Admin, User
- Audience: Institutional administrators, IT security teams

### Product Information

**Product FAQs**
- Files:
  - XML: [r_product_faqs.xml](r_product_faqs.xml)
  - ODT: [product_faqs.odt](product_faqs.odt)
  - PDF: [product_faqs.pdf](product_faqs.pdf)
- Topics:
  - What reconciliation is and why it is necessary
  - Data security and privacy (PII handling)
  - Data retention policies
  - Export and reporting capabilities
  - Monthly reconciliation requirements
- Audience: End users, system operators, training reference

### Operations

**Create New Estimates**
- Files:
  - XML: [t_create_new_estimates.xml](t_create_new_estimates.xml)
  - ODT: [create_new_estimates.odt](create_new_estimates.odt)
  - PDF: [create_new_estimates.pdf](create_new_estimates.pdf)
- Covers: Step-by-step guide for creating and managing cost estimates
- Audience: Financial aid staff, student services representatives, institutional and direct users

### Process & Automation

**Content Quality Review Script**
- Files:
  - Python: [content_review.py](content_review.py)
  - Reference: [CONTENT_REVIEW.md](CONTENT_REVIEW.md)
- Covers: Automated validation of DITA files against structural standards and the Microsoft Writing Style Guide
- Checks: Empty required elements, deprecated DITA elements, broken cross-references, hard-coded links, passive voice, filler words, Latin abbreviations, and 20+ additional style rules
- Output: HTML report and JSON report saved to `content_review_reports/`
- Audience: Content team members running self-service quality checks

## Additional Resources

**Megan Herzog Resume** ([Megan Herzog Resume.pdf](Megan%20Herzog%20Resume.pdf))
- Covers: Professional qualifications, experience, and credentials
- Audience: Hiring managers, stakeholders, team members

## Format Guide

### XML Format

XML files follow a structured format with:
- Metadata (IDs, titles, descriptions)
- Body content with tables and sections
- Consistent schema for easy parsing

**Benefits:**
- Version control friendly
- Machine-readable
- Structured and consistent

**Example Structure:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<topic id="topic-id">
  <title>Topic Title</title>
  <shortdesc>Brief description</shortdesc>
  <body>
    <!-- Content -->
  </body>
</topic>
```

### ODT Format

ODT (OpenDocument Text) files provide:
- Formatted, readable documents
- Print-friendly layouts
- Compatibility with multiple office suites

**Benefits:**
- Easy to read and share
- Professional formatting
- Wide software support

### Markdown Format

Markdown files provide:
- Quick reference guides
- README and navigation
- Source control friendly

**Benefits:**
- Easy to read and share
- README and navigation
- Source control friendly

### PDF Format

PDF files provide:
- Professional, formatted documents
- Print-ready files
- Portable read-only format

**Benefits:**
- Universal compatibility
- Maintains formatting across systems
- Suitable for sharing and archiving

### Python Format

Python (.py) files provide:
- Automated content quality checks
- Repeatable, self-service review workflows
- Portable scripts runnable on any folder of DITA/XML files

**Benefits:**
- Reduces reliance on manual checklists
- Consistent standards enforcement across the team
- HTML and JSON output for easy review and tracking

## Maintenance Guidelines

### Updating Content

1. **Dual Format Updates**: When updating content, maintain both XML and ODT versions
2. **Version Control**: Commit changes to both formats together
3. **Consistency**: Ensure titles, IDs, and descriptions match across formats

### Adding New Content

1. Create XML file with appropriate prefix (t_, r_, c_)
2. Create corresponding ODT file
3. Add reference to README.md
4. Commit both files together

### Quality Checklist

- [ ] Run `content_review.py` against the folder and resolve any errors or warnings
- [ ] Content is clear and concise
- [ ] All sections are properly titled and formatted
- [ ] Both XML and ODT versions are updated
- [ ] References are accurate and complete
- [ ] Commit messages are descriptive

## Best Practices

- **Keep it current**: Review and update content regularly
- **Be specific**: Include examples and use cases where applicable
- **Consistency matters**: Use uniform formatting and language
- **Link related content**: Reference related topics when appropriate
- **Version tracking**: Git commits should reference what changed and why
- **Run automated checks**: Use `content_review.py` before committing to catch structural and style issues early

---

**Last Updated:** March 2026
