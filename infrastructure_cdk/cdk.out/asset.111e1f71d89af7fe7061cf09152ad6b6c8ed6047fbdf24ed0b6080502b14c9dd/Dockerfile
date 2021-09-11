FROM ubuntu

ENV TZ=Etc/UCT
ENV DEBIAN_FRONTEND=noninteractive

# Install apache and remove the downloaded packages list from apt-get update command
RUN apt-get update -y && \
apt-get install -y apache2 && \
rm -r /var/lib/apt/list/*

# Copy the website in to apache web root dir
COPY webapp /var/www/html

EXPOSE 80

CMD ["apachectl", "-D", "FOREGROUND"]