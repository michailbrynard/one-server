# Docker Container for Ubuntu 14.04 x64
# 
# This image builds on the zapgo/base image and install miniconda
#
FROM kmaginary/base:base
MAINTAINER JR Minnaar <jr.minnaar@gmail.com>

#
# Install miniconda for python virtual environements package manageement
#
RUN wget http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh 
RUN chmod +x miniconda.sh \
    && bash ./miniconda.sh -b -p /opt/miniconda -f \
    && export PATH=/opt/miniconda/bin:$PATH \
    && conda update --yes conda \
    && conda install --yes ipython \
    && rm -f miniconda.sh

ENV PATH=/opt/miniconda/bin:$PATH

CMD ["ipython"]
