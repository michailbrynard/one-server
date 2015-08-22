#!/bin/bash

# PYTHON
# --------------------------------------------------------------------------------------------------------------------#
export PATH=/home/canary/miniconda/bin:$PATH

if command -v conda >/dev/null 2>&1; then
	echo "Found anaconda..."
else
    wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O miniconda.sh
    chmod +x miniconda.sh
    ./miniconda.sh -b
fi

conda create --yes -n analytics python=3.4 ipython-notebook pip requests pandas matplotlib scipy xlrd openpyxl

source activate analytics



# Bash
# --------------------------------------------------------------------------------------------------------------------#
# https://github.com/takluyver/bash_kernel
git clone https://github.com/takluyver/bash_kernel.git


# R
# --------------------------------------------------------------------------------------------------------------------#
# https://github.com/takluyver/IRkernel

sudo add-apt-repository ppa:marutter/rrutter sudo apt-get update sudo apt-get install r-base r-base-dev

# Grabs your version of Ubuntu as a BASH variable
CODENAME=`grep CODENAME /etc/lsb-release | cut -c 18-`

# Appends the CRAN repository to your sources.list file 
sudo sh -c 'echo "deb http://cran.rstudio.com/bin/linux/ubuntu $CODENAME" >> /etc/apt/sources.list'

# Adds the CRAN GPG key, which is used to sign the R packages for security.
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9

sudo apt-get update
sudo apt-get install r-base r-dev

# Julia
# --------------------------------------------------------------------------------------------------------------------#
https://github.com/JuliaLang/IJulia.jl



# Ruby
# --------------------------------------------------------------------------------------------------------------------#
# https://www.digitalocean.com/community/tutorials/how-to-install-ruby-on-rails-on-ubuntu-12-04-lts-precise-pangolin-with-rvm
# https://github.com/minrk/iruby
# https://github.com/SciRuby/iruby
# https://github.com/liudangyi/iruby/tree/ipython3

sudo apt-get update
sudo apt-get install curl
sudo apt-get install ruby1.9.1-dev
#gpg --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3
command curl -sSL https://rvm.io/mpapis.asc | gpg --import -
\curl -L https://get.rvm.io | bash -s stable
source ~/.rvm/scripts/rvm
rvm requirements
rvm install ruby
rvm use ruby --default
rvm rubygems current

# gem install rails
#git clone git://github.com/minrk/iruby
#cd iruby
# build and install IRuby
#gem build iruby.gemspec
#gem install iruby-*.gem
gem isntall iruby
gem install pry pry-doc pry-theme pry-git awesome_print gruff rmagick gnuplot rubyvis

./bin/iruby register --force

# Haskell
# --------------------------------------------------------------------------------------------------------------------#
sudo apt-get update
sudo apt-get install -y software-properties-common
sudo add-apt-repository -y ppa:hvr/ghc
sudo apt-get update
sudo apt-get install -y cabal-install-1.20 ghc-7.8.4
cat >> ~/.bashrc <<EOF
export PATH="~/.cabal/bin:/opt/cabal/1.20/bin:/opt/ghc/7.8.4/bin:\$PATH"
EOF
export PATH=~/.cabal/bin:/opt/cabal/1.20/bin:/opt/ghc/7.8.4/bin:$PATH
cabal update
cabal install alex happy


# Node.js
# --------------------------------------------------------------------------------------------------------------------#



