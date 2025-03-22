from sklearn.linear_model import SGDRegressor
from datetime import datetime
import pandas as pd


def initial_prediction(model, preprocessor, X):
    """
    Generate initial predictions based on all combinations of days, hours, and dishes.

    Parameters:
    - model: The trained model (e.g., XGBRegressor)
    - preprocessor: The fitted ColumnTransformer for preprocessing
    - X: Original DataFrame to extract unique dishes

    Returns:
    - prediction_data: DataFrame with predictions for all combinations
    """
    # Get unique dishes
    dishes = X["Dish"].unique()
    print(f"Number of unique dishes: {len(dishes)}")

    # Generate all combinations of Day, Hour, and Dish
    prediction_data = []
    for day_of_week in range(7):  # 7 days in a week
        for hour in range(24):  # 24 hours in a day
            for dish in dishes:  # Loop through unique dishes
                prediction_data.append([day_of_week, hour, dish])

    # Create DataFrame
    prediction_data = pd.DataFrame(prediction_data, columns=["Day", "Hour", "Dish"])

    # Preprocess the prediction data to match training features
    transformed_data = preprocessor.transform(prediction_data)

    # Make predictions
    prediction_data["Predicted Amount"] = model.predict(transformed_data)

    print("\nInitial Predictions:")
    return prediction_data


def main():
    # Connect to MongoDB
    collection = connect_to_mongo(mongo_uri, database_name, collection_name)

    # Fetch all data from MongoDB
    fetched_data = fetch_all_data_from_mongo(collection)
    print(f"Fetched Data:\n{fetched_data.head()}")

    # Transform the data
    print("\nDividing Data into Features and Target...")
    X, y = divide_data(fetched_data, target_column="Amount")

    print("\nPreprocessing Feature Data...")
    processed_X, preprocessor = preprocess_data(X)

    model = SGDRegressor(max_iter=1000, tol=1e-3, learning_rate="adaptive")

    # Train the model
    model.fit(processed_X, y)
    print(processed_X.shape)
    print("Initial model training complete.")

    dishes = X["Dish"].unique()
    print(len(dishes))

    # Generate predictions
    predicted_df = initial_prediction(model, preprocessor, X)
    print("\nInitial Predictions:")
    print(predicted_df)

    # # Connect to MongoDB for sending data
    collection_pred = connect_to_mongo(mongo_uri, database_name, collection_name_send)

    # # Insert the predicted DataFrame into MongoDB
    insert_dataframe_to_mongo(collection_pred, predicted_df)
    print("Predicted data sent.")

    return model


if __name__ == "__main__":
    model = main()


current_time = datetime.now()
print(current_time.minute)
