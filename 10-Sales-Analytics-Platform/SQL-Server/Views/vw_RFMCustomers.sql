USE AdventureWorksDW;
GO

CREATE OR ALTER VIEW vw_RFMCustomers AS
WITH CustomerRFM AS
(
    SELECT
        c.CustomerKey,

        MAX(f.OrderDate) AS LastPurchaseDate,

        DATEDIFF(
            DAY,
            MAX(f.OrderDate),
            (SELECT MAX(OrderDate) FROM FactSales)
        ) AS Recency,

        COUNT(DISTINCT f.SalesOrderNumber) AS Frequency,

        SUM(f.SalesAmount) AS Monetary

    FROM FactSales f

    JOIN DimCustomers c
        ON f.CustomerKey = c.CustomerKey

    GROUP BY
        c.CustomerKey
),

Scored AS
(
    SELECT
        *,

        NTILE(5) OVER(ORDER BY Recency DESC) AS R_Score,

        NTILE(5) OVER(ORDER BY Frequency ASC) AS F_Score,

        NTILE(5) OVER(ORDER BY Monetary ASC) AS M_Score

    FROM CustomerRFM
)

SELECT

    CustomerKey,

    Recency,

    Frequency,

    Monetary,

    R_Score,

    F_Score,

    M_Score,

    CONCAT(R_Score,F_Score,M_Score) AS RFM_Score,

    CASE

        WHEN R_Score >=4
         AND F_Score >=4
         AND M_Score >=4
            THEN 'Champions'

        WHEN R_Score >=4
         AND F_Score >=3
            THEN 'Loyal Customers'

        WHEN R_Score >=4
         AND M_Score >=3
            THEN 'Potential Loyalists'

        WHEN R_Score BETWEEN 2 AND 3
         AND F_Score >=3
            THEN 'Need Attention'

        WHEN R_Score <=2
         AND F_Score >=3
            THEN 'At Risk'

        WHEN R_Score =1
         AND F_Score =1
            THEN 'Lost Customers'

        ELSE 'Others'

    END AS CustomerSegment

FROM Scored;