const { mergeTypeDefs } = require('@graphql-tools/merge');
const actualDataSchema = require('./actualData');
const predictedDataSchema = require('./predictedData');

const typeDefs = mergeTypeDefs([actualDataSchema, predictedDataSchema]);

module.exports = typeDefs;
