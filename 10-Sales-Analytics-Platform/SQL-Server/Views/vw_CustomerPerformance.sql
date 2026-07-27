USE AdventureWorksDW;
GO

CREATE OR ALTER VIEW vw_CustomerPerformance
AS

WITH CustomerSummary AS
(
    SELECT

        C.CustomerKey,

        C.Name,

        C.Gender,

        C.AgeGroup,

        C.IncomeSegment,

        T.Country,

        T.Region,

        COUNT(DISTINCT F.SalesOrderNumber) AS Orders,

        SUM(F.OrderQuantity) AS Units,

        SUM(F.SalesAmount) AS Revenue,

        SUM(F.GrossProfit) AS Profit,

        CASE
            WHEN SUM(F.SalesAmount) = 0 THEN 0
            ELSE SUM(F.GrossProfit) * 1.0 / SUM(F.SalesAmount)
        END AS ProfitMargin,

        CASE
            WHEN COUNT(DISTINCT F.SalesOrderNumber) = 0 THEN 0
            ELSE SUM(F.SalesAmount) * 1.0
                 / COUNT(DISTINCT F.SalesOrderNumber)
        END AS AvgOrderValue,

        CASE
            WHEN SUM(F.OrderQuantity) = 0 THEN 0
            ELSE SUM(F.SalesAmount) * 1.0
                 / SUM(F.OrderQuantity)
        END AS RevenuePerUnit

    FROM FactSales F

    INNER JOIN DimCustomers C
        ON F.CustomerKey = C.CustomerKey

    INNER JOIN DimTerritory T
        ON F.SalesTerritoryKey = T.SalesTerritoryKey

    GROUP BY

        C.CustomerKey,
        C.Name,
        C.Gender,
        C.AgeGroup,
        C.IncomeSegment,
        T.Country,
        T.Region
)

SELECT

    CustomerKey,
    Name,
    Gender,
    AgeGroup,
    IncomeSegment,
    Country,
    Region,
    Orders,
    Units,
    Revenue,
    Profit,
    ProfitMargin,
    AvgOrderValue,
    RevenuePerUnit,

    CASE
        WHEN Orders = 1 THEN 'One-Time'
        ELSE 'Repeat'
    END AS CustomerType,

    CASE
        WHEN Revenue >= AVG(Revenue) OVER ()
            THEN 'High Value'
        ELSE 'Standard'
    END AS CustomerValue,

    NTILE(4) OVER (
        ORDER BY Revenue DESC
    ) AS RevenueQuartile,

    DENSE_RANK() OVER (
        ORDER BY Revenue DESC
    ) AS RevenueRank,

    DENSE_RANK() OVER (
        ORDER BY Profit DESC
    ) AS ProfitRank

FROM CustomerSummary;