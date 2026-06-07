-- ============================================================
-- SALES PERFORMANCE DASHBOARD -- SQL ANALYSIS
-- Project by: Ayushmaan Pandey | BCA, CSJMU
-- Dataset: 1000 orders | Year: 2023 | India Sales Data
-- ============================================================

-- ============================================================
-- 1. OVERALL BUSINESS SUMMARY
-- ============================================================
SELECT
    COUNT(DISTINCT Order_ID)          AS Total_Orders,
    ROUND(SUM(Revenue), 0)            AS Total_Revenue_INR,
    ROUND(SUM(Profit), 0)             AS Total_Profit_INR,
    ROUND(AVG(Profit_Margin_Pct), 2)  AS Avg_Profit_Margin_Pct,
    SUM(Quantity)                     AS Total_Units_Sold
FROM sales_data;

-- ============================================================
-- 2. REVENUE & PROFIT BY REGION
-- ============================================================
SELECT
    Region,
    COUNT(Order_ID)                   AS Total_Orders,
    ROUND(SUM(Revenue), 0)            AS Total_Revenue,
    ROUND(SUM(Profit), 0)             AS Total_Profit,
    ROUND(AVG(Profit_Margin_Pct), 2)  AS Avg_Margin_Pct,
    ROUND(SUM(Revenue) * 100.0 /
        (SELECT SUM(Revenue) FROM sales_data), 2) AS Revenue_Share_Pct
FROM sales_data
GROUP BY Region
ORDER BY Total_Revenue DESC;

-- ============================================================
-- 3. TOP 5 PERFORMING PRODUCTS BY REVENUE
-- ============================================================
SELECT
    Product,
    Category,
    SUM(Quantity)                     AS Units_Sold,
    ROUND(SUM(Revenue), 0)            AS Total_Revenue,
    ROUND(SUM(Profit), 0)             AS Total_Profit,
    ROUND(AVG(Profit_Margin_Pct), 2)  AS Avg_Margin_Pct
FROM sales_data
GROUP BY Product, Category
ORDER BY Total_Revenue DESC
LIMIT 5;

-- ============================================================
-- 4. MONTHLY REVENUE TREND (2023)
-- ============================================================
SELECT
    Month,
    COUNT(Order_ID)                   AS Orders,
    ROUND(SUM(Revenue), 0)            AS Monthly_Revenue,
    ROUND(SUM(Profit), 0)             AS Monthly_Profit,
    ROUND(AVG(Profit_Margin_Pct), 2)  AS Avg_Margin
FROM sales_data
GROUP BY Month
ORDER BY MIN(Date);

-- ============================================================
-- 5. SALESPERSON PERFORMANCE LEADERBOARD
-- ============================================================
SELECT
    Salesperson,
    COUNT(Order_ID)                   AS Total_Orders,
    ROUND(SUM(Revenue), 0)            AS Total_Revenue,
    ROUND(SUM(Profit), 0)             AS Total_Profit,
    ROUND(AVG(Profit_Margin_Pct), 2)  AS Avg_Margin_Pct,
    RANK() OVER (ORDER BY SUM(Revenue) DESC) AS Revenue_Rank
FROM sales_data
GROUP BY Salesperson
ORDER BY Total_Revenue DESC;

-- ============================================================
-- 6. CATEGORY-WISE PERFORMANCE
-- ============================================================
SELECT
    Category,
    COUNT(DISTINCT Product)           AS Products_Count,
    SUM(Quantity)                     AS Units_Sold,
    ROUND(SUM(Revenue), 0)            AS Total_Revenue,
    ROUND(SUM(Profit), 0)             AS Total_Profit,
    ROUND(AVG(Profit_Margin_Pct), 2)  AS Avg_Margin_Pct
FROM sales_data
GROUP BY Category
ORDER BY Total_Revenue DESC;

-- ============================================================
-- 7. QUARTERLY PERFORMANCE COMPARISON
-- ============================================================
SELECT
    Quarter,
    COUNT(Order_ID)                   AS Total_Orders,
    ROUND(SUM(Revenue), 0)            AS Quarterly_Revenue,
    ROUND(SUM(Profit), 0)             AS Quarterly_Profit,
    ROUND(AVG(Profit_Margin_Pct), 2)  AS Avg_Margin_Pct
FROM sales_data
GROUP BY Quarter
ORDER BY Quarter;

-- ============================================================
-- 8. DISCOUNT IMPACT ANALYSIS
-- ============================================================
SELECT
    Discount_Pct,
    COUNT(Order_ID)                   AS Orders,
    ROUND(AVG(Revenue), 0)            AS Avg_Revenue_Per_Order,
    ROUND(AVG(Profit_Margin_Pct), 2)  AS Avg_Margin_Pct
FROM sales_data
GROUP BY Discount_Pct
ORDER BY Discount_Pct;

-- ============================================================
-- 9. REVENUE LEAKAGE -- LOW MARGIN ORDERS (Below 25%)
-- ============================================================
SELECT
    Order_ID, Date, Region, Product,
    Quantity, Revenue, Profit,
    Profit_Margin_Pct
FROM sales_data
WHERE Profit_Margin_Pct < 25
ORDER BY Profit_Margin_Pct ASC
LIMIT 10;

-- ============================================================
-- 10. REGION + CATEGORY CROSS ANALYSIS
-- ============================================================
SELECT
    Region,
    Category,
    ROUND(SUM(Revenue), 0)            AS Revenue,
    ROUND(SUM(Profit), 0)             AS Profit
FROM sales_data
GROUP BY Region, Category
ORDER BY Region, Revenue DESC;
