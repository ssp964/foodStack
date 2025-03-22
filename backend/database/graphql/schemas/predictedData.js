const { gql } = require('apollo-server');

const predictedDataSchema = gql`
  type PredictedData {
    id: ID!
    day_of_week: String!
    hour: Int!
    dish: String!
    predicted_quantity: Int!
    price: Int!
    prediction_time: String!
  }

  type Query {
    getPredictedData: [PredictedData]
  }

  type Mutation {
    addPredictedData(
      day_of_week: String!
      hour: Int!
      dish: String!
      predicted_quantity: Int!
      price: Int!
    ): PredictedData
  }
`;

module.exports = predictedDataSchema;
