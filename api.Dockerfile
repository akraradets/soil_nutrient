FROM python:3.10.13-bookworm

LABEL org.opencontainers.image.source https://github.com/akraradets/soil_nutrient
ARG BUILD_VERSION='local'
ENV BUILD_VERSION=${BUILD_VERSION}
# https://vsupalov.com/docker-arg-env-variable-guide/
# https://bobcares.com/blog/debian_frontendnoninteractive-docker/
ARG DEBIAN_FRONTEND=noninteractive
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Timezone
ENV TZ="Asia/Bangkok"
RUN apt clean 
RUN apt update && apt upgrade -y
# Set timezone
RUN apt install -y tzdata
RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone

# Set locales
# https://leimao.github.io/blog/Docker-Locale/
RUN apt-get install -y locales
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LC_ALL en_US.UTF-8 
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  


WORKDIR /root/projects
RUN pip3 install pip==23.3.1
RUN pip3 install mlflow==2.7.1 --default-timeout=1000
RUN pip3 install fastapi==0.104.0
RUN pip3 install "uvicorn[standard]"==0.23.2
RUN pip3 install python-multipart==0.0.6
RUN pip3 install torch==2.0.1+cu118 torchvision --index-url https://download.pytorch.org/whl/cu118

COPY ./api /root/projects

RUN apt-get clean && rm -rf /var/lib/apt/lists/*
CMD uvicorn main:app --reload --host=0.0.0.0 --port=80