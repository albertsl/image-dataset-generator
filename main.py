from os import path, mkdir
from PIL import Image
import pandas as pd
import numpy as np

output_folder = "generated"
if not path.exists(output_folder):
    mkdir(output_folder)

backgrounds = ["countryside", "desert", "forest", "glacial"]
characters = ["mage", "warrior", "pirate", "monster", "toadking"]
objects = ["none", "barrel", "anchor", "axe", "bomb", "key", "chest", "bananas", "cupcake", "donut", "heart",]

def generate_image(background, character, object, file_name):
    """Generate image with given background, given character and given object and save it with the given file name

    Args:
        background (str): background name
        character (str): character name
        object (str): object name
        file_name (str): file name
    """
    background_file = path.join("backgrounds", f"{background}.png")
    background_image = Image.open(background_file)

    #Create character
    character_file = path.join("characters", f"{character}.png")
    character_image = Image.open(character_file)

    coordinates = (int(1920/2-character_image.width/2), int(1000-character_image.height)) #x, y
    background_image.paste(character_image, coordinates, mask=character_image)

    #Create object
    if object != "none":
        object_file = path.join("objects", f"{object}.png")
        object_image = Image.open(object_file)

        coordinates = (int(1920/2+character_image.width/2+30), int(1000-object_image.height)) #x, y
        background_image.paste(object_image, coordinates, mask=object_image)

    output_file = path.join(output_folder, f"{file_name}.png")
    background_image.save(output_file)

def generate_all_imgs():
    """Generate all possible combination of images
    """
    num = 0
    df = pd.DataFrame(columns = ["background", "character", "object", "generated image"])
    for background in backgrounds:
        for character in characters:
            for object in objects:
                generate_image(background, character, object, f"generated{num}")
                data = [background, character, object, f"generated{num}"]
                s = pd.Series(data, index=df.columns)
                df = df.append(s, ignore_index=True)
                num += 1
    df.to_csv('data.csv', index=False)

def generate_random_imgs(total_imgs):
    """Generates a given number of random images according to predefined probabilities

    Args:
        total_imgs (int): total number of images to generate
    """
    df = pd.DataFrame(columns = ["background", "character", "object", "generated image"])

    for num in range(total_imgs):
        background = np.random.choice(np.arange(0,len(backgrounds)), p=[0.3, 0.3, 0.3, 0.1])
        background = backgrounds[background]
        
        character = np.random.choice(np.arange(0,len(characters)), p=[0.4, 0.3, 0.2, 0.095, 0.005])
        character = characters[character]

        object = np.random.choice(np.arange(0,len(objects)), p=[0.3, 0.2, 0.1, 0.1, 0.1, 0.05, 0.05, 0.04, 0.03, 0.025, 0.005])
        object = objects[object]

        generate_image(background, character, object, f"generated{num}")
        data = [background, character, object, f"generated{num}"]
        s = pd.Series(data, index=df.columns)
        df = df.append(s, ignore_index=True)

    df.to_csv('data.csv', index=False)

if __name__ == "__main__":
    #generate_all_imgs()
    generate_random_imgs(500)

