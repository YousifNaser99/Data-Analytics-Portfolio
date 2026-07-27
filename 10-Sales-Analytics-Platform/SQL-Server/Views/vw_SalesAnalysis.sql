USE AdventureWorksDW;
GO

CREATE VIEW vw_SalesAnalysis
AS

SELECT

    f.SalesOrderNumber,
    f.SalesOrderLineNumber,
    f.OrderDate,
    c.CalendarYear,
    c.MonthName,
    c.MonthNumberOfYear,
    c.CalendarQuarter,

    p.ProductKey,
    p.ProductName,
    p.Category,
    p.SubCategory,
    p.PriceSegment,

    t.Country,
    t.Region,

    cu.CustomerKey,
    cu.Name,
    cu.Gender,
    cu.AgeGroup,
    cu.IncomeSegment,

    f.OrderQuantity,
    f.SalesAmount,
    f.TotalProductCost,
    f.GrossProfit,
    f.GrossMarginPercent,
    f.DiscountAmount,
    f.Freight

FROM FactSales f

INNER JOIN DimProducts p
ON f.ProductKey=p.ProductKey

INNER JOIN DimCustomers cu
ON f.CustomerKey=cu.CustomerKey

INNER JOIN DimCalendar c
ON f.OrderDate=c.Date

INNER JOIN DimTerritory t
ON f.SalesTerritoryKey=t.SalesTerritoryKey;
