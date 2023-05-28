import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# Keras libraries for datasets and CNN's model
from tensorflow.keras.datasets import mnist

# Main function for the AI part
def mainAI():
    # Load data from the mnist dataset into 2 main catergories :
    # Training data and Testing data
    # Handwritten digits dataset
    (xTrain, yTrain), (xTest, yTest) = mnist.load_data()
    # No need to clean this dataset

    # Preprocess the data
    xTrain = xTrain.reshape(-1, 28, 28, 1) / 255.0
    xTest = xTest.reshape(-1, 28, 28, 1) / 255.0
    yTrain = tf.keras.utils.to_categorical(yTrain, num_classes=10)
    yTest = tf.keras.utils.to_categorical(yTest, num_classes=10)

    # Create the CNN model
    model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)), # Input layers
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax') # Get the proba for the digits
    ])

    # Compile the model for the training and the 
    # Compile the model
    model.compile(optimizer='adam',
                loss='categorical_crossentropy', metrics=['accuracy'])

    # Train the model
    trained = model.fit(xTrain, yTrain, batch_size=32, 
                    epochs=7, validation_data=(xTest, yTest))
    
    # Get the plot from the data to show the accuracy of the model
    # Plot for the accuracy of the model
    plt.figure(figsize=(8, 6))
    plt.plot(trained.history['accuracy'], label='accuracy')
    plt.plot(trained.history['val_accuracy'], label = 'val_accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend(loc='lower right')
    plt.savefig('accuracy_graph.png')
    plt.close()

    # Plot for the loss of the model
    plt.figure(figsize=(8, 6))
    plt.plot(trained.history['loss'], label='loss')
    plt.plot(trained.history['val_loss'], label = 'val_loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend(loc='upper right')
    plt.savefig('loss_graph.png')
    plt.close()

    # Calculates the accuracy of the model on the dataset
    test_loss, test_acc = model.evaluate(xTest,  yTest, verbose=2)
    
    # Save the parameters only if the accuracy is greater than 98.6%
    if(test_acc * 100 > 98.6):
        model.save('model.h5')
    print(test_acc)

mainAI()