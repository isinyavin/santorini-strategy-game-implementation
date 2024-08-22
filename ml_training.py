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
    encoding = {"A": 0, "B": 1, "Y": 2, "Z": 3}
    return encoding.get(worker, -1)  # Default to -1 if the worker is not recognized

def encode_direction(direction):
    """Encodes a direction as a numerical feature."""
    encoding = {"n": 0, "ne": 1, "e": 2, "se": 3, "s": 4, "sw": 5, "w": 6, "nw": 7}
    return encoding.get(direction, -1)  # Default to -1 if the direction is not recognized


def extract_features(row):
    """Extract features from the game state."""
    board_state = eval(row["board_state"])
    available_moves = eval(row["available_moves"])
    chosen_move = eval(row["chosen_move"])

    board_features = []
    for board_row in board_state:
        for square in board_row:
            board_features.append(square["level"])
            # Encode each worker type distinctly
            board_features.append(encode_worker(square["worker"]))
    
    # Encode the chosen move (e.g., "Z,s,ne")
    worker = chosen_move[0]
    move_direction = chosen_move[1]
    build_direction = chosen_move[2]

    move_features = [
        encode_worker(worker),  # Encode the worker involved in the move
        encode_direction(move_direction),
        encode_direction(build_direction)
    ]

    # Combine board features and chosen move features
    features = board_features + move_features
    
    return np.array(features)

def preprocess_data(df):
    """Preprocesses the data for training the model."""
    X, y = [], []

    for _, row in df.iterrows():
        features = extract_features(row)
        winner = row["winner"]

        # Determine the label (1 for good move, 0 for bad move)
        label = 1 if row["player_to_move"] == winner else 0

        X.append(features)
        y.append(label)
    
    return np.array(X), np.array(y)

if __name__ == "__main__":
    check_for_gpu()

    df = pd.read_csv("raw_santorini_games.csv")
    X, y = preprocess_data(df)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = Sequential([
        Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
        Dropout(0.2),
        Dense(64, activation='relu'),
        Dense(1, activation='sigmoid')  # Output layer for binary classification (good/bad move)
    ])

    # Compile the model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Train the model with verbose output (detailed for each epoch)
    model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test), verbose=1)

    # Evaluate the model
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"Test Accuracy: {accuracy:.2f}")

    # Save the trained model
    model.save("santorini_move_predictor.h5")
