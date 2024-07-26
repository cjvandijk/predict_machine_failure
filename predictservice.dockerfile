FROM python:3.10-slim

ARG PROJECT_NAME=predict_machine_failure
ARG MAGE_CODE_PATH=/home/src
ARG USER_CODE_PATH=${MAGE_CODE_PATH}/${PROJECT_NAME}

COPY requirements.txt ${USER_CODE_PATH}/requirements.txt 

RUN pip3 install -r ${USER_CODE_PATH}/requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:${MAGE_CODE_PATH}/${PROJECT_NAME}:/usr/local/lib/python3.10/site-packages"

# WORKDIR ${MAGE_CODE_PATH}

# COPY ${PROJECT_NAME} ${PROJECT_NAME} 

WORKDIR /app

COPY [ "${PROJECT_NAME}/web_service/predict.py", "/models/lin_reg.bin", "./" ]

ENV MODELS_LOC="lin_reg.bin"

EXPOSE 9696

ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9696", "predict:app" ]

# gunicorn --bind=0.0.0.0:9696 predict:app