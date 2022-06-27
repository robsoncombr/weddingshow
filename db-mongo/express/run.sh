#!/bin/sh
#
# https://hub.docker.com/_/mongo-express
#
docker container stop weddingshow-mongo-express
docker container rm weddingshow-mongo-express
docker run \
        --network weddingshow \
        --name weddingshow-mongo-express \
        -p 8081:8081 \
        -e ME_CONFIG_MONGODB_ENABLE_ADMIN=true \
        -e ME_CONFIG_MONGODB_URL='mongodb://weddingshow-mongo5:27017' \
        --restart always \
        -d mongo-express:latest
