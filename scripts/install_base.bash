#!/bin/bash
set -ex

function install_ppl {
    if type "dnf list installed powerpanel" &> /dev/null; then
       return
    fi
    echo "Installing 'powepanel rpm for integration with UPS..."
    power_panel="PPL-1.3.3-64bit.rpm"
    wget -c "https://dl4jz3rbrsfum.cloudfront.net/software/${power_panel}"
    sudo dnf install -y "${power_panel}"
    rm "${power_panel}"
}

function install_theme {
    if [ ! -f /usr/share/themes/Prof-Gnome/index.theme ]; then
        return
    fi
    echo "Installing Prof-Gnome theme..."
    git clone git@github.com:paullinuxthemer/Prof-Gnome.git $HOME/workspace/Prof-Gnome
    sudo mkdir /usr/share/themes/Prof-Gnome
    sudo cp -r $HOME/workspace/Prof-Gnome/* /usr/share/themes/Prof-Gnome
    sudo cat >/usr/share/themes/Prof-Gnome/index.theme <<EOL
[X-GNOME-Metatheme]
Encoding=UTF-8
GtkTheme=ProfGnome
IconTheme=ProfGnome
CursorTheme=ProfGnome
CursorSize=24
EOL
}


sudo dnf install -y \
     make \
     automake \
     gcc \
     gcc-c++ \
     kernel-devel

install_ppl
install_theme

if [ ! -d "$HOME/workspace" ]; then
    echo "Creating workspace dir..."
    mkdir $HOME/workspace
fi
