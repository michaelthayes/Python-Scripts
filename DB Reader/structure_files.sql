
PRINT 'Getting Tables'
SELECT	  
    db_name() as 'db_nm', 
    ss.name AS 'schema_nm', 
    st.name AS 'table_nm', 
    sc.name as 'column_nm', 
    sc.column_id as 'column_ordr', 
    sty.name + CASE 
        WHEN sty.name IN ('char', 'varchar') AND sc.max_length = -1 THEN '(max' 
        WHEN sty.name IN ('char', 'varchar', 'numeric', 'decimal') THEN '(' + CONVERT(VARCHAR(20), sc.max_length) 
        WHEN sty.name IN ('nchar', 'nvarchar') THEN '(' + CONVERT(VARCHAR(20), sc.max_length/2) 
        ELSE '' 
    END + CASE 
        WHEN sty.name IN ('numeric', 'decimal') THEN ', ' + CONVERT(VARCHAR(20), sc.scale) + ')' 
        WHEN sty.name IN ('char', 'nchar', 'varchar', 'nvarchar') THEN ')' 
        ELSE '' 
    END as 'data_type', 
    CASE sc.is_nullable  
        WHEN 1 THEN 'Y'  
        ELSE 'N' 
    END AS 'nullable' 
FROM sys.tables st 
    INNER JOIN sys.columns sc 
        LEFT OUTER JOIN sys.types sty ON sc.system_type_id = sty.user_type_id 
    ON st.object_id = sc.object_id 
    INNER JOIN sys.schemas ss ON st.schema_id = ss.schema_id 
WHERE st.type = 'U' 
AND st.name <> 'dtproperties' 
ORDER BY ss.name, st.name, sc.column_id
GO


PRINT 'Getting Views'
SELECT	 
    db_name() as 'db_nm', 
    ss.name AS 'schema_nm', 
    st.name AS 'table_nm', 
    sc.name as 'column_nm', 
    sc.column_id as 'column_ordr', 
    sty.name + CASE 
        WHEN sty.name IN ('char', 'varchar') AND sc.max_length = -1 THEN '(max' 
        WHEN sty.name IN ('char', 'varchar', 'numeric', 'decimal') THEN '(' + CONVERT(VARCHAR(20), sc.max_length) 
        WHEN sty.name IN ('nchar', 'nvarchar') THEN '(' + CONVERT(VARCHAR(20), sc.max_length/2) 
        ELSE '' 
    END + CASE 
        WHEN sty.name IN ('numeric', 'decimal') THEN ', ' + CONVERT(VARCHAR(20), sc.scale) + ')' 
        WHEN sty.name IN ('char', 'nchar', 'varchar', 'nvarchar') THEN ')' 
        ELSE '' 
    END as 'data_type', 
    CASE sc.is_nullable  
        WHEN 1 THEN 'Y'  
        ELSE 'N' 
    END AS 'nullable' 
FROM sys.views st
    INNER JOIN sys.columns sc 
        LEFT OUTER JOIN sys.types sty ON sc.system_type_id = sty.user_type_id 
    ON st.object_id = sc.object_id 
    INNER JOIN sys.schemas ss ON st.schema_id = ss.schema_id
WHERE st.type = 'U'
AND st.name <> 'dtproperties'
ORDER BY ss.name, st.name, sc.column_id
GO



-- This query retusn all sproc's which contain a value
SELECT	db_name() as 'db_nm',
        ssc.name as 'schema_name',
        sp.name AS 'sproc_name'
FROM sys.procedures sp
    INNER JOIN sys.schemas ssc ON sp.schema_id = ssc.schema_id
WHERE sp.name not like 'dt_%'
ORDER BY ssc.name, sp.name





