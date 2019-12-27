#!/usr/bin/python3
import hashlib
import base64
import json
from reimage.shell import run_oneline


def metascript(script_name, metaprogram, metadata, config):
    ms = """
#!/bin/bash
THIS_SCRIPT=%s
PROGRAM_MD5=%s
DATA_MD5=%s

# Parsing this will produce the pexified python program that will be invoked
beginning_of_program=$(grep -n BEGINNING_OF_PROGRAM $THIS_SCRIPT | tail -n1 | cut -f1 -d:)
beginning_of_program="$((beginning_of_program + 1))"
end_of_program=$(grep -n END_OF_PROGRAM $THIS_SCRIPT | tail -n1 | cut -f1 -d:)
program_difference="$((end_of_program - beginning_of_program))"

# Parsing this will produce the tarball that formentioned program needs
beginning_of_data=$(grep -n BEGINNING_OF_DATA $THIS_SCRIPT | tail -n1 | cut -f1 -d:)
beginning_of_data="$((beginning_of_data + 1))"
end_of_data=$(grep -n END_OF_DATA $THIS_SCRIPT | tail -n1 | cut -f1 -d:)
data_difference="$((end_of_data - beginning_of_data))"

# Parsing this will produce the config file that the program was loaded with
beginning_of_config=$(grep -n BEGINNING_OF_CONFIG $THIS_SCRIPT | tail -n1 | cut -f1 -d:)
beginning_of_config="$((beginning_of_config + 1))"
end_of_config=$(grep -n END_OF_CONFIG $THIS_SCRIPT | tail -n1 | cut -f1 -d:)
config_difference="$((end_of_config - beginning_of_config))"

echo "Beginning of Program: $beginning_of_program"
echo "End of Program: $end_of_program"
echo "Program Diff: $program_difference"
tail -n +$beginning_of_program $THIS_SCRIPT | head -n $program_difference | cut -c 3- | rev | cut -c 2- | rev | base64 --decode > reimage.pex

program_md5=$(md5sum reimage.pex | awk '{print $1}')
if [ "$PROGRAM_MD5" != "$program_md5" ]; then
  echo "Expected md5sum of actual program does not match actual... exiting: $program_md5"
  rm reimage.pex reimage_data.tar.gz
  exit 1
fi
echo "Python pex program verified, reimage.pex stored in current dir"
chmod u+x reimage.pex

echo "Beginning of data: $beginning_of_data"
echo "End of data: $end_of_data"
echo "Data Diff: $data_difference"
tail -n +$beginning_of_data $THIS_SCRIPT | head -n $data_difference | cut -c 3- | rev | cut -c 2- | rev | base64 --decode > reimage_data.tar.gz

data_md5=$(md5sum reimage_data.tar.gz | awk '{print $1}')
if [ "$DATA_MD5" != "$data_md5" ]; then
  echo "Expected md5sum of program data does not match actual... exiting: $data_md5"
  rm reimage.pex reimage_data.tar.gz
  exit 1
fi
echo "System data tarball verified, reimage_data.tar.gz stored in current dir"

tail -n +$beginning_of_config $THIS_SCRIPT | head -n $config_difference > reimage_config.cfg
echo "Config file printed... reimage_config.cfg"

./reimage.pex -c reimage_config.cfg unload -d reimage_data.tar.gz
# rm reimage.pex reimage_data.tar.gz

exit 0

BEGINNING_OF_CONFIG
%s
END_OF_CONFIG
BEGINNING_OF_PROGRAM
%s
END_OF_PROGRAM
BEGINNING_OF_DATA
%s
END_OF_DATA
"""

    program_md5 = hashlib.md5(metaprogram).hexdigest()
    data_md5 = hashlib.md5(metadata).hexdigest()

    return ms % (script_name, program_md5, data_md5, json.dumps(config),
                 base64.b64encode(metaprogram), base64.b64encode(metadata))
