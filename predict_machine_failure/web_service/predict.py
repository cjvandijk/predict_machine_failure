import mlflow
import pickle
from mlflow.tracking import MlflowClient
from flask import Flask, request, jsonify

RUN_ID = "7c0cdf34f53042a4b24293fb27241767"   # os.getenv('RUN_ID')
MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"
MODEL_LOC = "../model/lin_reg.bin"

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)

# path = client.download_artifacts(run_id=RUN_ID, path='dict_vectorizer.bin')
logged_model = f"s3://claudia-mlops/1/{RUN_ID}/artifacts/model"

model = mlflow.pyfunc.load_model(logged_model)


# logged_model = f"s3://claudia-mlops/1/{RUN_ID}/artifacts/model"

# client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)
# path = client.download_artifacts(run_id=RUN_ID, path='dict_vectorizer.bin')
# lm = mlflow-artifacts:/1/7c0cdf34f53042a4b24293fb27241767/artifacts/model
# logged_model = f'runs:/{RUN_ID}/model'
# model = mlflow.pyfunc.load_model(logged_model)

with open(MODEL_LOC, 'rb') as f_in:
    (dv, model) = pickle.load(f_in)


def predict(features):
    X = dv.transform(features)
    preds = model.predict(X)
    return preds[0]


app = Flask('predict-machine-failure')


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    print("GETTING MACHINE_READINGS")
    machine_readings = request.get_json()

    pred = predict(machine_readings)

    result = {
        'failure_likelihood': pred,
        # 'model_version': RUN_ID
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
