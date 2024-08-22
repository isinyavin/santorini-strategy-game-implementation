import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

def check_for_gpu():
    """Check if a GPU is available and being used."""
    if tf.config.list_physical_devices('GPU'):
        print("Using GPU for training")
    else:
        print("Using CPU for training")

def encode_worker(worker):
    """Encodes the worker as a numerical feature."""
    encoding = {"A": 0, "B": 1, "Y": 2, "Z": 3, "None": 4}  
    return encoding.get(worker, 4)

def extract_features(board_state):
    """Extract features from the board state."""
    board_features = []
    for board_row in board_state:
        for square in board_row:
            board_features.append(square["level"])
            board_features.append(encode_worker(square["worker"]))

    return np.array(board_features)

def preprocess_data(df):
    """Preprocess the data for training the model."""
    X, y = [], []

    i = 0
    for _, row in df.iterrows():
        board_state = eval(row["board_state"])
        label = row["label"]

        features = extract_features(board_state)
        X.append(features)
        y.append(label)
        print(i)
        i+=1
    
    return np.array(X), np.array(y)

if __name__ == "__main__":
    check_for_gpu()

    df = pd.read_csv("board_state_data.csv")
    X, y = preprocess_data(df)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = Sequential([
        Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
        Dropout(0.2),
        Dense(64, activation='relu'),
        Dense(1, activation='sigmoid')  
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    model.fit(X_train, y_train, epochs=20, validation_data=(X_test, y_test), verbose=1)

    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"Test Accuracy: {accuracy:.2f}")

    model.save("santorini_win_predictor.h5")
