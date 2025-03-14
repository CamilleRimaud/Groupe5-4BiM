'''
This code transforms the file list_attr_celeba.txt in a np.array
where the first line is the list of th attributes
and the other lines are lists of 1 and -1 
according to whether or not the face contains said attribute

We have removed some attributes deemed unimportant in the context of 
this project.
'''

#import libraries
import numpy as np 

#path to the file to modify
path_file= './list_attr_celeba.txt'

with open(path_file, 'r') as file:
    ligns= file.readlines()

#remove all the attributes unuseful 
attributes=ligns[1].split(' ')
attributes.remove('Attractive')
attributes.remove('Bags_Under_Eyes')
attributes.remove('Blurry')
attributes.remove('Heavy_Makeup')
attributes.remove('Mouth_Slightly_Open')
attributes.remove('Smiling')
attributes.remove('Wearing_Earrings')
attributes.remove('Wearing_Hat')
attributes.remove('Wearing_Lipstick')
attributes.remove('Wearing_Necklace')
attributes.remove('Wearing_Necktie')
attributes.remove('\n')

#initialize the table
table= np.array(attributes)


#for all the lines, some modifications then add them to the table
for index in range(2, len(ligns)):
    line=(ligns[index].split(' ')) # transform into list
    line=line[1:] #remove title of image
    line= [int(i) for i in line if i!=''] #transform in integer
    #deletion of the values linked to unuseful attributes
    del(line[3])
    del(line[3])
    del(line[9])
    del( line[16])
    del( line[18])
    del( line[27])
    del( line[29])
    del( line[29])
    del( line[29])
    del( line[29])
    del( line[29])
    #convert into array and add to table
    line=np.array(line)
    new_matrix= np.vstack((table, line))
    table=new_matrix 
    






