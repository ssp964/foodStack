const { ApolloServer } = require('apollo-server');
const { Pool } = require('pg');
const typeDefs = require('./graphql/schemas');
const resolvers = require('./graphql/resolvers');
require('dotenv').config();

const pool = new Pool({
  connectionString: process.env.DATABASE_URL
});

const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: () => ({
    db: pool
  })
});

server.listen().then(({ url }) => {
  console.log(`🚀 Server ready at ${url}`);
});
