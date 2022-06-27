#!/bin/sh
docker container stop back-flask
docker container rm back-flask
docker image rm back-flask
docker image build --file /robson/weddingshow/back-flask/docker/Dockerfile --tag back-flask .
