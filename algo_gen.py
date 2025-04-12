
## import libraries
import random as rd
import numpy as np
import tensorflow as tf 


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
    
    crossover1_2 = np.mean([face1, face2], axis=0)
    crossover1_3 = np.mean([face1, face3], axis=0)
    crossover1_4 = np.mean([face1, face4], axis=0)
    crossover2_3 = np.mean([face2, face3], axis=0)
    crossover2_4 = np.mean([face2, face4], axis=0)
    crossover3_4 = np.mean([face3, face4], axis=0)

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
    
   
    # Create mutation mask (5% probability)
    mutation_mask = np.random.random(size=face.shape) < 0.05
   
   # Generate random mutation values
    mutation_values = np.random.uniform(
       low=-mutation_strength,
       high=mutation_strength,
       size=face.shape
   )
   
   # Apply mutations where mask is True
    mutant_face = np.where(mutation_mask, face + mutation_values, face)
   
    
    return mutant_face

