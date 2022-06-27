#!/bin/sh

docker container stop weddingshow-mongo5
docker container start weddingshow-mongo5

/robson/weddingshow/db-mongo/express/restart.sh
