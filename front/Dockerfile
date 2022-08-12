FROM node:18-alpine

COPY .. /front/package.json /testy/front/
COPY .. /front/package-lock.json /testy/front/

WORKDIR /testy/front

RUN npm install

COPY ../front /testy/front

EXPOSE 3000

CMD [ "npm", "start" ]
