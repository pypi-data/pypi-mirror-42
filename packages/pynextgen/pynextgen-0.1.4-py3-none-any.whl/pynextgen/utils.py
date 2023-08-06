"""
Utilities for pyNextGen
"""

import os
from multiprocessing import Pool
from pynextgen.logging_config import get_logger
import subprocess

logger = get_logger(__file__, __name__)


def apply_threads(func, arg_list, nthreads=1):
    """ Wrapper function to apply threads to a function
    """
    p = Pool(nthreads)
    p.starmap(func, arg_list)


def simplify_outpath(filename, prefix="", suffix="", keep_path=False, check_exist=True):
    """
    Produce a name for an output file
    """

    output_name = os.path.basename(filename)
    path = os.path.dirname(filename)

    # Remove all extensions
    output_name = os.path.splitext(output_name)[0]

    output_name = prefix + output_name + suffix

    if keep_path:
        output_name = os.path.join(path, output_name)

    if check_exist and os.path.exists(output_name):
        logger.error("File already exists: {}".format(output_name))
        raise IOError("File already exists: {}".format(output_name))

    return output_name


def exec_command(cmd, silent=False):
    """ Wrapper for proper execution of subprocesses
    """

    try:
        proc = subprocess.run(
            cmd,
            shell=True,
            check=True,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )
        if not silent and proc.stdout:
            logger.debug(proc.stdout.strip())

    except subprocess.CalledProcessError as exc:
        raise ChildProcessError(exc.stderr)
