#!/bin/bash

echo "Stopping database docker container ..."
docker stop /pg_test_container

echo "Removing database docker container ..."
docker rm /pg_test_container

echo "Removing database docker image ..."
docker image rm /pg_container

echo "Removing virtual environment ..."
rm -rf env

echo "Removing tox environment ..."
rm -rf .tox

echo "Removing logs ..."
find . -type f -name '*.log' -delete
