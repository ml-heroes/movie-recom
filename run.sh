#!/bin/bash

cd client
npm install
yarn build
cd ..
docker-compose build
docker-compose up
