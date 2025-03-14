import numpy as np 

path_file= './list_attr_celeba.txt'

with open(path_file, 'r') as file:
    ligns= file.readlines()
    
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


table= np.array(attributes)



for index in range(2, len(ligns)):
    line=(ligns[index].split(' '))
    line=line[1:]
    line= [int(i) for i in line if i!='']
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

    line=np.array(line)
    new_matrix= np.vstack((table, line))
    table=new_matrix 
    






