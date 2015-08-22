#!/bin/bash

if [ ! -f $HOME/miniconda/bin/conda ]; then
	echo "conda not found, installing now..."
	if [ ! -f $HOME/miniconda.sh ]; then
	    echo "Installer not found, downloading now..."
	    wget https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -O ~/miniconda.sh
		chmod +x ~/miniconda.sh
		bash ~/miniconda.sh -b -p $HOME/miniconda
	fi
fi

echo "Updating conda..."

export PATH="$HOME/miniconda/bin:$PATH"
conda update --yes conda
