#!/bin/bash

set -ex
config=""
action="none"
hostname=$(hostname)
root=$(git rev-parse --show-toplevel)

function install_script_deps {
    sudo dnf install -y redhat-lsb-core jq
}

function help_msg {
    echo "reimage - install my programs and configs on a common OS"
    echo "Usage: ./install.bash -c (config_file) <file>"
    echo "Optional args:"
    echo "-u (unload)  Take locally edited config files and cp them into ./files"
    echo "-l (load)   Take config files in ./files and cp them onto the system"
    echo "For more information check out the README"
    echo ""
}

function validate_input {
    local config=$1
    if [ "${config}" == "" ]; then
        echo "Error: Config file parameter cannot be empty"
        exit 1
    elif [ ! -f "${config}" ]; then
        echo "Error: Config file does not exist: ${config}"
        exit 1
    fi
    cat "${config}" | jq '.' > /dev/null
    if [ $? -ne 0 ]; then
        echo "Error: Config file not formatted as proper JSON"
        exit 1
    fi
}

function validate_systems {
    local config=$1
    # ensure current hostname exists in the list of hostnames
    hostnames=$(cat "${config}" | jq '.systems | keys | .[]')
    if [[ ! "${hostnames[@]}" =~ "${hostname}" ]]; then
        echo "Current machine hostname '${hostname} doesn't exist in config"
        exit 1
    fi
    # ensure all values are proper define classes
    classes=$(cat "${config}" | jq '.classes | .[]')
    class_options=$(cat "${config}" | jq '.systems | .[] | .[]')
    for selection in $class_options; do
        if [[ ! "${classes[@]}" =~ "${selection}" ]]; then
           echo "${selection} not one of the listed classes in classes"
           exit 1
        fi
    done
    # insure all 'install_on' values are known classes
    install_ons=$(cat "${config}" | jq --compact-output '.programs | .[] | select( .install_on ) | .install_on | .[]')
    for ins in $install_ons; do
        if [[ ! "${classes[@]}" =~ "${ins}" ]]; then
            echo "${ins} within 'install_on' is not a valid class"
            exit 1
        fi
    done
}

function install {
    local script_name=$1
    local prg_config=$2
    echo "Running script: ${root}/scripts/install_${script_name}.bash"
    echo "With argument: ${prg_config}"
    ${root}/scripts/install_${script_name}.bash "${prg_config}"
}

function parse_cmd_args {
    while getopts 'ulhc:' OPTION; do
        case "$OPTION" in
            u) action="unload"
               ;;
            l) action="load"
               ;;
            h) help_msg
               exit 0
               ;;
            c) config="$OPTARG"
               ;;
            ?)
            help_msg
            exit 1
            ;;
        esac
    done
    shift "$(($OPTIND -1))"
}

parse_cmd_args $@
install_script_deps
validate_input "$config"

sysinfo=$(lsb_release -a)
system="${hostname}"
all_classes=$(cat "${config}" | jq '.classes | .[]')
this_classes=$(cat "${config}" | jq -r -c ".systems[\"${system}\"] | .[]")
core_routines=(base fonts)
defined_routines=($(cat "${config}" | jq -r -c '.programs | .[] | .name'))
all_routines=("${core_routines[@]}" "${defined_routines[@]}")

echo "Bootstrapping system ${sysinfo}"
echo "Configuration file: ${config}"
echo "System: ${system}"
echo "Action: ${action}"

validate_systems "$config"
if [ "${action}" != "none" ]; then
    source $root/scripts/configs.bash
    echo "Not installing anything, in load/unload mode"
    go_configs $config $action
    exit 0
fi

# echo "core_routines: ${core_routines[@]}"
# echo "defined_routines: ${defined_routines[@]}"
# echo "All routines: ${all_routines[@]}"
# echo "Classes to install: ${this_classes}"

for routine in "${all_routines[@]}"; do
    obj=$(cat "${config}" | jq ".programs | .[] | select( .name | contains(\"${routine}\"))")
    if [ "${obj}" == "" ]; then
        echo "Installing base routine: ${routine}"
        install "${routine}" "null"
    else
        ins_on=$(echo "${obj}" | jq '.install_on')
        if [ "${ins_on}" == "null" ]; then
            echo "Installing non-base routine due to no 'install_on' directive: ${routine}"
            install "${routine}" "${obj}"
        else
            ins_on_arr=$(echo $ins_on | jq '.[]')
            for item in $ins_on_arr; do
                echo "Checking ${item}"
                if [[ "${this_classes[@]}" =~ "${item}" ]]; then
                    install "${routine}" "${obj}"
                elif [[ ! "${all_classes[@]}" =~ "${item}" ]]; then
                    echo "assertion failed: item $item is not a valid class.. exiting"
                    exit 1
                fi
            done
        fi
    fi
done
