FROM python:3.10-bookworm

# https://vsupalov.com/docker-arg-env-variable-guide/
# https://bobcares.com/blog/debian_frontendnoninteractive-docker/
ARG DEBIAN_FRONTEND=noninteractive
# Timezone
ENV TZ="Asia/Bangkok"

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
RUN pip3 install mlflow==2.7.1
RUN pip3 install fastapi==0.104.0
RUN pip3 install "uvicorn[standard]"==0.23.2

RUN apt-get clean && rm -rf /var/lib/apt/lists/*
CMD uvicorn main:app --reload --host=0.0.0.0 --port=80