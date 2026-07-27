USE AdventureWorksDW;
GO

CREATE OR ALTER VIEW vw_ExecutiveKPI
AS
SELECT

    SUM(F.SalesAmount) AS Revenue,

    SUM(F.GrossProfit) AS Profit,

    SUM(F.OrderQuantity) AS UnitsSold,

    COUNT(DISTINCT F.SalesOrderNumber) AS Orders,

    SUM(F.GrossProfit) * 1.0 
    / NULLIF(SUM(F.SalesAmount),0) AS GrossMargin,

    SUM(F.SalesAmount) * 1.0
    / NULLIF(COUNT(DISTINCT F.SalesOrderNumber),0) AS AverageOrderValue

FROM FactSales F
GO
