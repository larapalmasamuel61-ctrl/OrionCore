import requests
import json
from Config.user_config import cargar_configuracion

def analizar_con_ia(comando, resultado_docker):
    """
    Toma el comando ejecutado y su resultado, y pide a la IA que lo explique.
    Detecta automáticamente el proveedor (Groq, OpenAI, Ollama) y ajusta los
    parámetros (endpoint, modelo) de forma dinámica para evitar errores comunes de configuración.
    """
    config = cargar_configuracion()
    endpoint = config.get("endpoint", "").strip()
    api_key = config.get("api_key", "").strip()

    if not endpoint:
        return "ERROR: No hay un endpoint de IA configurado."

    # DETECCIÓN AUTOMÁTICA Y CORRECCIÓN DE CREDENCIALES/ENDPOINTS
    # Si el usuario tiene una clave de Groq (gsk_) pero configuró por error el endpoint de OpenAI
    if api_key.startswith("gsk_"):
        if "openai.com" in endpoint or not endpoint:
            endpoint = "https://api.groq.com/openai/v1"
        provider = "groq"
    elif api_key.startswith("sk-"):
        provider = "openai"
    elif "localhost" in endpoint or "127.0.0.1" in endpoint or "ollama" in endpoint:
        provider = "ollama"
    else:
        provider = "custom"

    # SELECCIÓN DINÁMICA DEL MODELO SEGÚN EL PROVEEDOR
    if provider == "groq":
        # Llama 3.3 70B es el modelo insignia actual de Groq para explicaciones complejas
        model = "llama-3.3-70b-versatile"
    elif provider == "openai":
        model = "gpt-4o-mini"
    elif provider == "ollama":
        model = "llama3"  # Modelo local estándar
    else:
        model = "llama3-70b-8192"  # Fallback genérico

    # CONSTRUIR EL PROMPT (Instrucción educativa estructurada para la IA)
    prompt = f"""
    Eres un instructor de ciberseguridad interactivo llamado VisionCore.
    Tu trabajo es explicar los resultados de los comandos ejecutados de forma breve, estructurada y en puntos clave.

    El comando ejecutado fue: {comando}
    El resultado obtenido del escaneo es:
    ---
    {resultado_docker}
    ---

    Genera una respuesta en español utilizando exactamente las siguientes etiquetas especiales al inicio de cada línea. Esto es fundamental para que el visualizador de la interfaz coloree cada sección correctamente:

    [TITULO] Descripción General
    [NORMAL] (Escribe una explicación breve de 1 o 2 líneas sobre qué hace el comando en general en redes).

    [TITULO] Parámetros Utilizados
    [PARAM] (Parámetro 1): (Explicación breve de qué hace, por ejemplo qué hace -sS, -sV, -O, etc. según corresponda).
    [PARAM] (Parámetro 2): (Explicación breve).

    [TITULO] Puntos Clave del Resultado
    [CLAVE] • (Punto clave 1 resumido: puertos abiertos y sus servicios/versiones detectados).
    [CLAVE] • (Punto clave 2 resumido: estado del host, vulnerabilidades o sistemas operativos si los hay).
    [CLAVE] • (Punto clave 3 resumido: otro detalle importante del escaneo).

    [TITULO] Lección de Aprendizaje
    [NORMAL] (Una explicación breve de 1 o 2 líneas sobre qué enseña este resultado a un estudiante de seguridad).

    REGLAS IMPORTANTES:
    1. Cada línea que generes DEBE empezar con una de las etiquetas: [TITULO], [PARAM], [CLAVE] o [NORMAL].
    2. Sé extremadamente conciso. Usa puntos clave breves en lugar de párrafos largos.
    3. No utilices negritas de markdown (**), encabezados de markdown (###), ni guiones de lista que no tengan etiqueta. Por ejemplo, en lugar de "- puerto 80", escribe "[CLAVE] • Puerto 80".
    """

    # PREPARAR LA PETICIÓN (Estándar OpenAI/Groq/Ollama)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Eres un experto en ciberseguridad y redes."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }

    try:
        # Hacemos la llamada al endpoint
        response = requests.post(f"{endpoint}/chat/completions", headers=headers, json=data, timeout=30)
        
        # Control de fallos defensivo: si el modelo insignia de Groq falla, intentamos con el modelo de 8B (más ligero)
        if response.status_code == 400 and provider == "groq" and model == "llama-3.3-70b-versatile":
            data["model"] = "llama-3.1-8b-instant"
            response = requests.post(f"{endpoint}/chat/completions", headers=headers, json=data, timeout=30)
            
        if response.status_code == 200:
            respuesta_json = response.json()
            return respuesta_json["choices"][0]["message"]["content"]
        else:
            return f"Error de la API ({provider}): {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error de conexión con la IA ({provider}): {str(e)}"