'''
This code transforms the file list_attr_celeba.txt in a np.array
where the first line is the list of th attributes
and the other lines are lists of 1 and -1 
according to whether or not the face contains said attribute

We have removed some attributes deemed unimportant in the context of 
this project.
'''

import numpy as np

class AttributeTable:
    def __init__(self, file_path):
        self.table = self.load_attributes(file_path)

    def load_attributes(self, file_path):
        with open(file_path, 'r') as file:
            ligns = file.readlines()

        attributes = ligns[1].split(' ')
        attributes_to_remove = ['Attractive', 'Bags_Under_Eyes', 'Blurry', 'Heavy_Makeup',
                                'Mouth_Slightly_Open', 'Smiling', 'Wearing_Earrings',
                                'Wearing_Hat', 'Wearing_Lipstick', 'Wearing_Necklace',
                                'Wearing_Necktie', '\n','5_o_Clock_Shadow ',
                                'Arched_Eyebrows ', 'Bangs','Big_Lips',
                                'Big_Nose ','Bushy_Eyebrows ','Chubby ',
                                'Double_Chin ', 'High_Cheekbones ',
                                'Narrow_Eyes', 'Oval_Face ','Pointy_Nose ',
                                'Receding_Hairline ', 'Rosy_Cheeks ',
                                'Sideburns ', 'Young ']


        for attr in attributes_to_remove:
            attributes.remove(attr)

        table = [attributes]
        
        indices_to_remove = [1,2,3,4,6,7,8,11,13,14,15,19,20,22,24,26,28,29,30,31,32,35,36,37,38,39,40] 

        for index in range(2, len(ligns)):
            line = ligns[index].split(' ')
            line = line[1:]
            line = [int(i) for i in line if i != '']

            # Indices à supprimer
            line = [line[i] for i in range(len(line)) if i not in indices_to_remove]

            table.append(line)
          

        return np.array(table)

    def get_table(self):
        return self.table




