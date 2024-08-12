FROM mageai/mageai:latest

ARG PROJECT_NAME=predict_machine_failure
ARG MAGE_CODE_PATH=/home/src
ARG USER_CODE_PATH=${MAGE_CODE_PATH}/${PROJECT_NAME}

COPY requirements-partial.txt requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:${MAGE_CODE_PATH}/magic_context/${PROJECT_NAME}:/usr/local/lib/python3.10/site-packages"

WORKDIR ${PROJECT_NAME}

COPY ./ ./
