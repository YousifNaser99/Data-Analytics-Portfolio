USE AdventureWorksDW;
GO

CREATE VIEW vw_TerritoryPerformance
AS

SELECT

t.Country,

t.Region,

SUM(f.SalesAmount) Revenue,

SUM(f.GrossProfit) Profit,

SUM(f.OrderQuantity) Units

FROM FactSales f

JOIN DimTerritory t

ON f.SalesTerritoryKey=t.SalesTerritoryKey

GROUP BY

t.Country,

t.Region;