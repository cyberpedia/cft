# frontend.Dockerfile
# Stage 1: Build the Vue.js application
FROM node:20-alpine as build-stage

WORKDIR /app/frontend

# Copy package.json and package-lock.json (or yarn.lock)
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend code
COPY frontend/ .

# Build the Vue.js app for production
RUN npm run build

# Stage 2: Serve the Vue.js application with Nginx
FROM nginx:alpine

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the built Vue.js assets from the build stage
COPY --from=build-stage /app/frontend/dist /usr/share/nginx/html

# Expose port 80 for Nginx
EXPOSE 80

# Command to start Nginx
CMD ["nginx", "-g", "daemon off;"]
