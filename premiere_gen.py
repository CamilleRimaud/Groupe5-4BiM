## import libraries
import tkinter as tk
from Interface_graphique import RobotPortrait
from traitement_donnees import AttributeTable


##functions
def dict_features(selected_features):
    # transforme les attributs select en dico avec attributs en cles, -1 ou 1 en values
    return dict(zip(attributes, selected_features))

def getFirstGen(faces, goal):
    allScore=[]
    
    for face in faces.values():
        score=0
        for attribut in selected_features.keys():
            if face[attribut]==selected_features[attribut]:
                score+=1
        allScore.append(score)
    indexScores = list(enumerate(allScore))
    sortedScores = sorted(indexScores, key=lambda x: x[1], reverse=True)
    top_12_indices = [index for index, value in sortedScores[:12]]
    
    list_FirstGen=[]
    for ind in top_12_indices:
        
        list_FirstGen.append(faces[ind])
    return list_FirstGen # retourne le numero (face1, face36, ..) des 12 visages les plus proches de celui voulu
        


##main 
attributes= ["Male ",
             "Pale_Skin ",
             "Eyeglasses ",
             "Gray_Hair ",
             "Blond_Hair ",
             "Black_Hair ",
             "Brown_Hair",
            "Bald",
            "Straight_Hair",
            "Wavy_Hair ",
            "No_Beard",
            "Mustache",
            "Goatee ",]


root= tk.Tk()
robot_portrait = RobotPortrait(root)
selected_features = robot_portrait.selected_features


    

attribute_table = AttributeTable('./list_attr_celeba.txt')
table=attribute_table.get_table()

faces = {}
for i in range(1, 201):
    faces[f'face{i}'] = dict(zip(table[0], [int(j) for j in table[i]]))


firstGen = getFirstGen(faces, selected_features)
print(firstGen)

 

