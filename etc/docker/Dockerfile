FROM mini/base
RUN apk-install bzip2 

RUN wget http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
RUN chmod +x miniconda.sh \
    && bash ./miniconda.sh -b -p /opt/miniconda -f \
    && rm -f miniconda.sh
    && export PATH=/opt/miniconda/bin:$PATH \
    && conda update --yes conda \
    && conda install --yes ipython

ENV PATH /opt/miniconda/bin:$PATH

CMD ["ipython"]