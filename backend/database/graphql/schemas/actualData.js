const { gql } = require('apollo-server');

const actualDataSchema = gql`
  type ActualData {
    id: ID!
    date: String!
    day_of_week: String!
    hour: Int!
    dish: String!
    quantity: Int!
    price: Int!
  }

  type Query {
    getActualData: [ActualData]
  }

  type Mutation {
    addActualData(
      date: String!
      day_of_week: String!
      hour: Int!
      dish: String!
      quantity: Int!
      price: Int!
    ): ActualData
  }
`;

module.exports = actualDataSchema;
