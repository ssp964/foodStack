from processing.data_ingestion_fn import fetch_current_data
from processing.model_predict_fn import daily_predict
from utils.server import PostgresConnector

db = PostgresConnector()


def daily_update_job():
    print("Running daily model update...")

    # Fetch today's data
    today_df = fetch_current_data()

    if today_df.empty:
        print("No data found for today. Skipping update.")
        return

    # Perform incremental update
    predicted_data = daily_predict(today_df)
    print("Daily model update completed.")

    db.insert_dataframe(table_name="predicted_data", df=predicted_data)

    print("Predicted data pushed into database successfully")
