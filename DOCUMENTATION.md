# Documentation Guide

This guide provides an overview of the documentation repository structure and content organization.

## Table of Contents

1. [Repository Overview](#repository-overview)
2. [Documentation Structure](#documentation-structure)
3. [File Descriptions](#file-descriptions)
4. [Format Guide](#format-guide)
5. [Maintenance Guidelines](#maintenance-guidelines)

## Repository Overview

This repository serves as a centralized hub for technical documentation covering:
- Authentication and security features
- User management and role definitions
- Frequently asked questions
- Process documentation for key operations

## Documentation Structure

The repository is organized with paired file formats for accessibility:
- **XML Files (t_/r_/c_ prefixed)**: Structured, version-controlled documentation
- **ODT Files**: Formatted documents for easy reading and printing
- **Markdown Files**: Human-readable guides and references

### File Naming Conventions

- **t_** prefix: Topic files (procedural and how-to guides)
- **r_** prefix: Reference files (factual information and FAQs)
- **c_** prefix: Configuration or security-related files

**Two-Step Authentication**
- Files: 
  - XML: [c_two_step_authentication.xml](c_two_step_authentication.xml)
- Covers: Implementation, configuration, and usage of two-factor authentication
- Audience: System administrators, security personnel

### User Management

**User Roles**
- Files: 
  - XML: [r_user_roles.xml](r_user_roles.xml)
- Covers: Role hierarchy, permissions, and responsibilities
- Key Roles: Admin, User
- Audience: System administrators, account managers

### Product Information

**Product FAQs**
- Files: 
  - XML: [r_product_faqs.xml](r_product_faqs.xml)
- Topics:
  - What reconciliation is and why it's necessary
  - Data security and privacy (PII handling)
  - Data retention policies (90-day retention)
  - Export and reporting capabilities
  - Monthly reconciliation requirements for campus-based aid and Direct Loan
- Audience: End users, system operators

### Operations

**Create New Estimates**
- Files: 
  - XML: [t_create_new_estimates.xml](t_create_new_estimates.xml)
- Covers: Step-by-step guide for estimate creation and management
- Audience: Users, operators

## Additional Resources

### PDF Documents

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

## Maintenance Guidelines

### Updating Documentation

1. **Dual Format Updates**: When updating content, maintain both XML and ODT versions
2. **Version Control**: Commit changes to both formats together
3. **Consistency**: Ensure titles, IDs, and descriptions match across formats

### Adding New Documentation

1. Create XML file with appropriate prefix (t_, r_, c_)
2. Create corresponding ODT file
3. Add reference to README.md
4. Commit both files together

### Quality Checklist

- [ ] Content is clear and concise
- [ ] Examples are provided where helpful
- [ ] All sections are properly titled and formatted
- [ ] Both XML and ODT versions are updated
- [ ] References are accurate and complete
- [ ] Commit messages are descriptive

## Best Practices

- **Keep it current**: Review and update documentation regularly
- **Be specific**: Include examples and use cases where applicable
- **Consistency matters**: Use uniform formatting and language
- **Link related content**: Reference related topics when appropriate
- **Version tracking**: Git commits should reference what changed and why

---

**Last Updated:** March 2026
