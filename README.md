# reimage

```
usage: reimage.pex [-h] [-c CONFIG_FILE] {load,unload} ...

Personal installer/packager script

positional arguments:
  {load,unload}         Choose the mode to run within
    load                Wrap existing config with an installation script
    unload              Take an existing config and unload it

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config_file CONFIG_FILE
                        Master configuration file, needed for load command
```

Collects configurations and data and create a single installer script, complete with code and data needed to unpack everything on the host machine. Unpacking is as simple as running

```
./reimage.run
```

on the host machine. To pack up, run the program with the 'load' parameter, passing a configuration file. The configuration file gets checked into the public repo and determines what gets copied. 

```
{
  "meta_enable_fedora_workstation_repos": true,
  "meta_enable_rpm_fusion": true,
  "meta_additional_rpm_repos": [
    "https://download.docker.com/linux/fedora/docker-ce.repo"
  ],
  "meta_package_dependencies": [
    "grubby",
    "tmux",
    "htop",
    "zsh",
    "socat",
    "keychain",
    "curl",
    "dnf-plugins-core",
    "make",
    "ninja-build",
    "cmake",
    "google-chrome-stable"
  ],
  "meta_local_package_dependencies":[
    "$HOME/Downloads/brscan4-0.4.8-1.x86_64.rpm"
  ],
  "meta_python_pip_package_dependencies": [
    "krakenx"
  ],
  "meta_workspace_dir": "$HOME/workspace",
  "meta_installed_fonts": [
    "https://github.com/i-tu/Hasklig/releases/download/1.1/Hasklig-1.1.zip"
  ],
  "configuration_files": [
    "$HOME/workspace/.perforce",
    "$HOME/.tmux.agnoster-theme",
    "$HOME/.tmux.conf",
    "$HOME/.zshrc",
    "$HOME/.spacemacs",
    "$HOME/conky-manager.json",
    "/etc/systemd/system/krakenx-config.service"
  ],
  "configuration_directories" : [
    { "location": "$HOME/.ssh", "recurse": true, "ignore_patterns": ["sockets"] },
    { "location": "$HOME/.certs", "recurse": true }
  ],
  "configuration_init_scripts": [
    {
      "url":"https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh",
      "run_when": {
        "predicate": "not_exists",
        "item": "$HOME/.oh-my-zsh"
      }
    }
  ],
  "configuration_post_scripts": [
    {
      "url":"$HOME/.certs/install_certs.bash",
      "run_when": {
        "predicate": "is_empty",
        "item": "/etc/pki/ca-trust/source/anchors"
      }
    }
  ],
  "configuration_build_from_source": [
    {
      "package_name":"emacs-26.3",
      "package_location":"http://gnu.mirrors.pair.com/emacs/emacs-26.3.tar.gz",
      "package_dependencies": [
        "glibc-devel", "libjpeg-turbo-devel", "ncurses-devel", "libpng-devel",
        "libtiff-devel", "giflib-devel", "Xaw3d-devel", "zlib-devel", "libSM-devel",
        "libX11-devel", "libXext-devel", "libXi-devel", "libXmu-devel", "libXpm-devel",
        "libXrandr-devel", "libXt-devel", "libXtst-devel", "libXv-devel", "ccls",
        "gnutls-devel", "libXft-devel"
      ],
      "package_install_as_root": true
    }
  ],
  "configuration_git_repos": [
    { "repo": "https://github.com/syl20bnr/spacemacs", "at": "$HOME/.emacs.d" },
    "https://github.com/facebook/folly.git",
    "https://github.com/facebook/wangle"
  ]
}
```

### Explaination of run file

During the 'load' phase the configuration data, pexified version of the program, and master configuration is encoded and written at the end of the resulting unload bash script. They will be seperated by delimiters so that the bash script may parse itself and decode the resulting products. Once parsed and extracted, the script just can call this program (its decoded, extracted, pexified self) passing the data and configuration (also just extracted) as parameters.


### To package this pip repository w/ pex

```
# 0. Get pex
sudo pip install pex
# 1. Package
pex . -r requirements.txt -v -m reimage.reimage:main -o reimage.pex 
# 2. Run
./reimage.pex -c configs/reimage.cfg load
```
