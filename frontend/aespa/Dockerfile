# use the official node docker file
FROM node:14-alpine AS build

# set the working directory
WORKDIR /app

# copy the package.json file to the working directory
COPY package.json .

# install dependencies
RUN npm install

# copy the rest of the files to the working directory
COPY . .

# build the app
RUN npm run build --prod

# Use nginx as a web server
FROM nginx:1.21-alpine

# Copy the Angular build artifacts to the web server directory
COPY --from=build /app/dist/aespa /usr/share/nginx/html

# expose port 3000
EXPOSE 4200

# start the app
CMD ["nginx", "-g", "daemon off;"]