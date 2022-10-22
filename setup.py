import os
import sys
import yaml
from colorama import Fore

from engine.style import generar_ascii, limpiar


generar_ascii()
print()
print("Presiona ENTER para comenzar la configuración del programa.")
input()

# Configuración de filename
limpiar()
filename = input("""
CONFIGURANDO: Nombre del archivo final descargado.

    {canal} representa el nombre del canal del vídeo.
    {titulo} representa el nombre del vídeo.

Con el parámetro "[{canal}] {titulo}", el nombre del archivo sería:
[Rick Astley] Never Gonna Give You Up (Official Music Video - dQw4w9WgXcQ.mp3

El id del vídeo al final del nombre es necesario para que el programa pueda
comprobar las canciones que ya han sido descargadas.

> ("[{canal}] {titulo}" por defecto) """)

filename = filename if filename != "" else "[{canal}] {titulo}"

# Configuración de download_path
limpiar()
download_path = input("""
CONFIGURANDO: Ruta donde se descargarán las canciones.

En caso de no especificar ninguna las canciones de descargarán en "./downloads".

> """)

# Añadir la barra al final y eliminar las contrabarras.
download_path = "/".join(download_path.split("\\"))
if download_path != "":
    download_path += "/" if download_path[-1] != "/" else ""

# Configuración de default_url
limpiar()
default_url = input("""
CONFIGURANDO: Playlist por defecto.

Al especificar una URL podrás ejecutar el programa sin el parámetro de URL y
descargará los nuevos videos de la lista especificada.

Esto es útil para actualizar una lista que suelas escuchar.

> """)

# Configuración de cover_art
limpiar()
cover_art = input("""
CONFIGURANDO: Miniatura como portada de la canción.
Esta opción se encarga de que las canciones tengan portada o no
Al ser activada las canciones incluiran la metadata album con el formato
[{canal}] {titulo}.

> (Habilitado por defecto) (S/N) """)

if cover_art.lower() == "s":
    cover_art = True

elif cover_art.lower() == "n":
    cover_art = False

else:
    if cover_art != "":
        print(f"{Fore.RED}{cover_art} no es un valor valido.{Fore.RESET}")
        sys.exit()
    
    else:
        cover_art = True

# Configuración de workers
limpiar()
workers = input("""
CONFIGURANDO: Hilos de procesamiento por cada núcleo del procesador.

Al aumentarlo se disminuye el tiempo de descarga de varios vídeos, pero
aumenta el uso del procesador!

**********************************************************************************
* Si no estás seguro de que poner aquí simplemente presiona ENTER sin poner nada *
**********************************************************************************

> (4 por defecto) """)

# En caso de que se especifique algo que no sea un número el porgrama se
# detendra, salvo si hay una cadena vacia.
try:
    workers = int(workers)

except ValueError:
    if workers != "":
        print(f"{Fore.RED}{workers} no es un número valido.{Fore.RESET}")
        sys.exit()
    
    else:
        workers = 4

d = {
    'filename': filename, 
    'download_path': download_path,
    'default_url': default_url, 
    'cover_art': cover_art,
    'workers': workers
}

# Guardar la configuración.
limpiar()
with open("config/config.yaml", "w", encoding="utf-8") as f:
    yaml.dump(d, f)
    print(f"{Fore.GREEN}Se ha guardado la configuración correctamente.{Fore.RESET}")