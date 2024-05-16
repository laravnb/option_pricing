import numpy as np
import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from sklearn.preprocessing import MinMaxScaler
from keras.metrics import MeanAbsolutePercentageError

# Function to scale input and output
def scale_data(x_train, x_test, y_train, y_test, input_scaler=None, output_scaler=None):
    if input_scaler:
        x_train = input_scaler.fit_transform(x_train)
        x_test = input_scaler.transform(x_test)
    if output_scaler:        
         # reshape 1d arrays to 2d arrays
        y_train = y_train.values.reshape(len(y_train), 1)
        y_test = y_test.values.reshape(len(y_test), 1)
        # fit scaler on training dataset
        # transform training dataset
        y_train = output_scaler.fit_transform(y_train)
        # transform test dataset
        y_test = output_scaler.transform(y_test)
    return x_train, x_test, y_train, y_test

# Function to invert scaling
def invert_scaling(data, scaler):
    if scaler:
        inverted_data = scaler.inverse_transform(data.reshape(-1, 1)).flatten()
    return inverted_data

# setting the seed for reproducibility
np.random.seed(19)
tf.random.set_seed(19)

# Import the input data
# Assumes file named "Input_c.csv" exists with Monte Carlo, Trinomial Tree, Finite Difference and Option Market price exists
data = pd.read_csv('Input_c.csv')

# Extract features and target variable
x = data[['Monte Carlo Price', 'Trinomial Tree Price', 'Finite Difference Price']]
y = data['Market Price']

# split data into training and testing
X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Initialize MinMaxScaler objects for input and output
input_scaler = MinMaxScaler()
output_scaler = MinMaxScaler()

# Scale data
x_train, x_test, y_train, y_test = scale_data(X_train, X_test, Y_train, Y_test, input_scaler, output_scaler)

# Multilayer perceptron model for regression
# Add 1 hidden layer with 2 neurons, sigmoid activation function, fully connected
nn_model = Sequential()
nn_model.add(Dense(2, input_dim=3, activation='sigmoid'))
nn_model.add(Dense(1, activation='linear'))
nn_model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mae', MeanAbsolutePercentageError()])

# Train the model
history = nn_model.fit(x_train, y_train, epochs=150, batch_size=16, validation_data=(x_test, y_test))

# Evaluate the model
train_mse, train_mae, train_mape = nn_model.evaluate(x_train, y_train)
test_mse, test_mae, test_mape = nn_model.evaluate(x_test, y_test)
# print("MSE, MAE, MAPE on training data:", train_mse, train_mae, train_mape)
# print("MSE, MAE, MAPE on test data:", test_mse, test_mae, test_mape)

# predict the NN option price
Y_pred = nn_model.predict(x_test)

# Invert scaling for predicted output
Y_pred = invert_scaling(Y_pred, output_scaler)
# print(Y_pred)

# Convert y_test.index to a pandas Index object
index = pd.Index(Y_test.index)

# Create a pandas Series with Y_pred and the converted index
# Add the Series to the DataFrame
C_nn = pd.Series(Y_pred, index=index)
data['NN Price'] = C_nn

# Remove empty rows
data = data.dropna()

# Save the dataset to a csv file
data.to_csv('NN_c.csv', index=False)

#plot the training and test loss
plt.plot(history.history['loss'], label='Train')
plt.plot(history.history['val_loss'], label='Test')
plt.title('Train vs Test MSE of NN')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(loc='upper right')
plt.show()

# Save the model with json
# model_json = nn_model.to_json()
# with open("Models/nn_architecture.json", "w") as json_file:
#     json_file.write(model_json)

# Save the weights
# nn_model.save_weights("Models/nn_weights.h5")
# print("Model saved ")


# from keras.models import model_from_json
# Load the model
# json_file = open('Models/nn_architecture.json', 'r')
# loaded_model_json = json_file.read()
# json_file.close()
# loaded_model = model_from_json(loaded_model_json)
# # Load weights into new model
# loaded_model.load_weights("Models/nn_weights.h5")
# print("Model loaded")
