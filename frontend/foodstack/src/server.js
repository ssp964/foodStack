const express = require('express');
const cors = require('cors');
const { MongoClient } = require('mongodb'); // MongoDB client for direct access

const app = express();
app.use(cors());
app.use(express.json());

// MongoDB URI
const MONGO_URI = "mongodb+srv://omkar:admin@cluster1.l7x2q.mongodb.net/foodstack?retryWrites=true&w=majority&appName=cluster1";

// Create a MongoDB client
const client = new MongoClient(MONGO_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

// Ensure the MongoDB connection is established when the app starts
client.connect()
  .then(() => console.log('Connected to MongoDB'))
  .catch((err) => console.error('Error connecting to MongoDB:', err));

// API endpoint to fetch data by dish
app.get('/api/data', async (req, res) => {
  const { dish } = req.query;

  try {
    const db = client.db('foodstack');
    const collection = db.collection('predicted_data');

    console.log('Querying for dish:', dish);

    const data = await collection.find({ Dish: dish }).sort({ Day: 1, Hour: 1 }).toArray();

    console.log('Data fetched:', data);

    res.json(data);
  } catch (err) {
    console.error('Error fetching data:', err);
    res.status(500).send('Internal server error');
  }
});

// API endpoint to list all dishes for a specific day with highest predicted amount
app.get('/api/day-data', async (req, res) => {
  const { day } = req.query;

  if (!day) {
    return res.status(400).send('Day query parameter is required');
  }

  try {
    const db = client.db('foodstack');
    const collection = db.collection('predicted_data');

    // Aggregation pipeline to group by dish and get the highest predicted amount
    const data = await collection.aggregate([
      { $match: { Day: parseInt(day) } }, // Filter by day
      {
        $group: {
          _id: "$Dish", // Group by dish name
          highestPredictedAmount: { $max: "$Predicted Amount" }, // Get the max predicted amount
        }
      },
      { $sort: { highestPredictedAmount: -1 } }, // Sort by highest predicted amount in descending order
    ]).toArray();

    console.log('Dishes for Day:', day);
    console.log('Sorted Data:', data);

    // Format the result
    const formattedData = data.map(item => ({
      Dish: item._id,
      HighestPredictedAmount: item.highestPredictedAmount
    }));

    res.json(formattedData);
  } catch (err) {
    console.error('Error fetching day data:', err);
    res.status(500).send('Internal server error');
  }
});

// Start the server
app.listen(3004, () => console.log('Server running on port 3004'));
