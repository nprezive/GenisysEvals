FROM node:8.9.0-alpine

RUN apk add -q --no-cache git yarn
RUN yarn global add --silent quasar-cli@0.6.5

ADD package.json /tmp/package.json
RUN cd /tmp && yarn --silent && mkdir -p /frontend && cp -a /tmp/node_modules /frontend

WORKDIR /frontend
ADD . /frontend
# RUN quasar build

EXPOSE 8080
CMD [ "quasar", "dev" ]
