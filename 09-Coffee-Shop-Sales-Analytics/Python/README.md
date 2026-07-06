# Python Processing Engine

## Overview

This folder contains the Python backend powering the AI Data Analysis Platform.

The Python engine is responsible for data cleaning, validation, profiling, report generation, and loading processed data into SQL Server before visualization in Power BI.

---

## Folder Structure

### api/
Contains the FastAPI application used by the n8n workflow to trigger and manage the data processing pipeline.

### cleaning/
Includes modules for:
- Data Cleaning
- Data Validation
- Data Profiling
- Report Generation
- Utility Functions

### database/
Responsible for SQL Server connectivity and loading validated data into the database.

### validation/
Implements business validation rules before data is processed.

---

## Main Features

- Automated Data Cleaning
- Business Rule Validation
- Data Profiling
- Report Generation
- SQL Server Data Loading
- FastAPI Integration
- Modular Python Architecture

---

## Technologies

- Python
- FastAPI
- Pandas
- NumPy
- SQL Server
- REST API
