#!/usr/bin/env bash

cd "../../$(dirname "$0")"

# Check if docker-compose is running
if ! docker-compose ps --services --filter "status=running" | grep -q .; then
    echo "Docker Compose is not running. Starting it now..."
    docker-compose up -d
else
    echo "Docker Compose is already running."
fi

sleep 1

pipenv run python tests/integration_tests/test_s3.py

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker-compose logs
fi

docker-compose down

exit ${ERROR_CODE}
