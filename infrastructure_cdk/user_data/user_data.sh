#!/bin/bash
# Install Apache web server and PHP
yum install -y httpd git
# Download lab files
git clone https://github.com/ps-interactive/lab_aws_implement-auto-scaling-amazon-ecs
rm -rf /var/www/html/*
mv lab_aws_implement-auto-scaling-amazon-ecs/webapp/* /var/www/html/
# Turn on webserver
chkconfig httpd on
service httpd start