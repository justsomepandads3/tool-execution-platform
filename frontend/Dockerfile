# Multi-stage build for optimal image size

# Stage 1: Build the React app
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* .

# Install dependencies
RUN npm i

# Copy source code
COPY . .

# Build the app
RUN npm run build

# Stage 2: Serve with a lightweight web server
FROM node:18-alpine

WORKDIR /app

# Install a simple HTTP server
RUN npm install -g serve

# Copy built app from builder stage
COPY --from=builder /app/dist ./dist

# Expose port
EXPOSE 5173

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:5173 || exit 1

# Serve the app
CMD ["serve", "-s", "dist", "-l", "5173"]
