
## import libraries
import random as rd
import numpy as np

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
    crossover1_2=[]
    crossover1_3=[]
    crossover1_4=[]
    crossover2_3=[]
    crossover2_4=[]
    crossover3_4=[]

    for i in range(len(face1)):
        val1=face1[i]
        val2=face2[i]
        val3=face3[i]
        val4=face4[i]
        crossover1_2.append(float(np.mean([val1,val2])))
        crossover1_3.append(float(np.mean([val1,val3])))
        crossover1_4.append(float(np.mean([val1,val4])))
        crossover2_3.append(float(np.mean([val2,val3])))
        crossover2_4.append(float(np.mean([val2,val4])))
        crossover3_4.append(float(np.mean([val3,val4])))

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
    mutantFace = face.copy()

    for i in range(len(face)):
        if rd.random() < 0.05:
            # Appliquer une mutation
            mutation = rd.uniform(-mutation_strength, mutation_strength)
            mutantFace[i] += mutation

    return mutantFace

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
