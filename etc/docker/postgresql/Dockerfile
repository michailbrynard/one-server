# Docker Container for Ubuntu 14.04 x64
# 
# This image builds on the zapgo/base image and install miniconda
#
FROM zapgo/base
MAINTAINER JR Minnaar <jr.minnaar@gmail.com>

#
# Install miniconda for python virtual environements package manageement
#
RUN wget http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh \ 
    && chmod +x miniconda.sh \
    && ./miniconda.sh -b -p /opt/miniconda -f \
    && export PATH=/opt/miniconda/bin:$PATH \
    && conda update --yes conda \

ENV PATH=/opt/miniconda/bin:$PATH
