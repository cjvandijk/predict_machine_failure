FROM mageai/mageai:alpha

RUN pip3 install mlflow==2.12.1

ARG PROJECT_NAME=predict_machine_failure
ARG MAGE_CODE_PATH=/home/src
ARG USER_CODE_PATH=${MAGE_CODE_PATH}/${PROJECT_NAME}
# RUN pip3 install -r ${USER_CODE_PATH}/requirements.txt

COPY requirements.txt ${MAGE_CODE_PATH}/requirements.txt

WORKDIR ${MAGE_CODE_PATH}

ENV USER_CODE_PATH=${USER_CODE_PATH}

RUN pip3 install -r requirements.txt
# RUN pip3 install -r ${USER_CODE_PATH}/requirements.txt
# RUN pip install mlflow==2.12.1

ENV USER_CODE_PATH=${USER_CODE_PATH}
ENV PYTHONPATH="${PYTHONPATH}:${MAGE_CODE_PATH}/${PROJECT_NAME}"
ENV PYTHONPATH="${PYTHONPATH}:/usr/local/lib/python3.10/site-packages"

COPY ${PROJECT_NAME} ${PROJECT_NAME}

CMD ["/bin/sh", "-c", "/app/run_app.sh"]
