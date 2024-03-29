#!/bin/bash
# install_emacs.bash
#
# Installs my custom emacs build on this machine, using the lastest version
# of emacs from the desired branch. Ensures all needed deps are needed to
# build this particular branch from source.
#
# Also does not attempt to re-install if previous installation is already
# detected, unless a major vesion change is detected, in this case the user
# is prompted before updating

emacs_config=$1
emacs_version=$(echo "${emacs_config}" | jq -r '.version')

function uninstall_emacs {
    if type "dnf list installed emacs" &> /dev/null; then
        # 1. emacs was installed via the package manager
        sudo dnf remove emacs
        echo "emacs has been uninstalled via dnf"
    elif [ -d $HOME/workspace/emacs ]; then
        # 2. emacs was built from source in the workspace dir
        cd $HOME/workspace/emacs
        sudo make uninstall
        echo "emacs has been uninstalled via source install"
    else
        echo "Could not uninstall emacs"
        exit 1
    fi
}

function install_emacs_deps {
    echo "Downloading emacs build dependencies..."

    sudo dnf install -y \
         gtk3-devel \
         libjpeg-devel \
         libXpm-devel \
         giflib-devel \
         libtiff-devel \
         gnutls-devel \
         texinfo \
         ncurses-devel

    # Additional libraries must exist for custom options enabled below to work
    sudo dnf install -y \
         jansson-devel \
         libgccjit-devel \
         libXft-devel \
         cairo-devel \
         harfbuzz-devel \
         libotf-devel \
         librsvg2-devel

    # Email utilities
    sudo dnf install -y \
         maildir-utils \
         gnutls-utils \
         offlineimap

    # Language server goodies
    sudo dnf install npm ShellCheck
    sudo npm install -g vscode-json-languageserver bash-language-server
    sudo pip install cmake-language-server bashate


    # Mu setup one time only
    if [ ! -d $HOME/Maildir ]; then
        mkdir $HOME/Maildir
        mu init --my-address=rob@vectorized.io --muhome=$HOME/Maildir
        mu mkdir $HOME/Maildir/queue
    fi
}

function build_and_install_emacs {
    cd $HOME/workspace/emacs
    git checkout feature/native-comp
    echo "Building emacs"
    ./autogen.sh
    ./configure --with-native-compilation --with-mailutils --with-json --with-cairo --with-rsvg --with-modules
    make -j$(nproc)
    echo "Installing emacs"
    sudo make install
}

# Check to see if emacs is already installed
# If it is, check the version
# 1. If the version is lower by a major number, prompt user to upgrade
# 2. If yes, uninstall previous version
# 3. Continue as normal, otherwise exit if user responded no
install="no"
if command -v emacs &> /dev/null; then
    version=$(emacs --version | head -n1 | awk '{print $3}')
    maj=$(echo "${version}" | cut -d. -f1)
    if [ $maj -lt "${emacs_version}" ]; then
        while true; do
            echo "Current emacs version detected: ${version}"
            read -p "Would you like to upgrade to ${emacs_version}?" yn
            case $yn in
                [Yy]* ) uninstall_emacs; install="yes; "break;;
                [Nn]* ) echo "emacs already installed... skipping"; break ;;
                * ) echo "Please answer yes or no.";;
            esac
        done
    fi
else
    install=yes
fi

if [ "${install}" == "yes" ]; then
    if [ ! -d $HOME/workspace/emacs ]; then
        git clone https://github.com/emacs-mirror/emacs.git $HOME/workspace/emacs
    fi
    install_emacs_deps
    build_and_install_emacs
    if [ ! -d $HOME/.emacs ]; then
        git clone https://github.com/syl20bnr/spacemacs $HOME/.emacs.d
        cd $HOME/.emacs.d
        git checkout develop
        cd $HOME/.emacs/.d/private/local
        git clone git@github.com:seanfarley/mu4e-patch.git
    fi
fi
