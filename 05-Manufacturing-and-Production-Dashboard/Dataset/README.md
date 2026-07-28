# Dataset Description

## Overview

This dataset contains manufacturing and maintenance records designed for analyzing equipment reliability, production downtime, maintenance performance, and inventory management.

The data represents an integrated maintenance management system containing operational information related to equipment, failures, downtime events, spare parts, and maintenance costs.

---

## Dataset Purpose

The dataset was used to build a Manufacturing & Production Analytics solution focused on:

- Equipment reliability analysis
- Downtime monitoring
- Failure pattern identification
- Maintenance cost analysis
- Spare parts inventory optimization

---

## Data Contents

The dataset includes multiple interconnected tables covering:

### Equipment Data

Contains information about industrial assets:

- Equipment ID
- Equipment Name
- Equipment Type
- Location
- Manufacturer
- Criticality level

---

### Downtime & Failure Records

Contains failure events and operational losses:

- Failure ID
- Failure Mode
- Failure Cause
- Failure Severity
- Downtime Hours
- Production Loss

---

### Maintenance Records

Includes maintenance activities and associated costs:

- Maintenance activities
- Labor Cost
- Parts Cost
- Other Maintenance Costs
- Total Maintenance Cost

---

### Spare Parts Inventory

Contains inventory and consumption information:

- Part Name
- Part Category
- Stock Quantity
- Parts Consumption
- Inventory Value
- Reorder Level

---

## Data Model

The dataset consists of multiple operational tables connected through common identifiers such as:

- Equipment_ID
- Part_ID
- Failure_ID

These relationships were used to create the analytical data model in Power BI.

---

## Data Preparation

The dataset was prepared through:

- Data cleaning
- Data transformation
- Data validation
- KPI calculation
- Relationship modeling

---

## Analytical Use Cases

The dataset supports analysis of:

- Downtime trends over time
- Most common failure causes
- High-risk equipment identification
- Maintenance cost drivers
- Spare parts availability
- Operational efficiency

---

## Data Source

The dataset is used for analytical and demonstration purposes and represents a simulated manufacturing environment.

---

## Technologies Used

- Power BI
- DAX
- Power Query
- Data Modeling
- SQL
