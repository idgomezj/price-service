FROM node:18-slim

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and install dependencies
COPY package*.json ./
RUN npm install

# Copy the entire project directory to the container
COPY . .



# Expose the desired port (replace 3000 with the actual port used by your Vite app)
EXPOSE 4173

RUN npm run build
ENTRYPOINT  ["npm", "run", "preview"]

