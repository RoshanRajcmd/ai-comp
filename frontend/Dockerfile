# Use a Node image to build and run the React app
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files and install dependencies
COPY package.json .
COPY package-lock.json .
RUN npm install --save-dev typescript@latest @types/react@latest @types/react-dom@latest react-icons react-router-dom --legacy-peer-deps

# Copy all application code
COPY . .

# Build the final production application (optional, for development, we run 'npm start')
# RUN npm run build

# Stage 2: Final Runtime Stage (using a smaller Node base)
FROM node:20-alpine

WORKDIR /app

# Copy dependencies and application files from the builder stage
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app .

# React development server runs on port 3000
EXPOSE 3000

# Default command to start the development server
CMD ["npm", "start"]