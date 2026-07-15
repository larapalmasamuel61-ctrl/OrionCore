# Usamos Debian 13 Slim
FROM debian:13-slim

# Instalamos solo las herramientas de red (nada de fastfetch)
RUN apt update && apt install -y \
    nmap \
    iputils-ping \
    traceroute \
    dnsutils \
    iproute2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root

# Cuando el contenedor arranque, solo se quedará esperando comandos
CMD ["/bin/bash"]