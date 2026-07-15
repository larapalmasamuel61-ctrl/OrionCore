import json
import os

# El archivo donde se guardará la configuración (en la raíz del proyecto)
CONFIG_FILE = "visioncore_config.json"

def cargar_configuracion():
    """Lee el archivo de configuración. Si no existe, devuelve valores vacíos."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {"api_key": "", "endpoint": ""}

def guardar_configuracion(api_key, endpoint):
    """Guarda la API Key y el Endpoint en el archivo JSON."""
    data = {"api_key": api_key, "endpoint": endpoint}
    with open(CONFIG_FILE, 'w') as f:
        json.dump(data, f, indent=4)