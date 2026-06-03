import random
from PIL import Image

def scanline_glitch(image_path):
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size

    for y in range(height):
        # Une chance sur 10 de faire glitcher cette ligne
        if random.random() < 0.10:
            # On choisit un décalage horizontal aléatoire
            shift = random.randint(-50, 50)
            row = [pixels[x, y] for x in range(width)]
            
            # On applique le décalage (effet de roulement/shift)
            for x in range(width):
                new_x = (x + shift) % width
                pixels[new_x, y] = row[x]
                
    img.save("decal.png")
    print("Image shiftée sauvegardée !")

# Exemple d'appel : 
scanline_glitch("photo.png")