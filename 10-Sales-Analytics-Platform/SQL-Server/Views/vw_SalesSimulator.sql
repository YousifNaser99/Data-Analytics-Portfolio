USE AdventureWorksDW;
GO

CREATE OR ALTER VIEW vw_SalesSimulator
AS

SELECT

    -- Product
    P.Category,
    P.ProductName,

    -- Customer / Territory
    T.Country,
    C.IncomeSegment,

    -- Historical Average Quantity
    AVG(F.OrderQuantity) AS AvgQuantity,


    -- Average Selling Price Per Unit
    AVG(
        F.SalesAmount / NULLIF(F.OrderQuantity,0)
    ) AS AvgUnitPrice,


    -- Average Cost Per Unit
    AVG(
        F.TotalProductCost / NULLIF(F.OrderQuantity,0)
    ) AS AvgUnitCost,


    -- Average Margin
    SUM(F.GrossProfit) /
    NULLIF(SUM(F.SalesAmount),0)
    AS AvgMargin


FROM FactSales F


INNER JOIN DimProducts P
ON F.ProductKey = P.ProductKey


INNER JOIN DimTerritory T
ON F.SalesTerritoryKey = T.SalesTerritoryKey


INNER JOIN DimCustomers C
ON F.CustomerKey = C.CustomerKey


GROUP BY

    P.Category,
    P.ProductName,
    T.Country,
    C.IncomeSegment;
GO
