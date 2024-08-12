FROM python:3.10-slim

ARG MAGE_CODE_PATH=/home/src
ARG PROJECT_NAME=predict_machine_failure
ARG USER_CODE_PATH=${MAGE_CODE_PATH}/${PROJECT_NAME}

COPY predict_service_context/requirements.txt requirements.txt 

RUN pip install --upgrade pip && pip install -r requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:${MAGE_CODE_PATH}/${PROJECT_NAME}:/usr/local/lib/python3.10/site-packages"

WORKDIR /app

COPY [ "predict_service_context/predict.py", "models/lin_reg.bin", "./" ]

# DictVectorizer/LRmodel binary is at /app level for the web service
ENV MODELS_LOC="lin_reg.bin"

EXPOSE 9696

ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9696", "predict:app" ]
