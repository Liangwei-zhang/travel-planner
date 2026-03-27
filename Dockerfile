# Travel Planner Bot - Dockerfile

FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --production

# Copy source files
COPY . .

# Create data directory if not exists
RUN mkdir -p data

# Expose port (if needed)
EXPOSE 3000

# Run the bot
CMD ["node", "src/bot.js"]