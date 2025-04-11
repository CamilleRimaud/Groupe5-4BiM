
## import libraries
import random as rd
import numpy as np
import tensorflow as tf 

# initialize pop
#fait par le décodeur


# selection meilleurs individus
#fais manuellement par l'utilisateur

# crossover



def crossover(face1, face2, face3, face4):
    '''

    Parameters
    ----------
    The four faces selected by the user.
    Each face is a vector with n values representing the face


    Returns
    -------
    Six faces: vectors
        -crossover between 1 and 2
        -crossover between 1 and 3
        -crossover between 1 and 4
        -crossover between 2 and 3
        -crossover between 2 and 4
        -crossover between 3 and 4

    This function creates all the crossovers between the four
    faces in entry.
    New vector contains value, means of the values of the parent faces


    '''
    
    crossover1_2 = tf.reduce_mean(tf.stack([face1, face2]), axis=0)
    crossover1_3 = tf.reduce_mean(tf.stack([face1, face3]), axis=0)
    crossover1_4 = tf.reduce_mean(tf.stack([face1, face4]), axis=0)
    crossover2_3 = tf.reduce_mean(tf.stack([face2, face3]), axis=0)
    crossover2_4 = tf.reduce_mean(tf.stack([face2, face4]), axis=0)
    crossover3_4 = tf.reduce_mean(tf.stack([face3, face4]), axis=0)

    return crossover1_2, crossover1_3, crossover1_4, crossover2_3, crossover2_4, crossover3_4

# mutations



def mutation(face, mutation_strength=1):
    '''


    Parameters
    ----------
    face : is a vector


    Returns
    -------
    Another face after mutation process, also a vector

    The mutation process switches each value of the vector
    with a probability of 5%

    '''
    

    mutation_mask = tf.random.uniform(shape=face.shape) < 0.05
    
    mutation_values = tf.random.uniform(shape=face.shape, 
                                        minval=-mutation_strength, 
                                        maxval=mutation_strength)
    
    mutant_face = tf.where(mutation_mask, face + mutation_values, face)
    
    return mutant_face

# generation new pop
#genration n =10 faces
#user selects 4
'''

crossFace1,crossFace2,crossFace3,crossFace4,crossFace5,crossFace6=crossover(face1, face2, face3, face4)


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