SET NOCOUNT ON

SELECT TOP 100 *
FROM eCommerce..Calendar
GO


SELECT TOP 100 *
INTO #tmp
FROM GoogleAnalytics..SiteVisitsLog
GO

SELECT TOP 100 *
from #tmp
GO


SELECT TOP 100 *
FROM Northwind..Categories
GO

