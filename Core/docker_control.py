import docker

cliente = docker.from_env()

def ejecutar_comando_docker(comando_completo):
    """
    Toma el comando completo (ej: "nmap -sS 192.168.1.1") y lo ejecuta en el contenedor.
    """
    try:
        resultado = cliente.containers.run(
            "visioncore-lab",
            command=comando_completo,
            remove=True,
            network="host"
        )
        return resultado.decode("utf-8")
    except Exception as e:
        return f"Error al ejecutar el contenedor: {str(e)}"