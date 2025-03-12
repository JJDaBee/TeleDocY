# Use an official Node.js image
FROM node:18

# Set working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy all files to container
COPY . .

# Expose API Gateway port
EXPOSE 4000

# Start the API Gateway
CMD ["node", "index.js"]
