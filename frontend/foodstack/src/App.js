import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const App = () => {
  const [dish, setDish] = useState('Steak');
  const [data, setData] = useState([]);
  const [chartData, setChartData] = useState({});
  const [day, setDay] = useState(0);
  const [dayDishes, setDayDishes] = useState([]);

  useEffect(() => {
    // Fetch data based on selected dish
    const fetchDishData = async () => {
      try {
        const response = await axios.get(`http://localhost:3004/api/data?dish=${dish}`);
        setData(response.data);
      } catch (error) {
        console.error('Error fetching dish data:', error);
      }
    };
    fetchDishData();
  }, [dish]);

  useEffect(() => {
    // Transform data into chart format
    if (data.length > 0) {
      const days = Array.from(new Set(data.map((item) => item.Day)));
      const amounts = days.map((day) => {
        return data.filter((item) => item.Day === day).map((item) => item['Predicted Amount']);
      });

      setChartData({
        labels: days.map((day) => `Day ${day}`),
        datasets: [
          {
            label: `Predicted Amounts for ${dish}`,
            data: amounts.flat(),
            borderColor: 'rgb(75, 192, 192)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            fill: true,
          },
        ],
      });
    }
  }, [data, dish]);

  useEffect(() => {
    // Fetch dishes for the selected day
    const fetchDayDishes = async () => {
      try {
        const response = await axios.get(`http://localhost:3004/api/day-data?day=${day}`);
        const sortedDishes = response.data.sort((a, b) => b['Predicted Amount'] - a['Predicted Amount']);
        setDayDishes(sortedDishes);
      } catch (error) {
        console.error('Error fetching day dishes:', error);
      }
    };
    fetchDayDishes();
  }, [day]);

  return (
    <div className="App" style={{ fontFamily: 'Arial, sans-serif', padding: '20px', maxWidth: '900px', margin: 'auto' }}>
      <h1 style={{ textAlign: 'center', marginBottom: '30px' }}>Dish Prediction Dashboard</h1>

      {/* Dish Selector and Chart */}
      <div style={{ display: 'flex', gap: '20px', marginBottom: '40px' }}>
        {/* Dish Selector */}
        <div
          style={{
            flex: 1,
            padding: '20px',
            border: '1px solid #ccc',
            borderRadius: '10px',
            boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
          }}
        >
          <h2>Select a Dish</h2>
          <select
            value={dish}
            onChange={(e) => setDish(e.target.value)}
            style={{
              width: '100%',
              padding: '10px',
              border: '1px solid #ccc',
              borderRadius: '5px',
            }}
          >
            <option value="Steak">Steak</option>
            <option value="Soup">Soup</option>
            <option value="Sandwich">Sandwich</option>
            <option value="Pizza">Pizza</option>
            <option value="Salad">Salad</option>
            <option value="Sushi">Sushi</option>
            <option value="Tacos">Tacos</option>
          </select>
        </div>

        {/* Chart Card */}
        <div
          style={{
            flex: 2,
            padding: '20px',
            border: '1px solid #ccc',
            borderRadius: '10px',
            boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
          }}
        >
          <h2>Predicted Amount Chart</h2>
          {chartData.labels && chartData.labels.length > 0 ? (
            <Line data={chartData} />
          ) : (
            <p>No data available for the selected dish.</p>
          )}
        </div>
      </div>

      {/* Day Selector and Dish List */}
      <div
  style={{
    padding: '20px',
    border: '1px solid #ccc',
    borderRadius: '10px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
  }}
>
  <h2>Select a Day</h2>
  <select
    value={day}
    onChange={(e) => setDay(parseInt(e.target.value))}
    style={{
      width: '100%',
      padding: '10px',
      border: '1px solid #ccc',
      borderRadius: '5px',
      marginBottom: '20px',
    }}
  >
    <option value="0">Sunday</option>
    <option value="1">Monday</option>
    <option value="2">Tuesday</option>
    <option value="3">Wednesday</option>
    <option value="4">Thursday</option>
    <option value="5">Friday</option>
    <option value="6">Saturday</option>
  </select>

  <h3>Dishes for Day {day} (Sorted by Amount)</h3>
  <ul>
  {dayDishes.map((dishItem, index) => (
    <li key={index}>
      {dishItem.Dish}: {dishItem.HighestPredictedAmount ? dishItem.HighestPredictedAmount.toFixed(2) : 'N/A'}
    </li>
  ))}

  </ul>
</div>


    </div>
  );
};

export default App;
