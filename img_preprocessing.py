import numpy as np
from PIL import Image
import os

def format_img(id):
    """
    For resizing the images to 128*128
    
    Args: 
        Id of image.
    
    Returns: 
        The Numpy array corresponding to the image.
    """
    image = Image.open(f'./{id}.jpg')
    image = image.crop((0, 20, 178, 198))
    img_resized = image.resize((128, 128))
    image_np = np.array(img_resized)
    return image_np

def import_data(nb_img):
    """
        This function transforms a certain number of images into Numpy array and returns them as a list.

    Args:
        nb_img (int): The number of images to be transformed (the first n images in a folder)

    Returns:
        data: A list containing the Numpy arrays transformed from images
    """
    data = []
    for i in range(1, nb_img + 1):
        id = f"{i:06}"
        data.append(format_img(id))
        if i % 1000 == 0:
            print(f"Processed {id}")
    data = np.array(data, dtype=np.uint8)  # Normalization to be realized later
    print("Shape:", data.shape)
    return data

# Import the first 50000 images
data = import_data(1000)

# Save as Numpy compressed file
np.savez_compressed("processed_faces_50000.npz", data=data)
print("Transformed images saved as: processed_faces_50000.npz")
