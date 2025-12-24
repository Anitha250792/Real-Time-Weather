import numpy as np
import joblib
from tensorflow.keras.models import load_model

model = load_model("ml/model.h5")
scaler = joblib.load("ml/scaler.pkl")

def predict_next_24_hours(last_24_temps):
    scaled = scaler.transform(np.array(last_24_temps).reshape(-1, 1))
    X = scaled.reshape(1, 24, 1)

    preds = []
    for _ in range(24):
        next_temp = model.predict(X, verbose=0)[0][0]
        preds.append(next_temp)
        X = np.append(X[:, 1:, :], [[[next_temp]]], axis=1)

    return scaler.inverse_transform(
        np.array(preds).reshape(-1, 1)
    ).flatten().round(1).tolist()
