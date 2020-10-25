#!/bin/bash

function install_liquidctl {
    sudo dnf install libusb-devel && sudo pip install liquidctl
    sudo cat >/etc/systemd/system/liquidcfg.service <<EOL
[Unit]
Description=AIO startup service

[Service]
Type=oneshot
ExecStart=liquidctl --product 0x170e set pump speed 90
ExecStart=liquidctl --product 0x170e set fan speed  20 30  30 50  34 80  40 90  50 100
ExecStart=liquidctl --product 0x170e set ring color fading 350017 ff2608
ExecStart=liquidctl --product 0x170e set logo color spectrum-wave

[Install]
WantedBy=default.target
EOL

    sudo systemctl daemon-reload
    sudo systemctl start liquidcfg
    sudo systemctl enable liquidcfg
}

if [ ! -f /etc/systemd/system/liquidcfg.service ]; then
    echo "Installing liquidctl and its dependencies..."
    install_liquidctl
    echo "Finished installing liquidctl and its dependencies..."
fi
