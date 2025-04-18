# -*- coding: utf-8 -*-
"""CVAE_callbacks_traitement_labels.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1IIbFnHo9iLr5cPRXpn2NzU7JYQpL3FAp
"""

import os

os.environ["KERAS_BACKEND"] = "tensorflow"

import numpy as np
import datetime
import matplotlib.pyplot as plt
import tensorflow as tf
import keras
import random
from keras import ops
from keras import Model, Input
from keras import layers, models
from keras import backend as K
from keras.callbacks import TensorBoard
from PIL import Image
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
"""
# Connexion Google Drive
from google.colab import drive
drive.mount('/content/drive')

cd drive/MyDrive/Colab Notebooks


# Load compressed data
loaded = np.load("processed_faces_50000.npz") # Check the npz filename and path
data = loaded["data"]

# Normalization
data = data.astype('float32') / 255.0
print("Data shape: ", data.shape)  # The shape should be (50000, 128, 128, 3)
"""

def build_encoder(input_shape=(128, 128, 3)):
    '''
    Parameters
    ----------
      - The image of shape (128,128,3)

    Description
    -----------
    The encoder (CNN) is structured as followed:
    1. Treatment of the image: extracting the image features
      - 2 Conv2D layers using 32 filters of size 3x3, with a stride of 1 to extract basic characteristics from each pixel of the image.
      - 1 MaxPooling layer using a filter of size 2x2, with a stride of 2 to reduce the size of feature map while preserving the most important information.
      - 2 more Conv2D layers of 64 and 128 filters, followed alternately by MaxPooling layers
      - 1 flatten layer to flatten the multidimensional data into a 1D vector.
      - 1 dense (or fully connected) layer with 512 neurons.

    2. The variational part:
      - 2 dense layers perform a linear transformation to combine the 512 values and project them into a latent_dim dimension space using weight and bias.
      - 1 layer generate the mean of the latent distribution, the other generate the log-variance
      - 1 Lambda layer is used to limit the values of log-variance in the range [-10.0, 10.0] and to prevent them from becoming too large or too small,
        which could affect model stability during training.

    Then it use the function Sampling() to create a sample from the latent distribution using the previous mean, log_variance and an additionl noise.

    Returns
    -------
    A keras Model able to encode an image of shape (128,128,3) into a latent vector of size latent_dim
    '''
    img_input = Input(shape=input_shape, name="encoder_image_input")

    x = layers.Conv2D(32, 3, activation="relu", strides=1, padding="same")(img_input)
    x = layers.Conv2D(32, 3, activation="relu", strides=1, padding="same")(x)
    x = layers.MaxPooling2D(2,2)(x) #2x2 kernel size. Test with Conv2D kernel size = 2, stride 2 and no padding
    x = layers.Conv2D(64, 3, activation="relu", strides=1, padding="same")(x)
    x = layers.Conv2D(64, 3, activation="relu", strides=1, padding="same")(x)
    x = layers.MaxPooling2D(2,2)(x)
    x = layers.Conv2D(128, 3, activation="relu", strides=1, padding="same")(x)
    x = layers.Conv2D(128, 3, activation="relu", strides=1, padding="same")(x)
    x = layers.MaxPooling2D(2,2)(x)
    x = layers.Flatten()(x)

    z = layers.Dense(512, activation="relu")(x)

    z_mean = layers.Dense(latent_dim, name="z_mean")(x)
    z_log_var = layers.Dense(latent_dim, name="z_log_var")(x)
    z_log_var = layers.Lambda(lambda t: tf.clip_by_value(t, -10.0, 10.0))(z_log_var)



    # Sampling layer
    def sampling(args):
        z_mean, z_log_var = args
        eps = tf.random.normal(shape=(tf.shape(z_mean)[0], latent_dim))
        return z_mean + tf.exp(0.5 * z_log_var) * eps

    z = layers.Lambda(sampling, output_shape=(latent_dim,), name="z")([z_mean, z_log_var])


    encoder = Model([img_input], [z_mean, z_log_var, z], name="encoder")
    return encoder

def build_decoder(output_shape=(128, 128, 3)):
    '''
    Parameters
    ----------
      - The latent vector of size latent_dim

    Description
    -----------
    The decoder is structured as followed:
      - 1 dense layer to extract information from the latent vector into a 1D vector of size 16 384 (8*8*256)
      - 1 reshape layer to reshape the vector to the shape (8, 8, 256). This corresponds to a "features map" of size 8x8 with 256 channels.
      This format is necessary to apply the following transposed convolution operations in the rest of the network.
      - 4 transposed convolution layers to increase the size of the image (doubling the width and height) while gradually reducing the number of channels (256 -> 128 -> 64 -> 32 -> 16)
      - One last transposed convolution layer generates the output image. It uses 3 filters, which corresponds the 3 channels of a RGB image.
      The sigmoid activation function is used here because it produces values between 0 and 1, to keep a normalized image.

    Returns
    -------
    A keras Model able to decode a latent vector of size latent_dim into an image of shape (128, 128, 3)
    '''
    latent_input = Input(shape=(latent_dim,), name="decoder_latent_input")

    x = layers.Dense(8 * 8 * 256, activation="relu")(latent_input)
    x = layers.Reshape((8, 8, 256))(x)

    x = layers.Conv2DTranspose(128, 3, strides=2, padding="same", activation="relu")(x)
    x = layers.Conv2DTranspose(64, 3, strides=2, padding="same", activation="relu")(x)
    x = layers.Conv2DTranspose(32, 3, strides=2, padding="same", activation="relu")(x)
    x = layers.Conv2DTranspose(16, 3, strides=2, padding="same", activation="relu")(x)

    output_img = layers.Conv2DTranspose(output_shape[2], 3, activation="sigmoid", padding="same")(x)

    # decoder = Model([latent_input, label_input], output_img, name="decoder")
    decoder = Model([latent_input], output_img, name="decoder")
    return decoder

class CVAE(keras.Model):
    def __init__(self, encoder, decoder, variational=False, **kwargs):
        '''
        Parameters
        ----------
          - The encoder and decoder models that the CVAE model will use to encode the input data and reconstruct it.
          - variational: a boolean optional argument which determines whether the model will be a classic VAE or a CVAE with loss KL.
            If variational=True, KL loss will be calculated in addition to the reconstruction loss.
          - **kwargs: allows to pass other arguments (such as data) to the parent class constructor keras. Model.

        Returns
        -------
        The image cropped and resized in a numpy array of shape (128, 128, 3)
        '''
        super(CVAE, self).__init__(**kwargs)
        self.encoder = encoder
        self.decoder = decoder
        self.total_loss_tracker = keras.metrics.Mean(name="total_loss")
        self.reconstruction_loss_tracker = keras.metrics.Mean(name="reconstruction_loss")

       # Initialization of the attribute 'variational' to control KL loss
        self.variational = variational
        if self.variational:
            self.kl_loss_tracker = keras.metrics.Mean(name="kl_loss")
        else:
            self.kl_loss_tracker = None  # No KL loss if 'variational' is False

    @property
    def metrics(self):
          # Returns the metrics depending on whether KL is used or not
        metrics = [self.total_loss_tracker, self.reconstruction_loss_tracker]
        if self.variational and self.kl_loss_tracker is not None:
            metrics.append(self.kl_loss_tracker)
        return metrics

    def train_step(self, data):
        images = data
        with tf.GradientTape() as tape:
            # Encoding
            z_mean, z_log_var, z = self.encoder([images])
            # Decoding
            reconstruction = self.decoder([z_mean])

            # reconstruction_loss (MSE) computation
            reconstruction_loss = tf.reduce_mean(
                tf.reduce_mean(
                    keras.losses.mean_squared_error(images, reconstruction), axis=(1, 2)
                )
            )

            # KL loss computation if 'variational' is True
            # The KL loss is calculated as the Kullback-Leibler divergence
            # between the approximate distribution (defined by z_mean and z_log_var) and a standard normal distribution
            if self.variational:
              kl_loss = -0.5 * tf.reduce_mean(
                  tf.reduce_mean(1 + z_log_var - tf.square(z_mean) - tf.exp(z_log_var), axis=1)
                  )
              # The weights of the kl_loss could be modified
              total_loss = reconstruction_loss + 0.1 * kl_loss
              self.kl_loss_tracker.update_state(kl_loss)  # Update of KL loss
            else:
                total_loss = reconstruction_loss

        # Gradients computation and weights update
        #  The gradients of the total loss versus the model weights are calculated and used to update the weights via the optimizer.
        grads = tape.gradient(total_loss, self.trainable_weights)
        self.optimizer.apply_gradients(zip(grads, self.trainable_weights))

        # Metrics update
        self.total_loss_tracker.update_state(total_loss)
        self.reconstruction_loss_tracker.update_state(reconstruction_loss)


        return {
            "loss": self.total_loss_tracker.result(),
            "reconstruction_loss": self.reconstruction_loss_tracker.result(),
            "kl_loss": self.kl_loss_tracker.result() if self.variational else 0.0,
        }

# Save of loss functions
class LossHistoryCallback(keras.callbacks.Callback):
    '''
    Description
    -----------
    Callback that records loss values at the end of each epoch during training.

    It stores the total loss, reconstruction loss, and KL divergence loss in
    three separate lists. These values can later be used to visualize training
    progress and assess whether the model is fitting well.
    '''
    def __init__(self):
        super().__init__()

    def on_epoch_end(self, epoch, logs=None):
        # Warning ：logs is a dictionnary containing all loss return
        total_loss_history.append(logs.get("loss"))
        reconstruction_loss_history.append(logs.get("reconstruction_loss"))
        kl_loss_history.append(logs.get("kl_loss"))

# Generation of images at every 10 epochs
class GenerateImageCallback(tf.keras.callbacks.Callback):
    '''
    Description
    -----------
    Callback that generates and displays two images every N epochs during training.

    One image is generated from a random latent vector, and the other is reconstructed
    from a real image passed through the encoder. This allows visual monitoring of
    both the decoder's generative ability and reconstruction quality over time.
    '''
    def __init__(self, encoder, decoder, latent_dim, epoch_interval=10):
        self.encoder = encoder
        self.decoder = decoder
        self.latent_dim = latent_dim
        self.epoch_interval = epoch_interval

    def on_epoch_end(self, epoch, logs=None):
        if (epoch + 1) % self.epoch_interval == 0:
            # Generate 2 images at every 10 epochs (nb epoch can be modified)
            z_sample = tf.random.normal(shape=(1, self.latent_dim))
            img = data[random.randint(1,500)]
            img = tf.expand_dims(img, axis=0)
            z_img, _, _ = self.encoder([img], training=False)

            generated_sample = self.decoder([z_sample], training=False)
            generated_img = self.decoder([z_img], training=False)

            sample_np = generated_sample[0].numpy()
            img_np = generated_img[0].numpy()

            plt.figure(figsize=(4, 2))
            plt.subplot(1, 2, 1)
            plt.title("Sample")
            plt.imshow(sample_np)
            plt.axis('off')

            plt.subplot(1, 2, 2)
            plt.title("Image")
            plt.imshow(img_np)
            plt.axis('off')
            plt.show()

latent_dim = 32  #  latent space dimension

# To test that the CVAE is functionning correctly, unquote the following section
"""
# Build the first encoder/decoder
encoder = build_encoder(input_shape=(128, 128, 3))
decoder = build_decoder(output_shape=(128, 128, 3))
encoder.summary()
decoder.summary()

# Split the data into training and testing parts
x_train, x_test = train_test_split(data, test_size=0.2, random_state=42)

# Create lists which contain loss values
total_loss_history = []
reconstruction_loss_history = []
kl_loss_history = []

# Create CVAE model
cvae = CVAE(encoder, decoder, variational=True)

# Initialise callbacks
history_callback = LossHistoryCallback() # To save the loss
gen_callback = GenerateImageCallback(encoder, decoder, latent_dim=latent_dim, epoch_interval=10) # To see the quality of the imaes we generate at every 10 epochs

# Model compiling and training
cvae.compile(optimizer=keras.optimizers.Adam(clipnorm=1.0))
cvae.fit(x_train, epochs=100, batch_size=32, callbacks=[history_callback, gen_callback])

# Plot the loss as graphic
plt.plot(total_loss_history, label="Total Loss")
plt.plot(reconstruction_loss_history, label="Reconstruction Loss")
plt.plot(kl_loss_history, label="KL Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.title("CVAE Loss over Epochs")
plt.show()

# According to the graphic, check if total loss, reconstruction loss et KL loss convergent rapidement et sont stables.

# Save the model for future usage (encoder, decoder trained with 50000 images)
encoder.save_weights("encoder_50000.weights.h5")
decoder.save_weights("decoder_50000.weights.h5")

# Build 2 new encoder/decoder for testing the saved models
enc = build_encoder(input_shape=(128,128,3))
dec = build_decoder(output_shape=(128,128,3))

# Add weights to the models
enc.load_weights("encoder_50000.weights.h5")
dec.load_weights("decoder_50000.weights.h5")

# Unit test for model loading
z_sample = tf.random.normal(shape=(1, latent_dim))
img = data[random.randint(1,500)]
img = tf.expand_dims(img, axis=0)
z_img, _, _ = enc([img], training=False)

generated_sample = dec([z_sample], training=False)
generated_img = dec([z_img], training=False)

sample_np = generated_sample[0].numpy()
img_np = generated_img[0].numpy()

plt.figure(figsize=(4, 2))
plt.subplot(1, 3, 1)
plt.title("Sample")
plt.imshow(sample_np)
plt.axis('off')

plt.subplot(1, 3, 3)
plt.title("Image")
plt.imshow(img_np)
plt.axis('off')
plt.show()
"""
