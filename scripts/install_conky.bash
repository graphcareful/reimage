#!/bin/bash
# install_conky.bash
#

conky_config=$1
conky_version=$(echo "${conky_config}" | jq -r '.version')

function uninstall_conky {
    if type "dnf list installed conky" &> /dev/null; then
        # 1. emacs was installed via the package manager
        sudo dnf remove conky
        echo "conky has been uninstalled via dnf"
    elif [ -d $HOME/workspace/conky ]; then
        # 2. emacs was built from source in the workspace dir
        cd $HOME/workspace/conky
        sudo make uninstall
        echo "conky has been uninstalled via source install"
    else
        echo "Could not uninstall conky"
        exit 1
   fi
}

function setup_conky_env {
    sudo bash -c "echo \"[Desktop Entry]
=Application
Name=conky
Exec=conky --daemonize --pause=1
StartupNotify=false
Terminal=false
Icon=conky-logomark-violet
Categories=System;Monitor;\" > /usr/local/share/applications/conky.desktop"

    if [ ! -d /etc/conky ]; then
        sudo mkdir -p /etc/conky
    fi
    if [ ! -L /etc/conky/conky.conf ]; then
        cd /etc/conky
        echo "" > ~/.config/.conkyrc
        sudo ln -s ~/.config/.conkyrc conky.conf
    fi
}

function build_and_install_conky {
    local idir=$HOME/workspace/conky
    if [ ! -d "${idir}" ]; then
        git clone https://github.com/brndnmtthws/conky.git "${idir}"
    fi
    mkdir -p "${idir}/build"
    cd "${idir}/build"
    cmake ..
    make -j$(nproc)
    sudo make install
}

install="no"
if command -v conky &> /dev/null; then
    version=$(conky --version | head -n1 | awk '{print $2}')
    if [ "$version" != "${conky_version}" ]; then
        while true; do
            echo "Current conky version detected: ${version}"
            echo "conky version in config: ${conky_version}"
            read -p "Would you like to install the latest?" yn
            case $yn in
                [Yy]* ) uninstall_conky; install="yes; "break;;
                [Nn]* ) echo "upgrade denied... skipping"; break ;;
                * ) echo "Please answer yes or no.";;
            esac
        done
    fi
else
    install="yes"
fi

if [ "${install}" == "yes" ]; then
    sudo dnf install -y lua-devel imlib2-devel libcurl-devel
    build_and_install_conky
fi

setup_conky_env
