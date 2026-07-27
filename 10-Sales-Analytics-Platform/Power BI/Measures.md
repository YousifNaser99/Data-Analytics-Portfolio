# DAX Measures

This document contains the main DAX measures created for the Sales Analytics Platform.

These measures were developed to support business intelligence analysis, KPI monitoring, profitability analysis, customer insights, product analysis, and time intelligence calculations.

---

# Executive KPI Measures

```DAX
Total Revenue =
SUM(FactSales[SalesAmount])

Total Cost =
SUM(FactSales[TotalProductCost])

Gross Profit =
SUM(FactSales[GrossProfit])

Profit Margin =
DIVIDE(
    [Gross Profit],
    [Total Revenue],
    0
)

Total Orders =
DISTINCTCOUNT(
    FactSales[SalesOrderNumber]
)

Units Sold =
SUM(
    FactSales[OrderQuantity]
)

Total Customers =
DISTINCTCOUNT(
    DimCustomer[CustomerKey]
)

# Sales Performance Measures
