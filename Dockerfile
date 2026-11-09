# Imagen base Debian
FROM debian:bookworm-slim

# Evitar prompts interactivos durante la instalación
ENV DEBIAN_FRONTEND=noninteractive

# Instalar Java, Python 3, curl y utilidades necesarias
RUN apt-get update && apt-get install -y \
    openjdk-17-jdk-headless \
    python3 \
    python3-pip \
    curl \
    tar \
    && rm -rf /var/lib/apt/lists/*

# Descargar e instalar Hadoop (versión 3.3.6 standalone)
ENV HADOOP_VERSION=3.3.6
RUN curl -sL "https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz" | tar -xz -C /opt/ \
    && mv /opt/hadoop-${HADOOP_VERSION} /opt/hadoop

# Configurar variables de entorno requeridas
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV HADOOP_HOME=/opt/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Configurar JAVA_HOME dentro del script de configuración de Hadoop
RUN echo "export JAVA_HOME=${JAVA_HOME}" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh

# Directorio de trabajo
WORKDIR /app

# Comando por defecto para verificar la versión al arrancar
CMD ["hadoop", "version"]