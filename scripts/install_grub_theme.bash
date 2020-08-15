#!/bin/bash
set -ex

if [ ! "grep GRUB_THEME= /etc/default/grub" &> /dev/null ]; then
    if [ ! -d $HOME/workspace/grub2-themes ]; then
        git clone git@github.com:vinceliuice/grub2-themes.git $HOME/workspace/grub2-themes
    fi
    cd $HOME/workspace/grub2-themes
    sudo ./install.sh -t -2
    sudo grub-mkconfig -o /boot/grub/grub.cfg
fi
