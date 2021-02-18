#!/bin/bash
CONNECTION_INFO=$(docker port pg_test_container)
echo "connection on port " "$CONNECTION_INFO"
PORT=$(echo "$CONNECTION_INFO" | cut -d':' -f 2)
echo "$PORT"
env/bin/python3.8 -m tox -- "$PORT"
