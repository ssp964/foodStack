import pandas as pd
from datetime import datetime
import pandas as pd
from datetime import datetime
from utils.server import PostgresConnector


# Initialize connector
db = PostgresConnector()


# 1. Test Insert
def test_insert_dataframe():
    test_data = pd.DataFrame(
        [
            {
                "date": datetime.now(),
                "day_of_week": "Friday",
                "hour": 12,
                "dish": "Grilled Chicken",
                "quantity": 3,
                "price": 250,
            },
            {
                "date": datetime.now(),
                "day_of_week": "Friday",
                "hour": 13,
                "dish": "Pasta",
                "quantity": 2,
                "price": 180,
            },
        ]
    )

    db.insert_dataframe("actual_data", test_data)
    print("Insert test passed.")


# 2. Test Query
def test_query_to_dataframe():
    query = "SELECT * FROM actual_data ORDER BY id DESC LIMIT 5"
    result_df = db.query_to_dataframe(query)
    print("Query test passed. Retrieved rows:")
    print(result_df)


# 3. Test get_connection + manual close
def test_manual_connection_close():
    with db.get_connection() as conn:
        print("Got connection from pool.")
        db.close(conn)
        print("Closed connection manually.")


# Run all tests
if __name__ == "__main__":
    test_manual_connection_close()
    # test_insert_dataframe()
    test_query_to_dataframe()
