import os
import joblib
import mlflow
import mlflow.sklearn
import numpy as np
from datetime import datetime
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_squared_error

# Define model directory at the root of prediction_backend
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")
os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")


def train_and_export_model(X_ip, y_ip):
    """
    Train a model using provided features (X_ip) and target (y_ip),
    then export the model and log only parameters, weights, and performance via MLflow.
    """
    print("Training model...")
    model = SGDRegressor(max_iter=1000, tol=1e-3, learning_rate="adaptive")
    model.fit(X_ip, y_ip)
    print("Model trained.")

    # Save locally
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to: {MODEL_PATH}")

    # Log to MLflow
    with mlflow.start_run(run_name="initial_training"):
        # Log model params
        mlflow.log_params(
            {
                "model_type": "SGDRegressor",
                "max_iter": 1000,
                "learning_rate": "adaptive",
                "update_type": "initial",
            }
        )

        # Log internal model weights
        mlflow.log_param("coef", np.array2string(model.coef_, precision=3))
        mlflow.log_param("intercept", np.array2string(model.intercept_, precision=3))

        # Log performance metric
        y_pred = model.predict(X_ip)
        mlflow.log_metric("mse", mean_squared_error(y_ip, y_pred))

        # Log the model only (no input_example, no signature)
        mlflow.sklearn.log_model(model, artifact_path="model")

        # Log the saved model file
        mlflow.log_artifact(MODEL_PATH)

        print("Model and parameters logged to MLflow.")

    return model
