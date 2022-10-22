import os
from colorama import Fore

def pintar(cadena, color) -> str:
    # Le pone color a una cadena.
    return f"{color}{cadena}{Fore.RESET}"

def limpiar():
    # Limpia la pantalla.
    os.system('cls') if os.name == 'nt' else os.system('clear')

def generar_ascii():
    # Genera un pequeño ASCII art con los datos del repositorio.
    limpiar()
    print("##############################################")
    print(f"#{pintar('YouTube Downloader'.center(44), Fore.MAGENTA)}#")
    print("##############################################")
    print(f"# {pintar('Desarrollado por:', Fore.MAGENTA)} ssr765{' '*19}#")
    print(f"# {pintar('GitHub:', Fore.MAGENTA)} https://github.com/ssr765{' '*10}#")
    print(f"# {pintar('Nombre del repositorio:', Fore.MAGENTA)} youtube-downloader #")
    print("##############################################")