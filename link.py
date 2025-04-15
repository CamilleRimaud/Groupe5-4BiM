## lien entre autoencodeur et algo gen

#importer les fonctions et librairies de l'autoencodeur
from tensorflow import keras
import matplotlib.pyplot as plt
import numpy as np
from keras.models import load_model
from algo_gen import crossover, mutation
from cvae_callbacks_traitement_labels import build_decoder, build_encoder
from PIL import Image
import tensorflow as tf
from img_preprocessing import import_data, format_img

def newImages(images_originales):
    # calcul des vecteurs latents
    image_tensor = []
    for img in images_originales:
        img_array = np.array(img)  # Convertit PIL Image en tableau NumPy
        img_tensor = tf.convert_to_tensor(img_array, dtype=tf.float32)  # Convertit en TensorFlow tensor
        image_tensor.append(img_tensor)
    
    image_tensor = np.array(image_tensor)
    V, _, _ = enc(image_tensor, training=False)

    ### Algo gen

    crossFace1,crossFace2,crossFace3,crossFace4,crossFace5,crossFace6 = crossover(V[0], V[1], V[2], V[3])

    mutant1=mutation(crossFace1)
    mutant2=mutation(crossFace2)
    mutant3=mutation(crossFace3)
    mutant4=mutation(crossFace4)
    mutant5=mutation(crossFace5)
    mutant6=mutation(crossFace6)

    mutant7=mutation(crossFace1)
    mutant8=mutation(crossFace2)
    mutant9=mutation(crossFace3)
    mutant10=mutation(crossFace4)
    mutant11=mutation(crossFace5)
    mutant12=mutation(crossFace6)

    mutatedV=np.array([mutant1,mutant2,mutant3,mutant4,mutant5,mutant6, mutant7,mutant8, mutant9, mutant10, mutant11, mutant12])

    # reconstruction nouvelles images avec vecteurs latents mutés
    nouvelles_images = dec([mutatedV], training=False)
    return nouvelles_images

def conversion_tensor_to_PIL(nouvelles_images):
    PIL_img=[]
    for img in nouvelles_images:
        # Etape 0 : récupère un tensor normalisé entre 0 et 1
        eager_tensor=img

        # Étape 1 : convertit le tensor en numpy
        np_array = eager_tensor.numpy()

        # Étape 2 : remet les valeurs entre 0 et 255
        np_array = (np_array * 255).astype(np.uint8)

        # Étape 3 : crée l’image
        image = Image.fromarray(np_array)
        PIL_img.append(image)
    return PIL_img


# récupération du modèle
# Construire 2 nouveaux encoder/decoder
enc = build_encoder(input_shape=(128,128,3))
dec = build_decoder(output_shape=(128,128,3))

# Ajouter les poids aux modèles
enc.load_weights("encoder_50000.weights.h5")
dec.load_weights("decoder_50000.weights.h5")

