
# Docker Container for Ubuntu 14.04 x64
# 
# This image builds on the zapgo/miniconda image to create a non-privilaged user
# and defines onbuild commands for specific webapps.
#
FROM kmaginary/base:miniconda
MAINTAINER JR Minnaar <jr.minnaar@gmail.com>

#
# Add a non-privilaged user
#
RUN adduser --disabled-password --gecos '' webapp && \
    chown -R webapp:webapp /home/webapp

USER webapp
ENV HOME /home/webapp
WORKDIR /home/webapp

#
# Onbuild commands
ONBUILD COPY environment.yml $HOME/
ONBUILD RUN conda env create
ONBUILD COPY . $HOME/
ONBUILD USER root
ONBUILD RUN chown -R webapp:webapp /home/webapp
ONBUILD USER webapp
