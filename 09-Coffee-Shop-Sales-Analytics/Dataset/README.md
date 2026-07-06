# Dataset Overview

This folder contains the raw coffee shop sales dataset used in the End-to-End Business Intelligence project.

The dataset serves as the starting point of the data pipeline before validation, cleaning, transformation, SQL loading, and Power BI reporting.

## Dataset Information

- Source: Coffee Shop Sales Dataset
- Period: January 2023 – June 2023
- Records: 149,116 Transactions
- Stores: 3
- Product Categories: 9
- Products: 80

## Dataset Fields

- Transaction ID
- Transaction Date
- Transaction Time
- Store Location
- Product Category
- Product Type
- Product Detail
- Unit Price
- Transaction Quantity

## Data Pipeline

The dataset follows the complete processing workflow:

Raw Dataset
→ Validation
→ Data Cleaning
→ SQL Server
→ Business Rules Validation
→ Audit Logging
→ Power BI Dashboard

## Purpose

The dataset is used to analyze sales performance, product contribution, store performance, customer purchasing patterns, and time-based business trends.

## Note

The original dataset is never used directly for reporting.

It passes through an automated ETL pipeline built with n8n, where the data is validated, cleaned, checked for business rules, logged into SQL Server audit tables, and prepared before being consumed by Power BI.
