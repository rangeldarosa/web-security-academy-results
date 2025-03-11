
class SQLComments:
    """Enum-like class for SQL comment syntax across different database systems."""
    
    # Standard SQL comments
    MYSQL = "-- "
    MYSQL_HASH = "#"
    MYSQL_BLOCK = "/* */"
    
    # Oracle specific
    ORACLE = "-- "
    ORACLE_BLOCK = "/* */"
    
    # PostgreSQL specific
    POSTGRES = "-- "
    POSTGRES_BLOCK = "/* */"
    
    # Microsoft SQL Server specific
    MSSQL = "-- "
    MSSQL_BLOCK = "/* */"
    
    # SQLite specific
    SQLITE = "-- "
    SQLITE_BLOCK = "/* */"