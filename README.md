# reimage

Third attempt at making a program to install my programs and configs on a fresh installation of my choice.

## How to use

Firstly set a unique hostname for the new machine, if you already haven't, then run the installer script like so:

```
# Install all of the programs for your system type (i.e. hostname)

➜  reimage git:(feature/f32) ✗ ./run.bash -c cfgs/config.json

# Then unload the configs

➜  reimage git:(feature/f32) ✗ ./run.bash -c cfgs/config.json -u

```

### Useage

```
➜  reimage git:(feature/f32) ✗ ./run.bash -h
reimage - install my programs and configs on a common OS
Usage: ./run.bash -c (config_file) <file>
Optional args:
-u (unload)  Take locally edited config files and cp them into ./files
-l (load)   Take config files in ./files and cp them onto the system
For more information check out the README
```

There are three ways to use the script:
1. To install all programs (idmpotently) on a f32 installation
2. To just update the local configs with the ones from this repo (unload-mode)
3. To update the configs in this repo with what are installed locally (load-mode)

### Configuration files

All three modes must be supplied a configuration file via the `-c` command line parameter

A configuration file will look like the following:

```
{
    "programs" : [
        { "name": "emacs", "version": "28" },
        { "name": "conky", "version": "1.11.7" },
        {
            "name": "grub_theme",
            "version": "",
            "install_on": ["desktop"]
        }
    ],

    "files" : [
        { "from": "spacemacs", "to": "~/.spacemacs" },
        { "from": "conkyrc", "to": "/etc/conky/conkyrc" },
        { "from": "ssh_config", "to": "~/.ssh/config" }
    ],

    "classes" : ["laptop", "desktop", "nvidia_gpu"],

    "systems" : {
        "workstation" : ["desktop", "nvidia_gpu"],
        "p53-laptop" : ["laptop", "nvidia_gpu"],
        "x1c-laptop" : ["laptop"],
        "workstation-co" : ["desktop", "nvidia_gpu"]
    }
}

```

with keys for "programs", "files", "classes" and "systems". Classes are arbitrary attributes which can be attached to a system. A system is a one-to-one mapping with a personal machine for which will map to an actual `hostname`.
