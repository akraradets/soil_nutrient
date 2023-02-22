FROM nvidia/cuda:11.7.0-cudnn8-devel-ubuntu22.04

# https://vsupalov.com/docker-arg-env-variable-guide/
# https://bobcares.com/blog/debian_frontendnoninteractive-docker/
ARG DEBIAN_FRONTEND=noninteractive
# Timezone
ENV TZ="Asia/Bangkok"

# like CD command in terminal. it will create directory if path is not existed

RUN apt update && apt upgrade -y
RUN apt install -y build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev curl \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
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

RUN apt install -y python3 python3-pip

RUN pip3 install ipykernel
RUN pip3 install ipywidgets
RUN pip3 install torch==1.13.1+cu117 --extra-index-url https://download.pytorch.org/whl/cu117
RUN pip3 install torchvision==0.14.1+cu117 --extra-index-url https://download.pytorch.org/whl/cu117
RUN pip3 install pandas
RUN pip3 install matplotlib
RUN pip3 install opencv-python

# RUN pip3 install torch
# RUN pip3 install torchvision==0.2.2.post3

CMD tail -f /dev/null