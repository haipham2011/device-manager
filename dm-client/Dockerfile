FROM node:14-alpine

WORKDIR /app

COPY ./dist /app

RUN npm install -g serve

CMD [ "serve", "-l", "8080"]