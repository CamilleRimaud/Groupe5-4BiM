# Guide d'installation
Il est nécessaire d'avoir au préalable les packages suivants :
* python (version 3.9.7)
* tensorflow (version 2.19.0)
* keras (version 3.9.0)
* PIL
* sklearn (version 1.6.1)
* (numpy et mathplotlib)


# Dev_logiciel
Projet de développement logiciel 4BiM - Groupe 5


**Documentation**  
Gehao Hua, Jeanne Le Guillou, Meyane Marage, Camille Rimaud  
Mars 2025

1. Introduction

Le logiciel permet de transformer des images en objets appelés vecteurs latents, sur lesquels est appliqué un algorithme génétique, créant de nouveaux vecteurs. Ceux-ci peuvent subir une transformation inverse pour générer des images inédites (qui ne proviennent pas de la banque d’images).

Ainsi, le logiciel permet de générer un portrait robot : 

- l’utilisateur mentionne les caractéristiques physiques du suspect recherché  
- le logiciel lui fournit 12 portraits de la banque d’images possédant ses caractéristiques  
- l’utilisateur sélectionne les 4 portraits les plus ressemblants  
- ces 4 portraits sont convertis en vecteurs latents, subissent l’algorithme génétique, et donnent naissance à 12 nouveaux portraits robots, tous possédant les caractéristiques du suspect 

1.5 Première génération de visage

La première génération de visage se base uniquement sur les attributs physiques enregistrés par l’utilisateur et pioche les visages les plus adéquats dans un sample des visages du dataset celebA.

createDataframe(path)  
**parameters** le chemin vers le fichier list\_attr\_celeba.txt issu de la base de donnée celebA  
**return** un dataframe avec en première colonne le nom des images et pour le reste des colonnes les valeurs des images pour tous les attributs.

aFewModifications(df)  
**parameters** le dataframe précédemment créé  
**return** un nouveau dataframe modifié pour les futures utilisation  
**method** on retire tous les attributs qui ne nous seront pas utiles, puis on prend le nom des images en index et on retire le colonne qui contient les noms des images

FirstGen(selected\_features, df)  
**parameters** liste de \-1 et 1 en fonction des attributs sélectionnés par l’utilisateur, le dataframe modifié  
**return** liste des indices des images du la database les plus proches de la description de l’utilisateur  
**method** le calcul de la meilleure image se fait avec la distance de hamming

getUserDescription(attr\_chosed)  
**parameters** une liste de str des attributs choisis par l’utilisateur  
**return** une liste de \-1 et 1 en fonction de ce qu’a choisi l’utilisateur

load\_choices()  
**return** une liste de str des attributs choisis par l’utilisateur  
**method** chargement du fichier JSON pour le transformer en liste

2.  Autoencodeur

L’autoencodeur est composé de deux grandes briques:

build\_encoder(input\_shape=(128, 128, 3))  
**parameters** un portrait (une image au format (128x128x3), c'est-à-dire une image carrée avec les 3 canaux RVB)   
**return** un vecteur latent de dimension 32

build\_decoder(output\_shape=(128, 128, 3))  
**parameters** un vecteur latent de dimension 32  
**return** une image au format (128x128x3)

Cette structure implique que les images produites par le decoder gardent les mêmes attributs que les images utilisées pour générer le vecteur latent. Il n’est pas possible de demander au decoder de produire une image en lui fournissant une liste d’attributs.

De plus, des classes Callback sont ajoutées à l’autoencodeur pour suivre la progression de l’entraînement en générant deux images toutes les 10 époques, et aussi pour déterminer si on obtient un loss convergent à la fin de l’entraînement. 

Pour enregistrer le modèle, les fichiers de poids du modèle sont enregistrés en format weights.h5 (un format est hautement compatible). Pour reconstruire le même autoencodeur à partir de ces fichiers, il suffit de créer une architecture vide, puis d’y charger les poids sauvegardés dans les fichiers weights.h5. 

Pour enregistrer les fichiers de poids :   
encoder.save\_weights(“encoder.weights.h5”)  
decoder.save\_weights(“decoder.weights.h5”)

Pour charger les fichiers de poids :   
new\_encoder.load\_weights(“encoder.weights.h5”)  
new\_decoder.load\_weights(“decoder.weights.h5”)

3. Algorithme génétique

crossover(face1,face2,face3,face4) :  
**parameters** Quatre vecteurs latents encodant les quatre visages ”parents”.  
**return** Six vecteurs encodant six visages ”enfants”, les crossover entre  
tous les quatres visages d'entrée.  
**method** Chaque vecteur enfant a comme valeur la moyenne entre les valeurs de même indice chez les deux vecteurs parents.

mutation(face, mutation\_strength) :  
**parameters** Cette fonction prend en entrée un seul visage encodé en vecteur. Et un float positif représentant une force de mutation.  
**return** Le visage muté sous forme de vecteur.  
**method** Avec une probabilité de 0.05, la fonction ajoute aux valeurs du vecteur un float compris entre la force de mutation et son opposé, et choisit aléatoirement.  
