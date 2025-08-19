import cv2
import numpy as np
import os
import sys
import tensorflow as tf
from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    # Initialize the return lists
    images = []
    labels = []

    # Read through each directory in data_dir
    for category in os.listdir(data_dir):
        # Each category has various images
        for img in os.listdir(os.path.join(data_dir, category)):
            # Prevent the case in which a non-image file slipped in to a directory
            if img is not None:
                # Use cv2 to open the image as a multidimensional array. Thus creating a neural network
                img = cv2.imread(os.path.join(data_dir, category, img))
                # Resize the image so that all are the same size in the neural network
                img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
                # Store in the return data structures
                images.append(img)
                labels.append(int(category))

    # Normalize the images array so that they become pixels from 0 to 1
    images = np.array(images) / 255.0
    return images, labels


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    # Create the convolutional neural network
    model = tf.keras.models.Sequential([
        # Specify the sizing
        tf.keras.Input(shape=(IMG_WIDTH, IMG_HEIGHT, 3)),

        # First convolutional layer. Learn 32 patterns (filters) using a 3x3 kernel. Edges and outlines of the image
        tf.keras.layers.Conv2D(
            filters=32,
            kernel_size=(3, 3),
            activation="relu",
        ),
        # Max-pooling layer using a 2x2 pool size
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        # Add a second convolutional layer. Shapes like triangles and circles
        tf.keras.layers.Conv2D(
            filters=64,
            kernel_size=(3, 3),
            activation="relu",
        ),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        # Add a third convolutional layer. Information inside the shapes learnt, for instance, number inside a sign
        tf.keras.layers.Conv2D(
            filters=128,
            kernel_size=(3, 3),
            activation="relu",
        ),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        # Flatten the units
        tf.keras.layers.Flatten(),

        # We add a hidden layer with dropout to avoid overfitting. Use ReLu for hidden layers (extract info)
        tf.keras.layers.Dense(NUM_CATEGORIES * 4, activation="relu"),
        tf.keras.layers.Dropout(0.5),

        # Output layer with softmax so that we can turn the features learnt into probability of being a certain sign
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax"),
    ])

    # Compile the model 
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


if __name__ == "__main__":
    main()
