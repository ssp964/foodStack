import os
import numpy as np
import pandas as pd
from processing.data_transformation_fn import preprocess_data
import joblib
import mlflow
import mlflow.sklearn
from sklearn.metrics import mean_squared_error
from datetime import datetime


# Define model directory at the root of prediction_backend
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")


def init_predict(X_input, model, preprocessor):
    """
    Load the trained model and use it to predict the target values for the given input features.

    Parameters:
        X_input (pd.DataFrame or np.ndarray): Input features

    Returns:
        np.ndarray: Predicted target values
    """
    # Validate input
    if not isinstance(X_input, (pd.DataFrame, np.ndarray)):
        raise ValueError("X_input must be a pandas DataFrame or NumPy ndarray.")

    # Get unique dishes
    dishes = X_input["dish"].unique()
    print(f"Number of unique dishes: {len(dishes)}")

    # Generate all combinations of Day, Hour, and Dish
    prediction_data = []
    id = 1
    for day_of_week in range(7):  # 7 days in a week
        for hour in range(24):  # 24 hours in a day
            for dish in dishes:  # Loop through unique dishes
                prediction_data.append([id, day_of_week, hour, dish])
                id += 1

    # Create DataFrame
    prediction_data = pd.DataFrame(
        prediction_data, columns=["id", "day_of_week", "hour", "dish"]
    )

    final_data = prediction_data.drop(columns=["id"])

    # Preprocess the prediction data to match training features
    transformed_data = preprocessor.transform(final_data)

    # Perform prediction
    prediction_data["predicted_quantity"] = model.predict(transformed_data)

    # Assuming 'X' still has dish -> price mapping
    dish_prices = X_input[["dish", "price"]].drop_duplicates()

    # Merge prices into predictions
    prediction_data = prediction_data.merge(dish_prices, on="dish", how="left")

    return prediction_data


def daily_predict(X_ip):
    X_today = X_ip[["day_of_week", "hour", "dish"]]
    y_today = X_ip["quantity"]

    # Assuming 'X' still has dish -> price mapping
    dish_prices = X_ip[["dish", "price"]].drop_duplicates()

    # Merge prices into predictions
    X_today = X_today.merge(dish_prices, on="dish", how="left")

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Trained model not found. Run initial training first.")

    model = joblib.load(MODEL_PATH)

    # Preprocess data before partial fitting
    print("Preprocessing input features...")
    X_today_preprocessed, preprocessor = preprocess_data(X_today)

    # Perform partial fit (online learning)
    print("Performing partial_fit with new data...")
    model.partial_fit(X_today_preprocessed, y_today)
    print("Model updated with today's data.")

    # Save updated model
    joblib.dump(model, MODEL_PATH)
    print(f"Updated model saved to: {MODEL_PATH}")

    # Log to MLflow
    with mlflow.start_run(
        run_name=f"model_update_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    ):
        # Log params
        mlflow.log_params({"model_type": "SGDRegressor", "update_type": "partial_fit"})

        # Log updated weights
        mlflow.log_param("coef", np.array2string(model.coef_, precision=3))
        mlflow.log_param("intercept", np.array2string(model.intercept_, precision=3))

        # Log performance metric
        y_pred = model.predict(X_today_preprocessed)
        mlflow.log_metric("mse", mean_squared_error(y_today, y_pred))

        # Log updated model (no schema, no example)
        mlflow.sklearn.log_model(model, artifact_path="model_update")

        # Log the updated model file
        mlflow.log_artifact(MODEL_PATH)

        print("Updated model logged to MLflow.")

    prediction_data = X_today.copy()  # Avoid modifying the original DataFrame

    # Predict the amounts for today's data
    prediction_data["predicted_quantity"] = model.predict(X_today_preprocessed)

    day_mapping = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6,
    }
    prediction_data["day_of_week"] = prediction_data["day_of_week"].map(day_mapping)

    return prediction_data
