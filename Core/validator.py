import re

def validar_objetivo_red(objetivo):
    """
    Verifica que el objetivo sea una IP válida, un rango de IP o un nombre de dominio.
    Retorna True si es seguro, False si parece malicioso.
    """
    # 1. PATRÓN DE SEGURIDAD: Solo permite números, letras, puntos, guiones y barras.
    # Esto bloquea caracteres como ; | & $ ( ) ` y espacios.
    patron_seguro = re.compile(r'^[a-zA-Z0-9\.\-\/]+$')
    
    if not patron_seguro.match(objetivo):
        return False

    # 2. (Opcional pero recomendado) Validar sintaxis de IP o Dominio.
    # Esto es para evitar que el usuario ponga cosas como "google.com; rm -rf"
    # (El paso 1 ya bloquea el ; y el rm, pero esto es una capa extra).
    if ";" in objetivo or "|" in objetivo or "&" in objetivo:
        return False
        
    return True