import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense, Dropout
from tensorflow.keras.layers import Conv2D, Flatten, Dense, Dropout, BatchNormalization, MaxPooling2D

def check_for_gpu():
    """Check if a GPU is available and being used."""
    if tf.config.list_physical_devices('GPU'):
        print("Using GPU for training")
    else:
        print("Using CPU for training")

def encode_board_state(board_state):
    """Encodes the board state as a 5x5x2 tensor for CNN input."""
    board_tensor = np.zeros((5, 5, 2))  

    for i, row in enumerate(board_state):
        for j, square in enumerate(row):
            level = square["level"]
            board_tensor[i, j, 0] = level
            
            worker = square["worker"]
            if worker in ["A", "B"]:  
                board_tensor[i, j, 1] = 1
            elif worker in ["Y", "Z"]:  
                board_tensor[i, j, 1] = -1 
    #print(board_tensor)
    return board_tensor

def preprocess_data(df):
    """Preprocess the data for training the model."""
    X, y = [], []

    i = 0
    for _, row in df.iterrows():
        board_state = eval(row["board_state"])
        label = row["label"]

        features = encode_board_state(board_state)
        X.append(features)
        if label == 100: label = 1000
        if label == -100: label = -1000
        y.append(label)
        
        if i % 100 == 0:
            print(i)

        i +=1

    return np.array(X), np.array(y)

if __name__ == "__main__":
    check_for_gpu()

    try:
        X = np.load("X_data_10k.npy")
        y = np.load("y_data_10k.npy")
        print("Loaded preprocessed data.")
    except FileNotFoundError:
        # If not found, preprocess the data and save it
        print("Preprocessed data not found, processing now...")
        df = pd.read_csv("board_state_data_1k.csv")
        X, y = preprocess_data(df)
        np.save("X_data_10k.npy", X)
        np.save("y_data_10k.npy", y)
        print("Data preprocessed and saved.")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

    #model = Sequential([
     #   Conv2D(64, (3, 3), activation='relu', input_shape=(5, 5, 5)), 
      #  BatchNormalization(),
      #  Dropout(0.3),

       # Conv2D(128, (3, 3), activation='relu'),  
       # BatchNormalization(),
       # Dropout(0.3),

      #  Flatten(),
      #  Dense(256, activation='relu'),
      #  Dropout(0.4),
      #  Dense(128, activation='relu'),
      #  Dropout(0.4),
       # Dense(1, activation='sigmoid')  
   # ])

    #model = Sequential([
       # Conv2D(32, (3, 3), activation='relu', input_shape=(5, 5, 5)),  
       # Conv2D(64, (3, 3), activation='relu'),
       # Flatten(),
       # Dense(128, activation='relu'),
       # Dropout(0.3),
       # Dense(64, activation='relu'),
       # Dense(1, activation='sigmoid')  
    #])

    model = Sequential([
        Conv2D(128, (3, 3), activation='relu', input_shape=(5, 5, 2)),  # First layer with 4x4 filter
        Conv2D(256, (2, 2), activation='relu'),  # Second layer with 3x3 filter
        Flatten(),
        Dense(512, activation='relu'),
        Dense(256, activation='relu'),
        Dense(1, activation='linear')  # Output layer for regression (predicting a continuous value)
    ])

    model.compile(optimizer='adam', loss='mse', metrics=['mae'])

    #checkpoint = ModelCheckpoint(
    #    "santorini_cnn_win_predictor_epoch_{epoch:02d}.h5",  # Save with epoch number in the filename
     #   save_weights_only=False,  # Save the entire model
     #   save_freq='epoch'  # Save at the end of every epoch
    #)

    model.fit(X_train, y_train, epochs=5, validation_data=(X_test, y_test), verbose=1)

    loss, mae = model.evaluate(X_test, y_test)
    print(f"Test MAE: {mae:.2f}")
    model.save("santorini_cnn_win_predictor_varied_denser.h5")
