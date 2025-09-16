dockerfile
# Stage 1: Build the Vue.js application
FROM node:18-alpine AS build-stage

WORKDIR /app

# The context is now ./frontend, so paths are simpler
COPY package.json ./
COPY package-lock.json ./
RUN npm ci

# Copy the rest of the frontend source code
COPY . .

# Build the static assets
RUN npm run build

# Stage 2: Serve the static files with Nginx
FROM nginx:stable-alpine AS production-stage

# Copy the built assets from the build stage
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Copy the Nginx configuration from the local context (./frontend)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
