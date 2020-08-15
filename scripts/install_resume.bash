#!/bin/bash
set -ex

# For sleep/hibernate
echo 'add_dracutmodules+=" resume "' > /etc/dracut.conf.d/resume.conf

grep 'resume=' /etc/default/grub
if [ $? != 0 ]; then
   echo "Must edit /etc/default/grub to include the swap partition for hibernate to work"
fi

echo '#  This file is part of systemd.
#
#  systemd is free software; you can redistribute it and/or modify it
#  under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 2.1 of the License, or
#  (at your option) any later version.
#
# Entries in this file show the compile time defaults.
# You can change settings by editing this file.
# Defaults can be restored by simply deleting this file.
#
# See systemd-sleep.conf(5) for details

[Sleep]
AllowSuspend=yes
AllowHibernation=yes
#AllowSuspendThenHibernate=yes
#AllowHybridSleep=yes
#SuspendMode=
#SuspendState=mem standby freeze
#HibernateMode=platform shutdown
#HibernateState=disk
#HybridSleepMode=suspend platform shutdown
#HybridSleepState=disk
#HibernateDelaySec=180min
' > /etc/systemd/sleep.conf

# Nvidia specific - fixes splashscreen bug
echo 'add_drivers+=" nvidia nvidia_modeset nvidia_uvm nvidia_drm "
intall_items+=" /etc/modprobe.d/nvidia.conf "
' > /etc/dracut.conf.d/nvidia.conf

echo 'options nvidia_drm modeset=1' > /etc/modprobe.d/nvidia.conf

dracut -f
