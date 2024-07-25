FROM mageai/mageai:latest

ARG PROJECT_NAME=predict_machine_failure
ARG MAGE_CODE_PATH=/home/src
ARG USER_CODE_PATH=${MAGE_CODE_PATH}/${PROJECT_NAME}

COPY requirements.txt ${USER_CODE_PATH}/requirements.txt 

RUN pip3 install -r ${USER_CODE_PATH}/requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:${MAGE_CODE_PATH}/${PROJECT_NAME}:/usr/local/lib/python3.10/site-packages"
# Database
ENV POSTGRES_HOST=magic-database
ENV POSTGRES_DB=magic
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_USER=postgres
ENV MAGE_DATABASE_CONNECTION_URL="postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:5432/${POSTGRES_DB}"

WORKDIR ${MAGE_CODE_PATH}

COPY ${PROJECT_NAME} ${PROJECT_NAME} 
