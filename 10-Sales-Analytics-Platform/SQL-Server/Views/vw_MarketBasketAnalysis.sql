USE AdventureWorksDW;
GO

CREATE OR ALTER VIEW vw_MarketBasketAnalysis
AS

/*==========================================================
    Product Support
==========================================================*/

WITH ProductSupport AS
(
    SELECT
        ProductKey,
        COUNT(DISTINCT SalesOrderNumber) AS ProductOrders
    FROM FactSales
    GROUP BY ProductKey
),

/*==========================================================
    Product Pairs
==========================================================*/

BasketPairs AS
(
    SELECT
        fs1.ProductKey AS ProductKeyA,
        fs2.ProductKey AS ProductKeyB,
        COUNT(DISTINCT fs1.SalesOrderNumber) AS PairOrders
    FROM FactSales fs1

    INNER JOIN FactSales fs2
        ON fs1.SalesOrderNumber = fs2.SalesOrderNumber
       AND fs1.ProductKey < fs2.ProductKey

    GROUP BY
        fs1.ProductKey,
        fs2.ProductKey
),

/*==========================================================
    Total Orders
==========================================================*/

TotalOrders AS
(
    SELECT
        COUNT(DISTINCT SalesOrderNumber) AS TotalOrders
    FROM FactSales
),

/*==========================================================
    Metrics
==========================================================*/

Metrics AS
(
    SELECT

        bp.ProductKeyA,
        bp.ProductKeyB,

        bp.PairOrders,

        t.TotalOrders,

        ps1.ProductOrders AS ProductA_Orders,
        ps2.ProductOrders AS ProductB_Orders,

        CAST(
            bp.PairOrders * 1.0 /
            t.TotalOrders
            AS DECIMAL(10,4)
        ) AS Support,

        CAST(
            bp.PairOrders * 1.0 /
            ps1.ProductOrders
            AS DECIMAL(10,4)
        ) AS Confidence,

        CAST(
            (
                bp.PairOrders * 1.0 /
                ps1.ProductOrders
            )
            /
            (
                ps2.ProductOrders * 1.0 /
                t.TotalOrders
            )
            AS DECIMAL(10,4)
        ) AS Lift

    FROM BasketPairs bp

    INNER JOIN ProductSupport ps1
        ON bp.ProductKeyA = ps1.ProductKey

    INNER JOIN ProductSupport ps2
        ON bp.ProductKeyB = ps2.ProductKey

    CROSS JOIN TotalOrders t
)

/*==========================================================
    Final Result
==========================================================*/

SELECT

    m.ProductKeyA,

    p1.ProductName AS ProductA,

    m.ProductKeyB,

    p2.ProductName AS ProductB,

    CONCAT(
        p1.ProductName,
        ' → ',
        p2.ProductName
    ) AS Recommendation,

    m.PairOrders,

    m.TotalOrders,

    m.ProductA_Orders,

    m.ProductB_Orders,

    m.Support,

    m.Confidence,

    m.Lift,

    CASE

        WHEN m.Lift < 1
            THEN '<1'

        WHEN m.Lift < 2
            THEN '1-2'

        WHEN m.Lift < 3
            THEN '2-3'

        WHEN m.Lift < 5
            THEN '3-5'

        ELSE '>5'

    END AS LiftClass,

    CASE

        WHEN m.Confidence < 0.20
            THEN '0-20%'

        WHEN m.Confidence < 0.40
            THEN '20-40%'

        WHEN m.Confidence < 0.60
            THEN '40-60%'

        WHEN m.Confidence < 0.80
            THEN '60-80%'

        ELSE '80-100%'

    END AS ConfidenceClass,

    CASE

        WHEN m.Lift >= 2
            THEN 'Strong Association'

        WHEN m.Lift >= 1
            THEN 'Moderate Association'

        ELSE 'Weak Association'

    END AS AssociationStrength,

    DENSE_RANK() OVER
    (
        ORDER BY
            m.Lift DESC
    ) AS RuleRank

FROM Metrics m

INNER JOIN DimProducts p1
    ON m.ProductKeyA = p1.ProductKey

INNER JOIN DimProducts p2
    ON m.ProductKeyB = p2.ProductKey;
GO