"""
LANZAR APLICACION CON EJECUTAR.py
registro.py
"""

import logging
import os

_RUTA_LOGS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
ARCHIVO_LOG = os.path.join(_RUTA_LOGS, "software_fj.log")


def obtener_logger(nombre: str = "SoftwareFJ") -> logging.Logger:

    """Devuelve un logger que escribe en archivo y consola,solo errores"""

    logger = logging.getLogger(nombre)
    if logger.handlers:        
        return logger

    logger.setLevel(logging.DEBUG)
    formato = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    try:
        os.makedirs(_RUTA_LOGS, exist_ok=True)
        archivo = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")
    except OSError as error:

        print(f"[AVISO] No se pudo abrir el archivo de logs: {error}")
    else:
        archivo.setLevel(logging.DEBUG)
        archivo.setFormatter(formato)
        logger.addHandler(archivo)
    finally:
        consola = logging.StreamHandler()
        consola.setLevel(logging.CRITICAL)  
        consola.setFormatter(formato)
        logger.addHandler(consola)

    return logger


logger = obtener_logger()
