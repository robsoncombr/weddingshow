#!/bin/sh
#
# https://hub.docker.com/_/mongo
#
docker container stop weddingshow-mongo5
docker container rm weddingshow-mongo5
docker run \
        --network weddingshow \
        --name weddingshow-mongo5 \
        -v /robson/weddingshow/db-mongo/data:/data/db \
        -v /robson/weddingshow/db-mongo/dump:/dump \
        -e wiredTigerCacheSizeGB=1.5 \
        --restart always \
        -d mongo:latest mongod