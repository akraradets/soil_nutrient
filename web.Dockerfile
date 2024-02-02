FROM php:7.4-apache-bullseye

COPY --from=composer:2 /usr/bin/composer /usr/bin/composer
LABEL org.opencontainers.image.source https://github.com/akraradets/soil_nutrient
ARG BUILD_VERSION='local'
ENV BUILD_VERSION=${BUILD_VERSION}
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
RUN docker-php-ext-install gd zip mysqli

RUN apt-get update && apt-get install -y \
    libfreetype6-dev \
    libjpeg62-turbo-dev \
    libpng-dev \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install -j$(nproc) gd

RUN a2enmod rewrite
# Use the default production configuration
RUN mv "$PHP_INI_DIR/php.ini-development" "$PHP_INI_DIR/php.ini"
# clean apt cache
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /var/www/html
COPY ./soid /var/www/html/
RUN rm /var/www/html/bk/config.php
RUN mv /var/www/html/bk/config_safe.php /var/www/html/config.php
RUN chown -R www-data:www-data /var/www
# ENV COMPOSER_ALLOW_SUPERUSER=1
USER www-data
RUN composer install 

COPY ./compose_soid_overwrite/InitialAvatar.php /var/www/html/vendor/lasserafn/php-initial-avatar-generator/src/InitialAvatar.php
EXPOSE 80




# CMD tail -f /dev/null
CMD ["/usr/sbin/apachectl", "-D", "FOREGROUND"]