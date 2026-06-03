from PIL import Image, ImageChops

def rgb_split(image_path, offset=15):
    # On ouvre l'image originale
    img = Image.open(image_path).convert("RGB")
    r, g, b = img.split()

    # On utilise ImageChops.offset pour décaler les canaux
    # offset(image, xoffset, yoffset)
    r_decale = ImageChops.offset(r, offset, 0)
    b_decale = ImageChops.offset(b, -offset, 0)
    
    # On fusionne à nouveau les canaux (le vert "g" reste au centre)
    img_glitch = Image.merge("RGB", (r_decale, g, b_decale))
    img_glitch.save("glitch.png")
    print("Glitch RGB sauvegardé avec succès !")

# Lance le script (assure-toi que "ta_photo.jpg" est bien dans le même dossier)
rgb_split("photo.png", offset=20)