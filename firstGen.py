# import librairies

import pandas as pd
from Interface_graphique import RobotPortrait
import tkinter as tk
import numpy as np
import json

#functions

def createDataframe(path):
    '''
    

    Parameters
    ----------
    path : the path leading to the file on which the dataframe is based

    Returns
    -------
    df : dataframe created
    
    This function opens the file makes 
    a dataframe to facilitate further manipulations.

    '''
    with open(path, 'r') as file:
         # Ignore first line
        file.readline()

        # Read second line to get attributes
        attributes = file.readline().strip().split()

        # Initialise list to store data
        data = []

        # Read the following lines
        for line in file:
            elements = line.strip().split()
            # First element is the name of the image
            name_image = elements[0]
            # The following elements are the associated values
            values = list(map(int, elements[1:]))
            # Add a line to data, with image name and the values
            data.append([name_image] + values)

    # Create a  DataFrame
    df = pd.DataFrame(data, columns=['Image'] + attributes)
    return df

def aFewModifications(df):
    '''
    

    Parameters
    ----------
    df : dataframe 

    Returns
    -------
    None.
    
    This function is here to transform the dataframe for further use

    '''
    attributes_to_remove = ['Attractive', 'Bags_Under_Eyes', 'Blurry', 'Heavy_Makeup',
                                'Mouth_Slightly_Open', 'Smiling', 'Wearing_Earrings',
                                'Wearing_Hat', 'Wearing_Lipstick', 'Wearing_Necklace',
                                'Wearing_Necktie','5_o_Clock_Shadow',
                                'Arched_Eyebrows', 'Bangs','Big_Lips',
                                'Big_Nose','Bushy_Eyebrows','Chubby',
                                'Double_Chin', 'High_Cheekbones',
                                'Narrow_Eyes', 'Oval_Face','Pointy_Nose',
                                'Receding_Hairline', 'Rosy_Cheeks',
                                'Sideburns', 'Young']
    attributes_to_remove.sort()
    for attr in attributes_to_remove:
        if attr in df.columns:
            del df[attr]
    df.index=df['Image']
    del df['Image']
    return df 

def FirstGen(selected_features, df):
    '''
    

    Parameters
    ----------
    selected_features : list of -1 and 1 of the features selected 
    by the user
    
    df : dataframe with name of the images in index
    attributes as columns names
    and containing all the values: -1 or 1 of
    whether or not image contains attributes

    Returns
    -------
    list of the 12 images names closest to what the user wants

    '''
    images= df.index #name of the images
    allImages=np.array(df.values.tolist()) #array of the list of the values of each image
    hamming_distances = np.sum(allImages != selected_features, axis=1) #calculate distance between each image and selected features
    closest_index = np.argsort(hamming_distances)[:12] #takes the 12 index of image closest to selected_features
    firstGen=images[closest_index] # name of the 12 image based on the index above
    return list(firstGen)


def getUserDescription(attr_chosed):
    '''
    

    Parameters
    ----------
    attr_chosed : list of string of the attributes chosed by the user

    Returns
    -------
    user_description : list of 1 and -1 according to whether the attributes was chosen or not
    
    

    '''
    allAttr=sorted(["Male", "Pale-skin", "Eyeglasses", "Gray Hair", "Blond Hair", "Black Hair", "Brown Hair", "Bald", "Straight Hair", "Wavy Hair", "No Beard", "Mustache", "Goatee"])
    user_description=[]
    for attr in allAttr:
        if attr in attr_chosed:
            user_description.append(1)
        else:
            user_description.append(-1)
    return user_description
    
#main

df=aFewModifications(createDataframe("list_attr_celeba.txt"))[:501] # we only keep the 500 first images of the dataset 
root = tk.Tk()
robot_portrait = RobotPortrait(root)
attr_chosed = robot_portrait.selected_features 
user_description= getUserDescription(attr_chosed)
#list of the name of the 12 first images, 
#ex:['141843.jpg', '202277.jpg', '061457.jpg', '197096.jpg', '103778.jpg', '180964.jpg', '125474.jpg', '031481.jpg', '066716.jpg', '165368.jpg', '182044.jpg', '104025.jpg']




firstGen = FirstGen(user_description, df)
print(firstGen)  # Affiche les 12 images générées





