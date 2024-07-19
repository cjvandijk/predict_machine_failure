import mlflow
from mlflow.tracking import MlflowClient
from flask import Flask, request, jsonify


RUN_ID = "7c0cdf34f53042a4b24293fb27241767"   # os.getenv('RUN_ID')
MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"

# mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
# logged_model = f"s3://claudia-mlops/1/{RUN_ID}/artifacts/model"

client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)
path = client.download_artifacts(run_id=RUN_ID, path='dict_vectorizer.bin')
logged_model = f'runs:/{RUN_ID}/model'
model = mlflow.pyfunc.load_model(logged_model)


def predict(features):
    preds = model.predict(features)
    return preds[0]


app = Flask('predict-machine-failure')


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    machine_readings = request.get_json()

    pred = predict(machine_readings)

    result = {
        'duration': pred,
        'model_version': RUN_ID
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
