## lien entre autoencodeur et algo gen

#importer les fonctions et librairies de l'autoencodeur
from tensorflow import keras
import matplotlib.pyplot as plt
import numpy as np
from keras.models import load_model
from algo_gen import crossover, mutation
from cvae_callbacks_traitement_labels import build_decoder, build_encoder, import_data, format_img
from PIL import Image
import tensorflow as tf

def newImages(imgOg):
    # calcul des vecteurs latents
    V, _, _ = enc(images_originales, training=False)

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



# récupération du modèle
# Construire 2 nouveaux encoder/decoder
enc = build_encoder(input_shape=(128,128,3))
dec = build_decoder(output_shape=(128,128,3))

# Ajouter les poids aux modèles
enc.load_weights("encoder.weights.h5")
dec.load_weights("decoder.weights.h5")




# C'est juste pour produire images_originales, ce sera à modifier
nb_img=500
data=import_data(nb_img)
images_originales=data[0:4]
#images_originales= RobotPortrait(root).select_portrait() # il faudra mettre le choix de l'user

nouvelles_images=newImages(images_originales)



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

PIL_img=conversion_tensor_to_PIL(nouvelles_images)

"""
plt.subplot(2, 2, 1)
plt.title("Nouveau portrait 1")
plt.imshow(nouvelles_images[0])
plt.axis('off')
plt.show()


images_originales_bis=nouvelles_images[0:4]
nouvelles_images_bis=newImages(images_originales_bis)

#affichage à envoyer dans l'interface

plt.subplot(2, 2, 1)
plt.title("Nouveau portrait 1")
plt.imshow(nouvelles_images_bis[0])
plt.axis('off')


plt.subplot(2, 2, 2)
plt.title("Nouveau portrait 2")
plt.imshow(nouvelles_images_bis[1])
plt.axis('off')


plt.subplot(2, 2, 3)
plt.title("Nouveau portrait 3")
plt.imshow(nouvelles_images_bis[2])
plt.axis('off')


plt.subplot(2, 2, 4)
plt.title("Nouveau portrait 4")
plt.imshow(nouvelles_images_bis[3])
plt.axis('off')
plt.show()


plt.subplot(2, 2, 1)
plt.title("Nouveau portrait 5")
plt.imshow(nouvelles_images[4])
plt.axis('off')

plt.subplot(2, 2, 2)
plt.title("Nouveau portrait 6")
plt.imshow(nouvelles_images[5])
plt.axis('off')

plt.subplot(2, 2, 3)
plt.title("Nouveau portrait 7")
plt.imshow(nouvelles_images[6])
plt.axis('off')

plt.subplot(2, 2, 4)
plt.title("Nouveau portrait 8")
plt.imshow(nouvelles_images[7])
plt.axis('off')
plt.show()


plt.subplot(2, 2, 1)
plt.title("Nouveau portrait 9")
plt.imshow(nouvelles_images[8])
plt.axis('off')

plt.subplot(2, 2, 2)
plt.title("Nouveau portrait 10")
plt.imshow(nouvelles_images[9])
plt.axis('off')

plt.subplot(2, 2, 3)
plt.title("Nouveau portrait 11")
plt.imshow(nouvelles_images[10])
plt.axis('off')

plt.subplot(2, 2, 4)
plt.title("Nouveau portrait 12")
plt.imshow(nouvelles_images[11])
plt.axis('off')
plt.show()
"""
