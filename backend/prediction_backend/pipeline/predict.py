from datetime import datetime
import time


def update_model(model_partial_fit, today_data):
    """
    Update the model using new data from today and adjust predictions in the predicted_data MongoDB collection.

    Parameters:
    - model_partial_fit: The partially trained model (e.g., SGDRegressor with partial_fit)
    - today_data: DataFrame containing today's data
    - preprocessor: Fitted ColumnTransformer for preprocessing

    Returns:
    - model_partial_fit: Updated model
    """
    # Step 1: Connect to the predicted_data collection
    predicted_data_collection = connect_to_mongo(
        mongo_uri, database_name, collection_name_send
    )

    # Step 2: Prepare today's data for training
    X_today = today_data[["Day", "Hour", "Dish"]]
    y_today = today_data["Amount"]

    # Preprocess data before partial fitting
    X_today_preprocessed, preprocessor = preprocess_data(X_today)

    # Perform partial fit (online learning)
    model_partial_fit.partial_fit(X_today_preprocessed, y_today)
    print("Model updated with today's data.")

    # Predict the amounts for today's data
    today_data["Predicted Amount"] = model_partial_fit.predict(X_today_preprocessed)

    day_mapping = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6,
    }
    today_data = today_data.copy()  # Avoid modifying the original DataFrame
    today_data["Day"] = today_data["Day"].map(day_mapping)

    # Step 3: Update MongoDB with new predictions
    for _, row in today_data.iterrows():
        day_of_week = row["Day"]
        hour = row["Hour"]
        dish = row["Dish"]
        predicted_amount = row["Predicted Amount"]

        # Update the corresponding document in MongoDB
        result = predicted_data_collection.update_one(
            {"Day": day_of_week, "Hour": hour, "Dish": dish},  # Match criteria
            {
                "$set": {"Predicted Amount": predicted_amount}
            },  # Update the predicted amount
        )

        # Optional: Print update status
        if result.matched_count > 0:
            print(
                f"Updated Predicted Amount for Day: {day_of_week}, Hour: {hour}, Dish: {dish}"
            )
        else:
            print(
                f"No matching document found for Day: {day_of_week}, Hour: {hour}, Dish: {dish}"
            )

    print("MongoDB predictions updated for the current day.")
    return model_partial_fit


current_time = datetime.now()
print(current_time.minute)


while True:
    current_time = datetime.now()

    # Check if it's 11:55 PM
    if current_time.hour == 5 and current_time.minute == 46:
        print(f"\n[{current_time}] Fetching today's data for model update...")

        # Fetch today's data from MongoDB (actual data for the current date)
        collection = connect_to_mongo(mongo_uri, database_name, collection_name)
        today_data = fetch_current_date_data(collection)

        if not today_data.empty:
            print("Today's data fetched successfully. Updating the model...")

            # Update the model and predictions using today's data
            model = update_model(model, today_data)

            print("Model updated and predictions stored for the day.")

        else:
            print("No new data available for today. Skipping update.")

        # Wait for the next day
        time.sleep(86400)  # Sleep for 24 hours
    else:
        # Sleep for a minute and recheck
        time.sleep(60)
