# n8n Workflow

This folder contains the automation workflows developed using n8n to build an end-to-end data processing pipeline for the Coffee Shop Sales Analytics project.

The workflows automate data validation, processing, SQL logging, file management, and notification tasks before the data is consumed by Power BI.

---

# Workflow 1: AI Data Analysis Pipeline

This workflow automates the ingestion and validation of incoming sales datasets.

## Workflow Steps

1. Google Drive Trigger
2. Validation Engine (JavaScript)
3. File Validation
4. SQL Server Audit Logging
5. Download File
6. HTTP Request (Python Cleaning Service)
7. JavaScript Processing
8. Business Rule Validation
9. Move Valid File
10. Email Notification
11. Error Logging
12. Pipeline Failure Notification

---

# Workflow 2: Human Approval Workflow

This workflow manages manual approval before publishing validated datasets into production.

## Workflow Steps

1. Form Submission
2. Retrieve Pending File
3. Approval Decision
4. Move to Production
5. Production Verification
6. SQL Audit Update
7. Download Reports
8. Upload Approved File
9. Email Notification
10. Error Handling
11. Audit Logging

---

# Technologies

- n8n
- JavaScript
- Python API
- SQL Server
- Google Drive API
- Gmail
- HTTP Requests

---

# Features

- Automated ETL Pipeline
- Data Validation
- Business Rules Validation
- SQL Audit Logging
- Human Approval Process
- File Version Management
- Automated Notifications
- Error Handling
- Production Deployment

---

# Purpose

The workflows ensure that only validated and approved datasets are processed and loaded into the Business Intelligence solution, providing reliable and trusted data for reporting.
