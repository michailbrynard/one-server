# Docker Container for RabbitMQ
# 
# This image builds on the zapgo/base image and install miniconda
#
FROM zapgo/base
MAINTAINER JR Minnaar <jr.minnaar@gmail.com>

# Install RabbitMQ
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys F7B8CEA6056E8E56 && \
    echo "deb http://www.rabbitmq.com/debian/ testing main" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y rabbitmq-server pwgen && \
    rabbitmq-plugins enable rabbitmq_management && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Erlang cookie
RUN echo "ERLANGCOOKIE" > /var/lib/rabbitmq/.erlang.cookie && \
    chown rabbitmq:rabbitmq /var/lib/rabbitmq/.erlang.cookie && \
    chmod 400 /var/lib/rabbitmq/.erlang.cookie

# Add scripts
COPY run.sh /run.sh
COPY set_rabbitmq_password.sh /set_rabbitmq_password.sh
RUN chmod 755 ./*.sh

EXPOSE 5672 15672
CMD ["/run.sh"]
