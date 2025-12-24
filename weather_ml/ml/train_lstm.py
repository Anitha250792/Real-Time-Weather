import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import joblib

# Example dataset (replace with real historical data)
data = pd.read_csv("temperature_history.csv")  # date, temp

temps = data["temp"].values.reshape(-1, 1)

scaler = MinMaxScaler()
temps_scaled = scaler.fit_transform(temps)

X, y = [], []
window = 24

for i in range(len(temps_scaled) - window):
    X.append(temps_scaled[i:i+window])
    y.append(temps_scaled[i+window])

X, y = np.array(X), np.array(y)

model = Sequential([
    LSTM(64, return_sequences=True, input_shape=(window, 1)),
    LSTM(32),
    Dense(1)
])

model.compile(optimizer="adam", loss="mse")
model.fit(X, y, epochs=20, batch_size=16)

model.save("model.h5")
joblib.dump(scaler, "scaler.pkl")
