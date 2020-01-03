#!/usr/bin/python3
import os
import sys
import logging
import argparse
import json
import reimage.load_configurator
import reimage.unload_configurator


def generate_options():
    parser = argparse.ArgumentParser(
        description='Personal installer/packager script')
    parser.add_argument(
        '-c',
        '--config_file',
        default="reimage.cfg",
        help="Master configuration file, needed for load command")
    subparsers = parser.add_subparsers(help="Choose the mode to run within",
                                       dest='command')
    load = subparsers.add_parser(
        'load', help="Wrap existing config with an installation script")
    unload = subparsers.add_parser(
        'unload', help="Take an existing config and unload it")
    unload.add_argument(
        '-d',
        '--data_tar',
        default="reimage_data.tar.gz",
        help="Tarball output of the load portion of this program")
    return parser


def load_config_file(config_file):
    config = None
    with open(config_file) as f:
        cfg = f.read()
        if cfg == None or cfg == "":
            raise Exception("Config file is empty")
        # Throws JSONDecodeError on malformed JSON
        config = json.loads(cfg)
    return config


def expand_path(config_file):
    if not os.path.isabs(config_file):
        return os.path.join(os.getcwd(), config_file)
    return config_file


def main():
    parser = generate_options()
    options, program_options = parser.parse_known_args()
    formatter = '%(levelname)s:%(asctime)s - %(filename)s:%(lineno)d] %(message)s'
    logging.basicConfig(stream=sys.stdout, level='DEBUG', format=formatter)

    if options.command is None:
        raise Exception("Missing command, choose load/store")

    config_file = expand_path(options.config_file)
    if not os.path.exists(config_file):
        raise Exception("Missing config file: %s" % config_file)
    config = load_config_file(config_file)

    if options.command == "load":
        reimage.load_configurator.perform_system_fetch(
            os.environ["HOME"], config["configuration_files"],
            config["configuration_directories"], config)
    elif options.command == "unload":
        if options.data_tar == "":
            raise Exception("Missing data_tar argument")
        reimage.unload_configurator.perform_system_restore(config, options.data_tar)

    print("Finished!")


if __name__ == '__main__':
    main()
