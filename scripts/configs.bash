#!/bin/bash
# configs.bash
# Loads or unloads a configuration
# Public methods are load and unload, they expect a raw configuration as argument 1
# Or call go_configs, passing the string "load" or "unload" as parameter 2

# returns all json objects inside of "programs" for which contain a "config" key
# ex: {"from":"spacemacs","to":"~/.spacemacs"}
#     {"from":"conkyrc","to":"/etc/conky/conkyrc"}

function config_files {
    local config=$1
    cfgs=$(cat "${config}" | jq -c -r '.files | .[]')
    echo "${cfgs}"
}

function copy {
    local from=$1
    local to=$2
    local permissions=$3
    local is_root=$(ls -ld "${to}" | awk '{print $3}')
    cmd="cp ${from} ${to}"
    if [ "${is_root}" == "root" ]; then
        cmd="sudo ${cmd}"
    fi
    if eval ${cmd}; then
        echo "Copied file '${from}' to '${to}'"
    fi
    if [ "${permissions}" != "null" ]; then
        sudo chmod "${permissions}" "${to}"
    fi
}

# Iterate over the from/to json object tuple, either copying file onto system
# or copying the file locally into ./file from the system, depending on param 2 switch
function itr_configs {
    local config=$1
    local action=$2
    local cfgs=$(config_files $config)
    for item in $cfgs; do
        local from="$root/files/$(echo ${item} | jq -r '.from')"
        local orig_to=$(echo "${item}" | jq -r '.to')
        local permissions=$(echo "${item}" | jq -r '.permissions')
        local to=$(echo "${orig_to}" | sed "s#^~#$HOME#")
        if [ "${action}" == "unload" ]; then
            if [ ! -f "${from}" ]; then
                echo "Warning: Source file missing: ${from}, skipping"
                continue
            fi
            if [ ! -d "$(dirname $to)" ]; then
                if [[ $to == /* ]]; then
                    sudo mkdir "$(dirname $to)"
                else
                    mkdir "$(dirname $to)"
                fi
                echo "Creating directory $(dirname $to)"
            fi
            copy "${from}" "${to}" "${permissions}"
        elif [ "${action}" == "load" ]; then
            if [ ! -f "${from}" ]; then
                echo "Warning: Source file missing: ${from}"
            fi
            copy "${to}" "${from}" "${permissions}"
        else
            echo "Unsupported itr_config action, either 'unload' or 'load"
            exit 1
        fi
    done
}

function unload {
    itr_configs $1 "unload"
    echo "Configs unloaded onto system"
}

function load {
    itr_configs $1 "load"
    echo "Local configs loaded, changes..."
    cd $root
    git status
}

# If second paramter is "load" the load function is called, then exit
# If second parameter is "unload" the unload functio is called, then exit
# Otherwise report error and exit 1
function go_configs {
    if [ $2 == "load" ]; then
        load $1
    elif [ $2 == "unload" ]; then
        unload $1
    else
        echo "Error: go_configs only takes unload/load as a switch"
    fi
}
