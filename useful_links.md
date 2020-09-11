# Useful links

## Hibernation / Suspend

Fedora workstation doesn't support hibernation out of the box.
Also for some reason suspend isn't working properly on F32

https://www.ctrl.blog/entry/fedora-hibernate.html

## Grub theme

https://github.com/vinceliuice/grub2-themes

## Nvidia DRM

Sometimes `nvidia-drm.modeset=1` isn't enough. For example the splash screen on the main workstation was broken. Adding nvidia modules to the `initramfs` via `dracut` fixed this

https://wiki.archlinux.org/index.php/NVIDIA#DRM_kernel_mode_setting
https://forums.developer.nvidia.com/t/plymouth-f23-and-364-15/42272/7


