from io import BytesIO
import requests

from PIL import Image


def generar_cover(link) -> bytes:
    # Coje la miniatura del video y devuelve una imagen cuadrada con bordes
    # negros en formato bytes para que eyed3 pueda trabajar con ella.
    x = requests.get(link)
    data = x.content

    # Imagen en negro.
    final_cover = Image.new(mode="RGB", size=(1280, 1280))

    # Poner la miniatura en el fondo negro.
    cover = Image.open(BytesIO(data))
    cover = cover.resize((1280, 720))
    Image.Image.paste(final_cover, cover, (0, 280))

    # Convertir la imagen a bytes y devolver los bytes.
    imagedata = BytesIO()
    final_cover.save(imagedata, format="JPEG")

    return imagedata.getvalue()