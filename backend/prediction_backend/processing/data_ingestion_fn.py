import pandas as pd
from datetime import datetime
from utils.server import PostgresConnector

db = PostgresConnector()


def fetch_all_data():
    """
    Fetch all historical data up to the current date from PostgreSQL.
    Filters out future records based on the 'date' column.
    """

    query = """
        SELECT * 
        FROM actual_data
    """

    now = datetime.now()
    data = db.query_to_dataframe(query)
    return data


def fetch_current_data():
    """
    Fetch only the rows from PostgreSQL that match today's date (ignores time).

    Returns:
    - current_date_data: Pandas DataFrame with today's records
    """
    query = """
        SELECT * FROM actual_data
        WHERE DATE(date) = %s
    """
    today = datetime.now().date()
    data = db.query_to_dataframe(query, params=(today,))
    return data
