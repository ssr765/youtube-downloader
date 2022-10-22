# youtube-downloader
Script para descargar varias canciones de YouTube mediante multiprocesamiento y YouTube-DL.
## Requisitos previos
Los requisitos para que el programa pueda funcionar son los siguientes.
- Python 3.7 o superior
- [ffmpeg](https://www.gyan.dev/ffmpeg/builds/) [*Tutorial para instalarlo*](https://youtu.be/bM8SIjjVnP0)
## Instalación
Antes de nada hay que instalar las librerías necesarias, para ello se puede usar el siguiente comando:
```
pip install -r requirements.txt
```
## Primeros pasos
Es recomendable antes de usar el programa usar el asistente de configuración configurar.py.
```
cd [carpeta del script]
python setup.py
```
Una vez configurado el programa, este funciona de la siguiente manera:
```
cd [carpeta del script]
python main.py [URL de la canción o playlist de YouTube]
```
No es necesario introducir una URL si se ha especificado una URL por defecto en la configuración, ya que entonces usará esa.

En caso de cualquier error puedes abrir una issue con todo el output del programa.
