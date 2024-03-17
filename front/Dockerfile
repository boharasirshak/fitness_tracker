# front/Dockerfile
FROM node:18 AS build

WORKDIR /app

COPY front/package*.json ./
RUN npm install

COPY . .

ARG VITE_BACKEND_URL
RUN echo "VITE_BACKEND_URL=${VITE_BACKEND_URL}" > .env

RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
