from PIL import Image

def pixel_sorting(image_path, threshold=100):
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size

    # On parcourt chaque ligne de l'image
    for y in range(height):
        row = [pixels[x, y] for x in range(width)]
        
        # On trie uniquement les pixels qui dépassent un certain seuil de luminosité
        # (Ici, une formule simple pour estimer la luminosité : R + G + B)
        sorted_row = sorted(row, key=lambda p: p[0] + p[1] + p[2] if (p[0] + p[1] + p[2]) > threshold else 0)
        
        # On réinjecte les pixels triés dans l'image
        for x in range(width):
            pixels[x, y] = sorted_row[x]
            
    img.save("exit.png")
    print("Image triée sauvegardée !")

pixel_sorting("photo.png", threshold=300)