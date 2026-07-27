USE AdventureWorksDW;
GO

CREATE OR ALTER VIEW vw_MonthlyPerformance
AS

WITH Monthly AS
(
    SELECT
        c.CalendarYear,
        c.MonthNumberOfYear,
        c.MonthName,

        SUM(f.SalesAmount)   AS Revenue,
        SUM(f.GrossProfit)   AS Profit,
        SUM(f.OrderQuantity) AS Units

    FROM FactSales f

    INNER JOIN DimCalendar c
        ON f.OrderDate = c.Date

    -- Remove incomplete July 2004
    WHERE NOT
    (
        c.CalendarYear = 2004
        AND c.MonthNumberOfYear = 7
    )

    GROUP BY
        c.CalendarYear,
        c.MonthNumberOfYear,
        c.MonthName
),


Base AS
(
    SELECT

        CalendarYear,
        MonthNumberOfYear,
        MonthName,

        Revenue,
        Profit,
        Units,


        -- Running Totals
        SUM(Revenue) OVER
        (
            ORDER BY CalendarYear, MonthNumberOfYear
        ) AS RunningRevenue,


        SUM(Profit) OVER
        (
            ORDER BY CalendarYear, MonthNumberOfYear
        ) AS RunningProfit,


        -- Previous Month
        LAG(Revenue) OVER
        (
            ORDER BY CalendarYear, MonthNumberOfYear
        ) AS PrevRevenue,


        LAG(Profit) OVER
        (
            ORDER BY CalendarYear, MonthNumberOfYear
        ) AS PrevProfit,


        -- Previous Year Same Month
        LAG(Revenue,12) OVER
        (
            ORDER BY CalendarYear, MonthNumberOfYear
        ) AS PrevYearRevenue,


        LAG(Profit,12) OVER
        (
            ORDER BY CalendarYear, MonthNumberOfYear
        ) AS PrevYearProfit,


        -- Rolling 3 Months
        AVG(Revenue) OVER
        (
            ORDER BY CalendarYear, MonthNumberOfYear
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ) AS RollingRevenue,


        AVG(Profit) OVER
        (
            ORDER BY CalendarYear, MonthNumberOfYear
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ) AS RollingProfit


    FROM Monthly
)


SELECT

    CalendarYear,

    MonthNumberOfYear,

    MonthName,


    CONCAT(
        CalendarYear,
        '-',
        FORMAT(MonthNumberOfYear,'00')
    ) AS Period,


    Revenue,

    Profit,

    Units,


    RunningRevenue,

    RunningProfit,


    RollingRevenue,

    RollingProfit,


    CAST
    (
        (
            (Revenue - PrevRevenue)
            * 100.0
        )
        /
        NULLIF(PrevRevenue,0)

        AS DECIMAL(10,2)

    ) AS MoMRevenue,


    CAST
    (
        (
            (Profit - PrevProfit)
            * 100.0
        )
        /
        NULLIF(PrevProfit,0)

        AS DECIMAL(10,2)

    ) AS MoMProfit,


    CAST
    (
        (
            (Revenue - PrevYearRevenue)
            * 100.0
        )
        /
        NULLIF(PrevYearRevenue,0)

        AS DECIMAL(10,2)

    ) AS YoYRevenue,


    CAST
    (
        (
            (Profit - PrevYearProfit)
            * 100.0
        )
        /
        NULLIF(PrevYearProfit,0)

        AS DECIMAL(10,2)

    ) AS YoYProfit


FROM Base;
GO