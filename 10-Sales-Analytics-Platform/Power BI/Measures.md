# DAX Measures

This document contains the main DAX measures created for the Sales Analytics Platform.

---

# Executive KPI Measures

## Total Revenue

SUM(FactSales[SalesAmount])

## Total Cost

SUM(FactSales[TotalProductCost])

## Gross Profit

SUM(FactSales[GrossProfit])

## Profit Margin

DIVIDE([Gross Profit],[Total Revenue],0)

## Total Orders

DISTINCTCOUNT(FactSales[SalesOrderNumber])

## Units Sold

SUM(FactSales[OrderQuantity])

## Total Customers

DISTINCTCOUNT(DimCustomer[CustomerKey])

---

# Sales Performance Measures

## Average Order Value

DIVIDE([Total Revenue],[Total Orders],0)

## Average Profit Per Order

DIVIDE([Gross Profit],[Total Orders],0)

## Revenue Per Customer

DIVIDE([Total Revenue],[Total Customers],0)

---

# Financial Analysis

## Total Freight

SUM(FactSales[Freight])

## Cost Ratio

DIVIDE([Total Cost],[Total Revenue],0)

---

# Time Intelligence

## Running Revenue

CALCULATE(
[Total Revenue],
FILTER(
ALL(DimCalendar),
DimCalendar[Date] <= MAX(DimCalendar[Date])
)
)

## Revenue YoY %

Revenue comparison with previous year performance.

## Revenue MoM %

Monthly revenue growth comparison.

---

# Customer Analytics

## Customer Lifetime Value

Average revenue generated per customer.

## Repeat Customers

Customers with more than one order.

## One Time Customers

Customers with only one order.

---

# Product Analysis

## Product Revenue Rank

Ranks products based on total revenue.

## Product Profit Rank

Ranks products based on gross profit.

---

# ABC Analysis

Products classified based on cumulative revenue contribution:

- A Class: High-value products
- B Class: Medium-value products
- C Class: Low-value products

---

# Market Basket Analysis

Metrics:

- Support
- Confidence
- Lift

Used to identify product purchasing relationships.

---

# Forecasting & Sales Simulator

Used for:

- Future sales estimation
- Scenario analysis
- Revenue simulation
- Profit impact analysis

---

# Tools Used

- Power BI
- DAX
- SQL Server
- Python
- Star Schema Modeling

---

# Purpose

Create a complete analytical layer for business monitoring, performance evaluation, and data-driven decision making.
