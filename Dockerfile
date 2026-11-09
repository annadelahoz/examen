# Imagen base Debian
FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

# Instalar Java, Python 3, OpenSSH Server y utilidades necesarias
RUN apt-get update && apt-get install -y \
    openjdk-17-jdk-headless \
    python3 \
    python3-pip \
    openssh-server \
    curl \
    tar \
    && rm -rf /var/lib/apt/lists/*

# Descargar e instalar Hadoop
ENV HADOOP_VERSION=3.3.6
RUN curl -sL "https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz" | tar -xz -C /opt/ \
    && mv /opt/hadoop-${HADOOP_VERSION} /opt/hadoop

# Configurar variables de entorno
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV HADOOP_HOME=/opt/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

RUN echo "export JAVA_HOME=${JAVA_HOME}" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh

# Configuración de SSH (acceso por llave sin contraseña)
RUN ssh-keygen -t rsa -P '' -f /root/.ssh/id_rsa && \
    cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys && \
    chmod 0600 /root/.ssh/authorized_keys

# Script de arranque para iniciar el servicio SSH y mantener el contenedor vivo
RUN echo '#!/bin/bash\nservice ssh start\nexec "$@"' > /entrypoint.sh && \
    chmod +x /entrypoint.sh

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]