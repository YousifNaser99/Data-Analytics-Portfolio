USE AdventureWorksDW;
GO

CREATE OR ALTER VIEW vw_FinancialAnalysis
AS

SELECT

    -- Calendar
    C.CalendarYear,
    C.CalendarQuarter,
    C.MonthNumberOfYear,
    C.MonthName,
    C.Date,

    -- Product
    P.Category,
    P.Subcategory,
    P.ProductName,

    -- Territory
    T.Country,
    T.Region,

    -- Order
    F.SalesOrderNumber,

    -- Metrics
    F.OrderQuantity AS Units,
    F.SalesAmount AS Revenue,
    F.TotalProductCost AS Cost,
    F.GrossProfit AS Profit,
    F.TaxAmt AS Tax,
    F.Freight AS Freight,

    CASE
        WHEN F.SalesAmount = 0 THEN 0
        ELSE F.GrossProfit * 1.0 / F.SalesAmount
    END AS ProfitMargin

FROM FactSales F

INNER JOIN DimCalendar C
    ON F.OrderDate = C.Date

INNER JOIN DimProducts P
    ON F.ProductKey = P.ProductKey

INNER JOIN DimTerritory T
    ON F.SalesTerritoryKey = T.SalesTerritoryKey;

GO
