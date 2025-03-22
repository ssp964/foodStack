# Use Node.js image
FROM node:18

# Create app directory
WORKDIR /app

# Copy package files
COPY package.json ./

# Install dependencies
RUN npm install

# Copy the entire backend code
COPY . .

# Expose port
EXPOSE 4000

# Start the server
CMD ["node", "index.js"]
