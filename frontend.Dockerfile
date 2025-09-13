# Stage 1: Build the Vue.js application
FROM node:18-alpine AS build-stage

WORKDIR /app

COPY frontend/package.json ./
COPY frontend/package-lock.json ./
RUN npm ci

COPY frontend/ ./

RUN npm run build

# Stage 2: Serve the static files with Nginx
FROM nginx:stable-alpine AS production-stage

# Copy the built assets from the build stage
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Copy the Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
