FROM php:8.2-apache-bookworm
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

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

RUN apt install -y libzip-dev libpng-dev unzip
RUN docker-php-ext-install gd zip

WORKDIR /var/www/html
# RUN composer install 

CMD tail -f /dev/null