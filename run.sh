#!/bin/bash

cd client
yarn build
cd ..
# docker-compose build
docker-compose up
