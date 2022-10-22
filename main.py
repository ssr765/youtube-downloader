from __future__ import unicode_literals
import multiprocessing
import os
from pathlib import Path
import sys
import logging

import eyed3
import yaml
from youtube_dl import YoutubeDL
from colorama import Fore
from youtube_dl.utils import DownloadError

from engine.style import pintar, generar_ascii
from engine.coverart_gen import generar_cover


def borrar_cache():
    # Borrar la cache.
    print(f"{Fore.BLUE}[⚙] Borrando la cache\n[⚙] ", end="")
    os.system("youtube-dl --rm-cache-dir")
    print(Fore.RESET)

def descargar_video(nombre_cancion, url, nombre_playlist = None):
    # Descarga la canción del video.
    global no_descargadas

    # Reintenta la descarga las veces especificadas, si no lo consigue muestra
    # el error, si no muestra el mensaje de descarga exitosa.
    retries = 0
    while retries < MAX_RETRIES:
        try:
            info = YDL.extract_info(url)
        
        except DownloadError as e:
            retries += 1

        else:
            print(pintar(f"[+] {'(' + nombre_playlist + ') ' if nombre_playlist else ''}Descarga completada: {info['title']}.", Fore.GREEN))

            # Añadir la metadata.
            cancion = eyed3.load(DOWNLOAD_PATH + config['filename'].format(titulo=info['title'], canal=info['channel']) + f" - {info['id']}.mp3")
            cancion.tag.title = info['title']

            # Preferir datos de la canción en caso de que lo sea.
            cancion.tag.artist = ";".join(info['artist'].split(",")) if "artist" in info else info['channel']
            
            if COVER_ART:
                cancion.tag.album = config['filename'].format(titulo=info['title'], canal=info['channel'])
                cancion.tag.images.set(3, generar_cover(info['thumbnail']), "image/jpeg")

            cancion.tag.save(version=eyed3.id3.ID3_V2_3)
            return

    print(pintar(f"[✖] {'(' + nombre_playlist + ') ' if nombre_playlist else ''}No se ha podido encontrar {nombre_cancion}.", Fore.RED))
    no_descargadas += 1


# Cargar la configuración.
with open("config/config.yaml", "r", encoding="utf-8") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)


FILENAME = config['filename'].format(titulo="%(title)s", canal="%(channel)s") + " - %(id)s.%(ext)s"

# Si no se especifica localización de descarga, esta se hará en downloads/
DOWNLOAD_PATH = config['download_path'] if config['download_path'] != "" else "downloads/"
DOWNLOAD_PATH = "/".join(DOWNLOAD_PATH.split("\\"))
DEFAULT_URL = config['default_url']
COVER_ART = config['cover_art']

# Máximo de 50 procesos.
WORKERS = config['workers']
WORKERS = multiprocessing.cpu_count() * WORKERS if multiprocessing.cpu_count() * WORKERS <= 50 else 50

# Reintentos máximos para que deje de intentar descargar la canción.
MAX_RETRIES = 5

# Logger para ignorar los errores.
LOGGER = logging.getLogger("ytdl-ignore")
LOGGER.disabled = True

# YoutubeDL
YDL_OPTS = {
    'format': 'bestaudio/best',
    'outtmpl': DOWNLOAD_PATH + FILENAME,
    'noplaylist': True,
    'quiet': True,
    'logger': LOGGER,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}
YDL = YoutubeDL(YDL_OPTS)

# Contador de canciones que han dado error o ya estaba descargadas.
no_descargadas = 0

# Crear la carpeta de descargas en caso de que no exista y buscar canciones
# ya descargadas.
Path(DOWNLOAD_PATH).mkdir(parents=True, exist_ok=True)
ya_descargados = [cancion[-15:-4] for cancion in os.listdir(DOWNLOAD_PATH)]

# Leer el parametro en la ejecución del script.
try:
    url = sys.argv[1]

except IndexError:
    # En caso de que no se especifique URL intentará usar la URL por defecto,
    # si no lo consigue terminará el programa.
    if DEFAULT_URL != "":
        url = DEFAULT_URL

    else:
        print(pintar(f"[⚠] Debes introducir una URL de YouTube.", Fore.RED))
        sys.exit()


if __name__ == '__main__':
    generar_ascii()
    print(f"{pintar('[⚙] Nucleos del procesador:', Fore.BLUE)} {multiprocessing.cpu_count()}")
    print(f"{pintar('[⚙] Descargando en:', Fore.BLUE)} {DOWNLOAD_PATH}")
    print()

    # Descarga de video.
    if url.find("watch") != -1 or url.find("youtu.be") != -1:
        print(f"[👁] Leyendo datos de la canción...")
        
        # Consigue el nombre y comprueba que no esté descargada.
        try:
            info = YDL.extract_info(url, download=False)
        
        except DownloadError:
            print(pintar(f"[⚠] El video de \"{url}\" no existe o es privado.", Fore.RED))
            sys.exit()

        if info['id'] not in ya_descargados:
            print(f"[⬇] Descargando {info['title']}...")
            descargar_video(info['title'], url)
        
        else:
            print(pintar(f"[!] {info['title']} ya estaba descargada.", Fore.YELLOW))
            no_descargadas += 1
        
        borrar_cache()

    # Descarga de playlist.
    elif url.find("list") != -1:
        print(f"[👁] Leyendo datos de la playlist... (Esto puede tardar un rato depende la duración de la playlist.)")

        # Consigue el nombre y la lista de videos.
        try:
            info = YDL.extract_info(url, download=False)
        
        except DownloadError:
            print(pintar(f"[⚠] \"{url}\" no es una URL valida. Saliendo del programa.", Fore.RED))
            sys.exit()
            
        print(f"[⬇] Descarga de \"{info['title']}\" iniciada.")

        # Pool de procesos.
        pool = multiprocessing.Pool(WORKERS)

        for video in info['entries']:
            if video['id'] not in ya_descargados:

                # Los procesos empiezan a descargar las canciones.
                p = pool.apply_async(descargar_video, [video['title'], video['webpage_url'], info['title']])
            
            else:
                print(pintar(f"[!] ({info['title']}) {video['title']} ya estaba descargada.", Fore.YELLOW))
                no_descargadas += 1

        # Espera a que terminen todas las descargas para terminar el programa.
        pool.close()
        pool.join()
        
        print(pintar(f"[✔] Se han descargado {len(info['entries']) - no_descargadas}/{len(info['entries'])} canciones de \"{info['title']}\".", Fore.GREEN))
        borrar_cache()

    else:
        print(f"{Fore.RED}[⚠] \"{url}\" no es una URL valida. Saliendo del programa.{Fore.RESET}")