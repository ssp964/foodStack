# Project Overview

This repository consists of Jupyter Notebooks designed to handle data ingestion, transformation, model training, and prediction tasks for a machine learning pipeline. All operations are integrated with MongoDB for data storage and retrieval. Below is a detailed description of each notebook:

## Notebooks

### 1. Ingestion.ipynb

- **Purpose**: Handles the ingestion of data into the pipeline.
- **Key Features**:
  - Interacts with MongoDB to fetch and store data.
  - Utilizes Python libraries like `pandas` for data manipulation and `datetime` for timestamp handling.

### 2. IntialTrain.ipynb

- **Purpose**: Performs the initial training of the machine learning model.
- **Key Features**:
  - Loads data ingestion and transformation modules.
  - Configures MongoDB to store results.
  - Contains a function to generate predictions based on various input combinations (e.g., days, hours, and dishes).

### 3. Predict.ipynb

- **Purpose**: Manages real-time predictions and model updates.
- **Key Features**:
  - Includes functionality to fetch and store prediction data in MongoDB.
  - Implements a function to update the model incrementally with new data.
  - Uses an iterative approach for predictions with time-based triggers.

### 4. Transformation.ipynb

- **Purpose**: Preprocesses and transforms data to make it suitable for machine learning models.
- **Key Features**:
  - Utilizes `pandas` for data manipulation.
  - Employs `OneHotEncoder` and `StandardScaler` for encoding categorical variables and scaling numeric data, respectively.

## Setup and Installation

To run these notebooks, ensure you have the following dependencies installed:

- Python (>=3.8)
- Jupyter Notebook or Jupyter Lab
- Required Python Libraries:
  - `pandas`
  - `scikit-learn`
  - `pymongo`

You can install the dependencies using the following command:

```bash
pip install pandas scikit-learn pymongo
```

## Usage

1. **Ingest Data**: Start with `Ingestion.ipynb` to load the data into MongoDB.
2. **Transform Data**: Use `Transformation.ipynb` to preprocess the data.
3. **Train Model**: Run `IntialTrain.ipynb` to train the model on the transformed data.
4. **Make Predictions**: Use `Predict.ipynb` for real-time predictions and model updates.

## Notes

- Ensure MongoDB is properly configured and running before executing the notebooks.
- Modify the database connection string and configuration as needed in the notebooks.
- For real-time prediction tasks, `Predict.ipynb` might require periodic execution or scheduling.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## System requirements

To deploy this project run

```bash
  pip install -r requirements.txt
```

To run a specific processing file use

python -m package.module

