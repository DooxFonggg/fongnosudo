FROM node:20-alpine as build
WORKDIR /app
COPY . .
RUN npm install 
RUN npm run build

## run stage ##
FROM nginx:alpine
COPY --from=build /app/dist /run
COPY nginx.conf /etc/nginx/nginx.conf