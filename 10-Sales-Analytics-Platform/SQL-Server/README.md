# SQL Server Database

SQL Server was used as the data warehouse layer for the Sales Analytics Platform.

The database was designed to store cleaned sales data, create analytical views, and provide optimized datasets for Power BI and Streamlit dashboards.

---

# Database Architecture

The project follows a dimensional modeling approach using a Star Schema design.

## Fact Table

### FactSales

Contains transactional sales data including:

- Sales Amount
- Product Cost
- Quantity
- Profit
- Freight
- Order Information


## Dimension Tables

### DimProduct

Contains product information:

- Product Name
- Category
- Subcategory
- Product Attributes


### DimCustomer

Contains customer information:

- Customer Details
- Demographics
- Customer Segmentation


### DimCalendar

Contains time intelligence attributes:

- Date
- Year
- Quarter
- Month


### DimTerritory

Contains geographical information:

- Country
- Region
- Territory

---

# SQL Views

Analytical views were created to support dashboard reporting:

## Executive Analysis

- vw_ExecutiveKPI

## Sales Analysis

- vw_SalesAnalysis
- vw_MonthlyPerformance
- vw_TerritoryPerformance

## Product Analysis

- vw_ProductPerformance
- vw_CategoryPerformance

## Customer Analysis

- vw_CustomerPerformance
- vw_RFMCustomers

## Financial Analysis

- vw_FinancialAnalysis

## Market Basket Analysis

- vw_MarketBasketAnalysis

## Simulation

- vw_SalesSimulator

---

# Technologies Used

- SQL Server
- T-SQL
- Star Schema Modeling
- Views
- Data Warehouse Concepts

---

# Purpose

Create a structured analytical database layer that transforms cleaned data into business-ready datasets for reporting, visualization, and decision support.
