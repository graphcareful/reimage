#!/usr/bin/env python3

import subprocess
import sys
import re
import os
import logging
import getpass

logger = logging.getLogger('concord')
passwd = None

def run_subprocess(cmd,
                   my_stdout=sys.stdout,
                   my_stderr=sys.stderr,
                   my_env=os.environ.copy()):
    logger.debug("Running command: exec bash -c '%s'" % cmd)
    proc = subprocess.Popen(
        "exec bash -c '%s'" % cmd,
        stdout=my_stdout,
        stderr=my_stderr,
        env=my_env,
        shell=True,
    )
    return_code = 0
    try:
        return_code = proc.wait()
        sys.stdout.flush()
        sys.stderr.flush()
    except Exception as e:
        proc.kill()
        raise
    if return_code != 0:
        raise subprocess.CalledProcessError(return_code, cmd)


def _cleanup_whitespace(s):
    return re.sub(r'\s+', '', s)


def raw_check_output(cmd, quiet=False):
    stderr = sys.stderr if quiet is False else subprocess.STDOUT
    ret = subprocess.check_output(cmd, shell=True, stderr=stderr)
    if ret is None: return ret
    return str(ret.decode("utf-8"))


def run_oneline(cmd, quiet=False):
    logger.debug("run_oneline: %s", cmd)
    ret = raw_check_output(cmd, quiet)
    if ret is None: return ret
    return _cleanup_whitespace(ret)

def run_oneline_sudo(cmd, quiet=False):
    global passwd
    if passwd is None:
        passwd = getpass.getpass("[sudo] password for user: ")
    cmd = "echo %s | sudo -S %s" % (passwd, cmd)
    run_oneline(cmd)
