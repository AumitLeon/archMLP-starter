import logging
import dill
import pandas as pd
from flask import Flask, request
from werkzeug.exceptions import BadRequest

application = Flask(__name__)

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s [%(levelname)s] %(message)s", level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S")

# Load the model 
def build_model(model_path):
    with open(model_path, "rb") as f:
        mdl = dill.load(f)
    return mdl

# Produce a prediction
def predict(mdl, request):
    try:
        features_as_dict = request.get_json()
        print(features_as_dict)
        features_as_df = pd.io.json.json_normalize(features_as_dict)

        #logger.info("Predicting {}".format(features_as_df))
        print("Predict using the following features")
        print(features_as_dict)
        print("Preparing to predict")
        binary_predictions = mdl.predict(features_as_df)

        prediction = str(binary_predictions[0]) + '\n'
        print("Model predicts: " + prediction)
        #logger.info("Predicted {}".format(prediction))
    except Exception as e:
        logger.exception("Error in pipeline")
        raise BadRequest(description=getattr(e, 'message', repr(e)))

    return prediction


@application.route("/predict", methods=["POST"])
def handle_predict_request():
    global model
    return predict(model, request)


if __name__ == "__main__":
    try:
        model = build_model("mod.pk")
        application.run(host='0.0.0.0')
    except KeyboardInterrupt:
        logger.exception("Shutting down")
    except Exception:
        logger.exception("Error in initialization chain")
