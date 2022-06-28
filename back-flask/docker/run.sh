#!/bin/sh
docker container stop back-flask
docker container rm back-flask
docker run \
        --network weddingshow \
        -p 5000:5000 \
        -v /robson/weddingshow/back-flask/app/run.py:/weddingshow/run.py \
        -v /robson/weddingshow/back-flask/app/config.py:/weddingshow/config.py \
        -v /robson/weddingshow/back-flask/app:/weddingshow/app \
        --restart always \
        -d -t --name back-flask back-flask
