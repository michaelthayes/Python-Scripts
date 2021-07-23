
PRINT 'Getting Tables'
SELECT	 
    db_name() as 'db_nm',
    ss.name AS 'schema_nm',
    st.name AS 'table_nm',    
    sc.name as 'column_nm',
    sc.column_id as 'column_ordr'
FROM sys.tables st
    INNER JOIN sys.columns sc ON st.object_id = sc.object_id
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
    sc.column_id as 'column_ordr'
FROM sys.views st
    INNER JOIN sys.columns sc ON st.object_id = sc.object_id
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





