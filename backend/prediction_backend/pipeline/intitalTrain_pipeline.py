from processing.data_ingestion_fn import fetch_all_data
from processing.data_transformation_fn import divide_data
from processing.model_train_fn import train_and_export_model
from processing.data_transformation_fn import preprocess_data
from processing.model_predict_fn import init_predict
from datetime import datetime
from utils.server import PostgresConnector

db = PostgresConnector()


def run_initial_training_pipeline():
    """
    Runs the full pipeline: load data → preprocess → train → export model.
    """
    print("Fetching all historical data...")
    data = fetch_all_data()

    if data.empty:
        print("No data available to train.")
        return

    print("Splitting data into features and target...")
    X, y = divide_data(data, target_column="quantity")

    print("Preprocessing input features...")
    X_processed, preprocessor = preprocess_data(X)

    print("Running training and export...")
    model = train_and_export_model(X_processed, y)
    print("Initial training pipeline completed.")

    predicted_data = init_predict(X, model, preprocessor)

    db.insert_dataframe(table_name="predicted_data", df=predicted_data)

    print("Intial predicted data pushed into database successfully")
