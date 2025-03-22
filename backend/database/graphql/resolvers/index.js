const actualDataResolvers = require('./actualData');
const predictedDataResolvers = require('./predictedData');

const resolvers = {
  Query: {
    ...actualDataResolvers.Query,
    ...predictedDataResolvers.Query,
  },
  Mutation: {
    ...actualDataResolvers.Mutation,
    ...predictedDataResolvers.Mutation,
  },
};

module.exports = resolvers;
