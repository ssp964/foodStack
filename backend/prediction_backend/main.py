from train import train_model
from predict import update_model
from data_ingestion_fn import connect_to_mongo, fetch_current_date_data
from datetime import datetime
import time

mongo_uri = "..."  # put your env/config here
database_name = "..."
collection_name = "..."
collection_name_send = "..."


def continuous_training_pipeline():
    model, preprocessor = train_model()

    while True:
        now = datetime.now()
        if now.hour == 23 and now.minute == 55:
            collection = connect_to_mongo(mongo_uri, database_name, collection_name)
            today_data = fetch_current_date_data(collection)

            if not today_data.empty:
                model = update_model(model, today_data)
            else:
                print("No data to update.")

            time.sleep(86400)  # sleep 1 day
        else:
            time.sleep(60)


if __name__ == "__main__":
    continuous_training_pipeline()
