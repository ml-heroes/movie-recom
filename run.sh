#!/bin/bash

cd client
npm install
ng build --prod
cd ..
docker-compose build
docker-compose up
