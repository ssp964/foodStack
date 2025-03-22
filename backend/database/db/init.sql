-- Create waiter_data table
CREATE TABLE actual_data (
    id SERIAL PRIMARY KEY,
    date TIMESTAMP NOT NULL,
    day_of_week VARCHAR(10) NOT NULL,
    hour INTEGER NOT NULL,
    dish VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL,
    price INTEGER NOT NULL
);

-- Create predicted_data table
CREATE TABLE predicted_data (
    id SERIAL PRIMARY KEY,
    day_of_week VARCHAR(10) NOT NULL,
    hour INTEGER NOT NULL,
    dish VARCHAR(100) NOT NULL,
    predicted_quantity INTEGER NOT NULL,
    price INTEGER NOT NULL,
    prediction_time TIMESTAMP DEFAULT NOW()
);
