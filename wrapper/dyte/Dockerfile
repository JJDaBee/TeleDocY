# Use official Node.js image
FROM node:18

# Set working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the code
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Run the app
# CMD ["node", "index.js"]
# CMD ["npm", "start"]
CMD ["npm", "run", "dev"]

