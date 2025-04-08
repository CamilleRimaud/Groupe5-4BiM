## lien entre autoencodeur et algo gen

#importer les fonctions et librairies de l'autoencodeur
from tensorflow import keras
import matplotlib.pyplot as plt
import numpy as np
from keras.models import load_model
from algo_gen import crossover, mutation
from Interface_graphique import RobotPortrait, root


def newImages(imgOg):
    V, _, _ = encoder.predict(imgOg, batch_size=32)
    
    #algo gen
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
    
    nouvelles_images = decoder.predict([mutatedV])
    return nouvelles_images

# récupération du modèle
encoder = load_model("encoder_model.keras", compile=False)
decoder = load_model("decoder_model.keras", compile=False)


#génération d'un vecteur latent
#images_originales= RobotPortrait(root).select_portrait() # il faudra mettre le choix de l'user

#calcul vecteurs latents
#V, _, _ = encoder.predict(images_originales, batch_size=32)

### rentre en jeu l'algo gen
'''
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
'''
#mutatedV=np.array([mutant1,mutant2,mutant3,mutant4,mutant5,mutant6, mutant7,mutant8, mutant9, mutant10, mutant11, mutant12])

# reconstruction nouvelles images avec vecteurs latents mutés
#nouvelles_images = decoder.predict([mutatedV])

#affichage à envoyer dans l'interface
'''
plt.subplot(2, 2, 2)
plt.title("Nouveau portrait 1")
plt.imshow(nouvelles_images[0])
plt.axis('off')


plt.subplot(2, 2, 4)
plt.title("Nouveau portrait 2")
plt.imshow(nouvelles_images[1])
plt.axis('off')
plt.show()

plt.subplot(2, 2, 4)
plt.title("Nouveau portrait 2")
plt.imshow(nouvelles_images[2])
plt.axis('off')
plt.show()

plt.subplot(2, 2, 4)
plt.title("Nouveau portrait 2")
plt.imshow(nouvelles_images[3])
plt.axis('off')
plt.show()

plt.subplot(2, 2, 4)
plt.title("Nouveau portrait 2")
plt.imshow(nouvelles_images[4])
plt.axis('off')
plt.show()

plt.subplot(2, 2, 4)
plt.title("Nouveau portrait 2")
plt.imshow(nouvelles_images[5])
plt.axis('off')
plt.show()

plt.subplot(2, 2, 4)
plt.title("Nouveau portrait 2")
plt.imshow(nouvelles_images[6])
plt.axis('off')
plt.show()

plt.subplot(2, 2, 4)
plt.title("Nouveau portrait 2")
plt.imshow(nouvelles_images[7])
plt.axis('off')
plt.show()

plt.subplot(2, 2, 4)
plt.title("Nouveau portrait 2")
plt.imshow(nouvelles_images[8])
plt.axis('off')
plt.show()

plt.subplot(2, 2, 4)
plt.title("Nouveau portrait 2")
plt.imshow(nouvelles_images[9])
plt.axis('off')
plt.show()

plt.subplot(2, 2, 4)
plt.title("Nouveau portrait 2")
plt.imshow(nouvelles_images[10])
plt.axis('off')
plt.show()

plt.subplot(2, 2, 4)
plt.title("Nouveau portrait 2")
plt.imshow(nouvelles_images[11])
plt.axis('off')
plt.show()

plt.subplot(2, 2, 4)
plt.title("Nouveau portrait 2")
plt.imshow(nouvelles_images[12])
plt.axis('off')
plt.show()
'''