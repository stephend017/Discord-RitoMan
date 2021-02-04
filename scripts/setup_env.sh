#!/bin/bash
# TODO remove upon verification it is no longer needed
# docker build -t pg_container .

ret=$?
build_count=0

while [ $build_count -lt 3 ];
do
    echo "Started build docker image ..."
    docker build -t pg_container .
    if [ $ret -ne 0 ]; then
        if [$build_count -eq 3]; then
            echo "Exceeded max number of build attempts"
            echo "Cleaning docker containers and images ..."
            docker stop /pg_test_container
            docker rm /pg_test_container
            docker image rm /pg_container
            echo "Exiting setup environment script ..."
            exit 1
        fi

        echo "Failed to create image"
        echo "Retrying to build image ..."
        build_count=$build_count + 1
    else
        build_count=3
    fi
done

echo "Successfully built docker image"
echo "Started running docker container ..."
docker run -P --name pg_test_container pg_container &

echo "Building python virtual environment ..."
python3.8 -m venv env

echo "Installing project requirements ..."
env/bin/python3.8 -m pip install -r requirements.txt
env/bin/python3.8 -m pip install -r requirements-dev.txt
env/bin/python3.8 -m pip install .
