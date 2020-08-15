#!/bin/bash
# install_fonts.bash
# Manages and installs my personal global systemwide font settings
# This isn't mean't to be a per system configuration, this is to be declared
# as a 'base' package and run for all system types

set -ex

if [ ! -d $HOME/.fonts ]; then
    mkdir $HOME/.fonts
fi
cd $HOME/.fonts

# Want to add a new custom font to the total global font install list?
# Add another JSON object entry in this list of configurations here,
# All keys must be supplied
font_cfg=$(cat <<-END
{
  "config": [
    {
        "url": "https://github.com/i-tu/Hasklig/releases/download/1.1/Hasklig-1.1.zip",
        "file": "Hasklig-1.1.zip",
        "uncompress": "zip"
    }
  ]
}
END
)

# If the static configuration above is incorrect or malformed, exit 1
echo "${font_cfg}" | jq '.' > /dev/null
if [ $? != 0 ]; then
    echo "Error: Custom font config is malformed JSON, edit and try again"
    exit 1
fi

# Loop through all configs, only call refresh cache if a new configuration
# has been detected
refresh_cache=false
for i in $(echo "${font_cfg}" | jq -r -c '.config | .[]'); do
    echo "I: $i"
    url=$(echo "$i" | jq -r '.url')
    file=$(echo "$i" | jq -r '.file')
    echo "Url: ${url}"
    echo "File: ${file}"
    if [ ! -f "${file}" ]; then
        wget -c "${url}"
        uncompress_method=$(echo "$i" | jq -r '.uncompress')
        if [ "${uncompress_method}" == "zip" ]; then
            unzip "${file}"
            refresh_cache=true
        else
            echo "Error: Unsupported uncompress method found: ${uncompress_method}"
            exit 1
        fi
    fi

done

if [ "${refresh_cache}" = true ]; then
    echo "Refreshing font-cache..."
    sudo fc-cache -fv
fi

