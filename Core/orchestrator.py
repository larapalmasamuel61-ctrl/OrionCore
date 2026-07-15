from Core.docker_control import ejecutar_comando_docker
from Core.ia_brain import analizar_con_ia
from Core.validator import validar_objetivo_red

def ejecutar_flujo_completo(comando_base, objetivo, max_intentos=2):
    """
    Orquestador principal.
    """
    # 1. VALIDACIÓN DE SEGURIDAD
    if not validar_objetivo_red(objetivo):
        return {
            "exito": False,
            "error": "SEGURIDAD: El objetivo contiene caracteres no permitidos.",
            "output_docker": "",
            "output_ia": ""
        }

    # 2. CONSTRUIR EL COMANDO FINAL
    comando_final = f"{comando_base} {objetivo}"
    
    # 3. EJECUTAR EN DOCKER (Le pasamos el comando completo)
    try:
        resultado_docker = ejecutar_comando_docker(comando_final)
    except Exception as e:
        return {
            "exito": False,
            "error": f"Error al ejecutar el contenedor: {str(e)}",
            "output_docker": "",
            "output_ia": ""
        }

    # 4. ANÁLISIS CON IA
    if resultado_docker and "Error" not in resultado_docker:
        try:
            resultado_ia = analizar_con_ia(comando_final, resultado_docker)
        except Exception as e:
            resultado_ia = f"Error al conectar con la IA: {str(e)}"
    else:
        resultado_ia = "La IA no pudo analizar el resultado porque el comando falló."

    return {
        "exito": True,
        "error": "",
        "output_docker": resultado_docker,
        "output_ia": resultado_ia
    }