#!/usr/bin/env bash

cd "../../$(dirname "$0")"

pipenv run python tests/integration_tests/test_s3.py

pipenv run python tests/integration_tests/test_prediction_service.py

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker-compose logs
fi

exit ${ERROR_CODE}
