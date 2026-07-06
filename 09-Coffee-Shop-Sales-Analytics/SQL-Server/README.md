# SQL Server

This folder documents the SQL Server environment used in the automated ETL pipeline.

SQL Server acts as the central data repository between the automation workflows and the Power BI reporting layer.

## Database Structure

The solution includes three main tables:

### stg_coffee_sales

Temporary staging table used to receive validated datasets before production processing.

### fact_coffee_sales

Production fact table used by Power BI for reporting and business analysis.

### Pipeline_Audit_Log

Audit table used to monitor every pipeline execution.

The audit process records:

- Pipeline Status
- Validation Result
- Processing Timestamp
- Error Messages
- File Information

## SQL Server Responsibilities

- Data Staging
- Production Storage
- Audit Logging
- Business Rule Validation
- Power BI Data Source

## Integration

Google Drive

↓

n8n Automation

↓

SQL Server

↓

Power BI Dashboard

## Technologies

- Microsoft SQL Server
- T-SQL
- Audit Logging
- ETL Support
- Production Data Storage
