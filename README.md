# Predicting Machine Failure from Sensor Data

## Problem Description
Can we predict ahead of time whether a machine will fail based on its sensor data? If we could feed the machine's sensor data to a prediction webservice, we may be able to prevent failure, or prepare for machine failure ahead of the actual failure.

## Dataset Overview

<details>
<summary><i><b>High Level Data Overview</b> (click to expand)</i></summary>
Kaggle contains a dataset for [Machine Failure Prediction Using Sensor Data](https://www.kaggle.com/datasets/umerrtx/machine-failure-prediction-using-sensor-data?resource=download)
<br><br>
The data in that dataset was collected from the sensors on various machines. Each observation contains the data in Columns Description (below), along with whether there was an associated machine failure. The aim of this project is to produce and deploy a Linear Regression model with this data, which can then be used to predict machine failure in advance.
</details><br>

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
<summary><b><i>Project Focus</i></b></summary>

The emphasis on this project is not on producing the best model possible. I focused instead on implementing the MLOps steps required to:
- ingest and transform data with Mage AI
- split and encode the dataset in Mage
- train a model in Mage AI, while
    - tracking model training experiments in Mage/MLFlow
    - registering the model in Mage/MLFlow
- save the model as a pickle binary
- deploy the model as a web service using Flask/gunicorn
- monitor the model using Evidently (not yet implemented)
- test the webservice with Python's requests module

</details><br>

<details>
<summary><b><i>Initial exploratory data analysis</i></b></summary>

See `notebooks/1.0-cvd-machine-failure-eda.ipynb`
</details><br>

<details>
<summary><b><i>Additional Technical Overview</i></b></summary>

Training and deployment code is Dockerized. Docker Compose uses three separate docker images to spin up separate containers for Mage, MLFlow, and the Web Service, exposing all ports on host machine.

This dockerized project can be run on your host machine or the steps for running it (below) can be done on cloud, e.g. AWS EC2.

Python test files are included which can be used to check the model prediction using two separate observations
- test_fail.py will predict machine failure 
- test_no_fail.py will predict no failure.

</details>

## Running the Project

### Spin up the containers

1. Docker must be installed and the daemon running on the host or cloud machine.
1. Fork or clone this repository into your local machine or into a cloud virtual machine, such as AWS EC2. It contains data, code, docker config needed.
1. `cd` to the project folder you just created
1. `docker-compose build && docker-compose up`
1. If you are running this on the cloud, you will need to establish ssh connection your local machine and forward port 9696 to use the web service, and if you want to view the Mage and MLFlow UI, also forward ports 6789 and 5000. (this can be done via [Visual Studio Code](https://code.visualstudio.com/docs/remote/ssh))

### Test the webservice

1. Once the containers are running, open a new terminal and `cd` into the project folder.
1. You may wish to install requirements.txt or pipenv file into your system.
1. `python predict_machine_failure/web_service/test_fail.py` to see a prediction for a (very) likely failure.
1. `python predict_machine_failure/web_service/test_no_fail.py` to see a prediction for an unlikely failure.

### View the Mage and MLFlow UI

- The Mage UI will be available from your browser at http://localhost:6789

- The MLFlow UI will be available at http://localhost:5000

- Gunicorn will be serving the web service at port 9696, but there is no UI for it. It is intended to be used as part of a larger system that takes action based on the result. The result has been formatted for human view; it can be changed to its unformatted version for machine use.
