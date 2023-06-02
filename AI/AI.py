import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import mnist

def main_ai():
    """Create and save a CNN model"""
    # Load data from the mnist dataset into 2 main catergories :
    # Training data and Testing data
    # Handwritten digits dataset
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    # No need to clean this dataset
    
    # Preprocess the data
    input_shape = (28, 28, 1)

    # Normalization and reshaping
    x_train=x_train.reshape(x_train.shape[0], x_train.shape[1], x_train.shape[2], 1)
    x_train=x_train / 255.0
    x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], x_test.shape[2], 1)
    x_test=x_test/255.0

    # Encode labels
    y_train = tf.one_hot(y_train.astype(np.int32), depth=10)
    y_test = tf.one_hot(y_test.astype(np.int32), depth=10)

    batch_size = 64
    num_classes = 10
    epochs = 6

    # Stop if we have a good accuracy
    class myCallback(tf.keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs={}):
            if(logs.get('accuracy')>0.9965):
                self.model.stop_training = True

    callbacks = myCallback()

    # Create the CNN model
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, (5,5), padding='same', activation='relu', input_shape=input_shape),
        tf.keras.layers.Conv2D(32, (5,5), padding='same', activation='relu'),
        tf.keras.layers.MaxPool2D(),
        tf.keras.layers.Dropout(0.25),
        tf.keras.layers.Conv2D(64, (3,3), padding='same', activation='relu'),
        tf.keras.layers.Conv2D(64, (3,3), padding='same', activation='relu'),
        tf.keras.layers.MaxPool2D(strides=(2,2)),
        tf.keras.layers.Dropout(0.25),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])

    model.compile(optimizer='adam',
    loss='categorical_crossentropy', metrics=['accuracy'])
    
    # Train the model
    trained = model.fit(x_train, y_train,
    batch_size=batch_size,
    epochs=epochs,
    validation_data=(x_test, y_test),
    callbacks=[callbacks])
    
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
    test_loss, test_acc = model.evaluate(x_test, y_test)
    
    # Save the parameters of the model
    model.save('model.h5')

# To get the 
main_ai()