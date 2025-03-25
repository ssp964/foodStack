import pandas as pd
from datetime import datetime, timedelta
import random
from utils.server import PostgresConnector

# Initialize the database connector
db = PostgresConnector()

# Define dishes
dishes = [
    "Pizza",
    "Burger",
    "Pasta",
    "Sushi",
    "Salad",
    "Tacos",
    "Steak",
    "Curry",
    "Sandwich",
    "Noodles",
]

# Generate dummy data for the past 7 days
data = []
today = datetime.today()

for i in range(7):
    date = today - timedelta(days=i)
    day_of_week = date.strftime("%A")

    for dish in dishes:
        hour = random.randint(11, 21)
        quantity = random.randint(20, 50)
        price = random.randint(6, 20)

        data.append(
            {
                "date": date.replace(hour=hour, minute=0, second=0, microsecond=0),
                "day_of_week": day_of_week,
                "hour": hour,
                "dish": dish,
                "quantity": quantity,
                "price": price,
            }
        )

# Convert to DataFrame
df = pd.DataFrame(data)

# Insert into PostgreSQL
db.insert_dataframe("actual_data", df)

print("✅ Dummy data inserted into dactual_data.")
