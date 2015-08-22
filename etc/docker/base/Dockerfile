# Docker Container for Ubuntu 14.04 x64
# 
# This container just takes a default ubuntu14.04
# and does some basic configuration common to all
# of the machines we deploy.  The idea here is to
# establish a baseline for all operations.
#
FROM ubuntu:latest
MAINTAINER JR Minnaar <jr.minnaar@gmail.com>

COPY . /usr/bin/

#
# Configure the machine (shell, apt, timezone, locale, etc.)
# These are just some basic configuration parameters we need
# to get started.
#
RUN ln -sf /bin/bash /bin/sh && \
    echo "deb http://archive.ubuntu.com/ubuntu trusty main universe" > /etc/apt/sources.list && \
    echo "Africa/Johannesburg" > /etc/timezone; dpkg-reconfigure --frontend noninteractive tzdata && \
    locale-gen en_US.UTF-8 && \
    export LANGUAGE=en_US.UTF-8; \
    export LANG=en_US.UTF-8; \
    export LC_ALL=en_US.UTF-8; \
    DEBIAN_FRONTEND=noninteractive dpkg-reconfigure locales

#
# Clean up some of the junk that comes in Linux that we just do not need
# Who needs a user 'games' for a server after all?
#
RUN for i in games news irc backup; do userdel -r $i &> /dev/null; done; \
    for i in disk dialout fax voice cdrom floppy tape audio backup operator; do groupdel $i &> /dev/null; done; \
    rm -rf /usr/games/ &> /dev/null; \
    rm -rf /usr/local/games &> /dev/null; \
    rm /etc/motd /etc/update-motd.d/* &> /dev/null; \
    exit 0

#
# Update the system and install software 
# packages.
#
RUN DEBIAN_FRONTEND=noninteractive \
    apt-get update && \
    apt-get install \
        ca-certificates \
        curl \
        htop \
        openssl \
        tree \
        vim \
        wget \
        -y --no-install-recommends && \
    apt-get autoremove -y && \
    apt-get clean -y && \
    apt-get autoclean -y && \
    rm -rf /var/lib/apt/lists/* 

CMD ["/bin/bash"]
