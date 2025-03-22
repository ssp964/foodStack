import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer


# Function to divide data into features (X) and target (y)
def divide_data(data: pd.DataFrame, target_column: str = "Amount"):
    """
    Divides the data into features (X) and target (y).

    Parameters:
    - data: input DataFrame to divide
    - target_column: Column to use as the target variable

    Returns:
    - X: Features DataFrame
    - y: Target Series
    """

    feature_columns = [col for col in data.columns if col != target_column]
    X = data[feature_columns]
    y = data[target_column]
    return X, y


# Function to preprocess the data
def preprocess_data(data: pd.DataFrame):
    """
    Preprocesses the data for scaling and encoding.

    Parameters:
    - data: DataFrame to preprocess

    Returns:
    - transformed_data: Preprocessed data as a NumPy array (ready for model input)
    - preprocessor: Fitted ColumnTransformer for consistent preprocessing
    """

    # Map the 'Day' column
    day_mapping = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6,
    }
    data = data.copy()
    data["Day"] = data["Day"].map(day_mapping)

    # preprocessing pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            # Scale 'Day' and 'Hour'
            ("scale", StandardScaler(), ["Day", "Hour"]),
            # One-hot encode 'Dish'
            ("onehot", OneHotEncoder(), ["Dish"]),
        ]
    )

    transformed_data = preprocessor.fit_transform(data)

    return transformed_data, preprocessor
