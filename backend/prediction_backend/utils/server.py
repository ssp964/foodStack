import psycopg2
from psycopg2 import pool
import pandas as pd
import os
from contextlib import contextmanager


class PostgresConnector:
    def __init__(self):
        self.connection_pool = psycopg2.pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("POSTGRES_DB", "foodstack_db"),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", "postgres"),
            port=os.getenv("DB_PORT", "5432"),
        )

    @contextmanager
    def get_connection(self):
        """Context manager for acquiring and releasing a pooled connection"""
        conn = self.connection_pool.getconn()
        try:
            yield conn
        finally:
            self.connection_pool.putconn(conn)  # Return to pool

    def query_to_dataframe(self, query, params=None):
        """Execute a SQL query and return results as a pandas DataFrame"""
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn, params=params)

    def insert_dataframe(self, table_name, df):
        """Insert a pandas DataFrame into a PostgreSQL table"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cols = ",".join(df.columns)
            placeholders = ",".join(["%s"] * len(df.columns))
            insert_query = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"
            records = [tuple(x) for x in df.to_numpy()]
            cursor.executemany(insert_query, records)
            conn.commit()

    def close(self, conn):
        """Close a single connection (used with caution)"""
        if conn:
            conn.close()
