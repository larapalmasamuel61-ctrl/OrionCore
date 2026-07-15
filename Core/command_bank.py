# Diccionario con los comandos organizados por niveles de aprendizaje
COMANDOS_DISPONIBLES = [
    # --- NIVEL 1: RECONOCIMIENTO BÁSICO (🟢) ---
    {"nivel": "Basico", "nombre": "Ping básico (Enviar 4 paquetes)", "comando": "ping -c 4"},
    {"nivel": "Basico", "nombre": "Escaneo de red local (Ping sweep)", "comando": "nmap -sn"},
    {"nivel": "Basico", "nombre": "Escaneo rápido de puertos comunes", "comando": "nmap --top-ports 100"},
    {"nivel": "Basico", "nombre": "Búsqueda DNS inversa", "comando": "nmap -R -sn"},
    {"nivel": "Basico", "nombre": "Trazar ruta de red (Traceroute)", "comando": "traceroute"},

    # --- NIVEL 2: ENUMERACIÓN INTERMEDIA (🟡) ---
    {"nivel": "Intermedio", "nombre": "Escaneo simple de puertos (TCP SYN)", "comando": "nmap -sS"},
    {"nivel": "Intermedio", "nombre": "Detección de versiones de servicios", "comando": "nmap -sV"},
    {"nivel": "Intermedio", "nombre": "Escaneo de puertos estándar (Web/SSH)", "comando": "nmap -p 80,443,22"},
    {"nivel": "Intermedio", "nombre": "Escaneo rápido temporizado (T4)", "comando": "nmap -F -T4"},
    {"nivel": "Intermedio", "nombre": "Escaneo de puertos UDP comunes", "comando": "nmap -sU --top-ports 20"},

    # --- NIVEL 3: AUDITORÍA AVANZADA (🔴) ---
    {"nivel": "Avanzado", "nombre": "Detección profunda de SO y servicios", "comando": "nmap -sV -O"},
    {"nivel": "Avanzado", "nombre": "Escaneo de todos los puertos (1-65535)", "comando": "nmap -p-"},
    {"nivel": "Avanzado", "nombre": "Escaneo con scripts vulnerables (NSE)", "comando": "nmap -sC"},
    {"nivel": "Avanzado", "nombre": "Escaneo sigiloso evasivo (T1)", "comando": "nmap -sS -T1"},
    {"nivel": "Avanzado", "nombre": "Detección de firewalls (TCP ACK)", "comando": "nmap -sA"}
]