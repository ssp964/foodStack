const { Pool } = require('pg');
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

module.exports = {
  Query: {
    async getActualData() {
      const res = await pool.query('SELECT * FROM actual_data');
      return res.rows;
    },
  },
  Mutation: {
    async addActualData(_, { date, day_of_week, hour, dish, quantity, price }) {
      const res = await pool.query(
        'INSERT INTO actual_data (date, day_of_week, hour, dish, quantity, price) VALUES ($1, $2, $3, $4, $5, $6) RETURNING *',
        [date, day_of_week, hour, dish, quantity, price]
      );
      return res.rows[0];
    },
  },
};
