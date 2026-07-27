USE AdventureWorksDW;
GO

CREATE VIEW vw_CategoryPerformance
AS

SELECT

p.Category,

SUM(f.SalesAmount) Revenue,

SUM(f.GrossProfit) Profit,

SUM(f.OrderQuantity) Units

FROM FactSales f

JOIN DimProducts p

ON f.ProductKey=p.ProductKey

GROUP BY

p.Category;
