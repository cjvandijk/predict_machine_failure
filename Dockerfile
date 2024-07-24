FROM mageai/mageai:latest
# FROM mageai/mageai:alpha

ARG PROJECT_NAME=predict_machine_failure
ARG MAGE_CODE_PATH=/home/src
ARG USER_CODE_PATH=${MAGE_CODE_PATH}/${PROJECT_NAME}


# Install and use pipenv
COPY [ "Pipfile", "Pipfile.lock", "./" ]

WORKDIR ${MAGE_CODE_PATH}

RUN python -m pip install --upgrade pip 
RUN pip install pipenv --upgrade 
RUN pipenv lock 
# RUN pipenv sync && pipenv shell

# The following is equivalent to pipenv sync with the --system flag, 
# which is not available for the sync command, only the install command
#    --system flag will install packages into system python instead of virtual env
#    --ignore-pipfile will install from lock file instead, maintaining exact dependency versions
#    --deploy will keep pipenv install from attempting to re-lock
RUN pipenv install --dev --system --deploy


# RUN pip3 install -r ${USER_CODE_PATH}/requirements.txt
# COPY requirements.txt ${MAGE_CODE_PATH}/requirements.txt


ENV USER_CODE_PATH=${USER_CODE_PATH}
ENV PYTHONPATH="${PYTHONPATH}:${MAGE_CODE_PATH}/${PROJECT_NAME}"
ENV PYTHONPATH="${PYTHONPATH}:/usr/local/lib/python3.10/site-packages"

COPY ${PROJECT_NAME} ${PROJECT_NAME} 

CMD ["mage", "start", "${PROJECT_NAME}"]"
# CMD ["/bin/sh", "-c", "/app/run_app.sh"]
