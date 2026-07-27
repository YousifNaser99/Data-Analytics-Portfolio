USE AdventureWorksDW;
GO

CREATE OR ALTER VIEW vw_ProductPerformance
AS

WITH ProductSummary AS
(

    SELECT

        p.ProductKey,
        p.ProductName,
        p.Category,
        p.SubCategory,
        p.PriceSegment,

        COUNT(DISTINCT f.SalesOrderNumber) AS Orders,

        SUM(f.OrderQuantity) AS UnitsSold,

        SUM(f.SalesAmount) AS Revenue,

        SUM(f.TotalProductCost) AS Cost,

        SUM(f.GrossProfit) AS Profit,

        CASE
            WHEN SUM(f.SalesAmount)=0 THEN 0
            ELSE
                SUM(f.GrossProfit)*1.0
                /
                SUM(f.SalesAmount)
        END AS ProfitMargin,

        CASE
            WHEN SUM(f.OrderQuantity)=0 THEN 0
            ELSE
                SUM(f.SalesAmount)
                /
                SUM(f.OrderQuantity)
        END AS AvgSellingPrice,

        CASE
            WHEN SUM(f.OrderQuantity)=0 THEN 0
            ELSE
                SUM(f.GrossProfit)
                /
                SUM(f.OrderQuantity)
        END AS ProfitPerUnit

    FROM FactSales f

    INNER JOIN DimProducts p
        ON f.ProductKey=p.ProductKey

    GROUP BY

        p.ProductKey,
        p.ProductName,
        p.Category,
        p.SubCategory,
        p.PriceSegment

),

Ranking AS
(

    SELECT

        *,

        DENSE_RANK() OVER
        (
            ORDER BY Revenue DESC
        ) AS RevenueRank,

        DENSE_RANK() OVER
        (
            ORDER BY Profit DESC
        ) AS ProfitRank,

        NTILE(4) OVER
        (
            ORDER BY Revenue DESC
        ) AS RevenueQuartile,

        SUM(Revenue) OVER
        (
            ORDER BY Revenue DESC
            ROWS BETWEEN
            UNBOUNDED PRECEDING
            AND CURRENT ROW
        ) AS CumRevenue,

        SUM(Revenue) OVER() AS TotalRevenue

    FROM ProductSummary

)

SELECT

    ProductKey,

    ProductName,

    Category,

    SubCategory,

    PriceSegment,

    Orders,

    UnitsSold,

    Revenue,

    Cost,

    Profit,

    ProfitMargin,

    AvgSellingPrice,

    ProfitPerUnit,

    RevenueRank,

    ProfitRank,

    RevenueQuartile,

    CumRevenue,

    TotalRevenue,

    Revenue * 1.0
    /
    TotalRevenue
    AS RevenueContribution,

    CumRevenue * 1.0
    /
    TotalRevenue
    AS CumRevenuePct,

    CASE

        WHEN
            CumRevenue * 1.0
            /
            TotalRevenue <= 0.80

        THEN 'A'

        WHEN
            CumRevenue * 1.0
            /
            TotalRevenue <= 0.95

        THEN 'B'

        ELSE 'C'

    END AS ABCClass

FROM Ranking;
GO
