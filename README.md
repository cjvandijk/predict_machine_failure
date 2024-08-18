# Predicting Machine Failure from Sensor Data

## Problem Description
This project is designed to predict ahead of time whether a machine will fail based on its sensor data. By sending the machine's sensor data to a prediction webservice, we can prevent machine failure, or prepare for machine failure ahead of the actual failure.

## Dataset Overview

<details>
<summary><i><b>High Level Data Overview</b> (click to expand)</i></summary>

Kaggle contains a dataset for [Machine Failure Prediction Using Sensor Data](https://www.kaggle.com/datasets/umerrtx/machine-failure-prediction-using-sensor-data?resource=download). The data in that dataset was collected from the sensors on various machines. Each observation contains the data in Columns Description (below), along with whether there was an associated machine failure. The aim of this project is to produce and deploy a Linear Regression model with this data, which can then be used to predict machine failure in advance.<br><br>
</details>

<details>
<summary><i><b>Column Descriptions</b></i></summary>

- footfall: The number of people or objects passing by the machine.
- tempMode: The temperature mode or setting of the machine.
- AQ: Air quality index near the machine.
- USS: Ultrasonic sensor data, indicating proximity measurements.
- CS: Current sensor readings, indicating the electrical current usage of the machine.
- VOC: Volatile organic compounds level detected near the machine.
- RP: Rotational position or RPM (revolutions per minute) of the machine parts.
- IP: Input pressure to the machine.
- Temperature: The operating temperature of the machine.
- fail: Binary indicator of machine failure (1 for failure, 0 for no failure).
</details>

## Project Details

<details>
<summary><b><i>Project Components</i></b></summary>

The emphasis on this project is not on producing the best model possible. It focuses instead on implementing the MLOps steps required to:
- ingest and transform data with Mage AI
- split and encode the dataset in Mage
- train a model in Mage AI, while
    - tracking model training experiments in Mage/MLFlow
    - registering the model in Mage/MLFlow
- run hourly trigger in Mage to automatically re-train the model when data changes
- save the model as a pickle binary
- deploy the model as a web service using Flask/gunicorn
- monitor the pipeline through Mage
- integration testing
    - s3 upload using localstack
    - the prediction webservice using Python's requests module

<br><br>
</details>

<details>
<summary><b><i>Initial exploratory data analysis</i></b></summary>

See `notebooks/1.0-cvd-machine-failure-eda.ipynb`<br><br>
</details>

<details>
<summary><b><i>Additional Technical Overview</i></b></summary>

Training and deployment code is Dockerized. Docker Compose uses three separate docker images to spin up separate containers for Mage, MLFlow, and the Web Service, exposing all ports on host machine.

This dockerized project can be run on your host machine or the steps for running it (below) can be done on cloud, e.g. AWS EC2.

All code has been linted with black, flake8, and isort.

The hourly trigger for the Mage re-training pipeline only executes if data changes. Since the data from Kaggle datasets is not changing, this process has been mocked using the pull request count of an active github repository. It tracks the repo's previous pull request count and if the current count has increased, it triggers a re-training. Since the training data has not actually changed, the resulting model will be the same as the previous one. But since the pull requests are frequent in this repo, it will trigger re-training so that the process can be witnessed.
<br><br>
</details>

## Running the Project

<details>
<summary><b><i>Spin up the containers</i></b></summary>

1. Docker must be installed, and the daemon must be running on the host or cloud machine.
1. Fork or clone this repository into your local machine or into a cloud virtual machine, such as AWS EC2. It contains data, code, docker config needed.
1. `cd` to the project folder you just created, TOP LEVEL ('predict_machine_failure/'). If you run docker-compose from another folder, mlflow will create new directories and data structures for itself instead of using the existing ones.
1. `docker-compose build && docker-compose up`
1. If you are running this on the cloud, you will need to establish ssh connection your local machine and forward port 9696 to use the web service, and if you want to view the Mage and MLFlow UI, also forward ports 6789 and 5000. (this can be done via [Visual Studio Code](https://code.visualstudio.com/docs/remote/ssh))
<br><br>
</details>

<details>
<summary><b><i>View the Mage and MLFlow UI</i></b></summary>

- The Mage UI will be available from your browser at http://localhost:6789. 
    - Navigate to that address.
    - Select the pipelines button at the left.
    - Select the predict_machine_failure pipeline.
    - Select the edit pipeline button at the left.
    - Run each block in order.

- The MLFlow UI will be available at http://localhost:5000
    - The Experiments tab (top) will show the model training experiments that have been run through the Mage pipeline.
    - The Models tab will show the model versions that have been registered through the Mage training/re-training pipelines.
<br><br>
</details>

<details>
<summary><b><i>Test the webservice</i></b></summary>

Gunicorn will be serving the web service at port 9696, but there is no UI for it. It is accessed through API requests, querying the prediction service which returns a result indicating whether or not an action should be taken (due to probable machine failure). The returned JSON has been formatted for human view; it could eaily be changed to a more machine-readable format.

1. With the containers running, open a new terminal and `cd` into the `predict_machine_failure` project folder.
1. `pipenv install` to install requirements.
1. `pipenv run python tests/test_fail.py` to use an observation that will predict machine failure.
1. `pipenv run python tests/test_no_fail.py` to use an observation that will predict machine non-failure.
<br><br>
</details>

<details>
<summary><b><i>Run unit and integration tests</i></b></summary>
<br>
The docker containers must be up and running prior to running the test scripts.

When the tests are done, you may execute docker-compose down if you are finished with the services.

The tests do the following:

- use localstack to create an s3 bucket and upload the model pickle file to it. 
- print a list of buckets created on localstack:s3, and list the files in the bucket that were just created.
- runs several unit tests on the prediction-webservice predict function

<br>
Begin at the project root directory (predict_machine_failure)

```
cd predict_machine_failure
```

Build and start docker containers
```
docker-compose build --no-cache
docker-compose up --remove-orphans
```

Run unit and integration tests
```
pipenv run pytest tests/
```

Stop docker containers
```
docker-compose down
```

<br><br>
</details>