"""
Command-line interface for comfydbg.

ComfyUI startup manager, version detective, and troubleshooting toolkit.

Usage:
    comfydbg                                      # default: skip + launch
    comfydbg skip [pkg1 pkg2 ...] [-- main args]  # exclude packages
    comfydbg full [-F]                            # install all requirements
    comfydbg force [pkg[==ver] ...]               # uninstall/reinstall
    comfydbg install <pkg> [-CN N] [-HN N] [-G] [-W] [-U]
    comfydbg version [--all] [pkg]                # show versions
    comfydbg detect <file> [--save out.json]      # workflow fingerprint
    comfydbg bisect {start,good,bad,skip,exclude,restore,status,reset}
"""

import sys

# For now, delegate directly to the launcher module which contains all the
# working logic from the begin_launcher.py development session.
# TODO: Refactor launcher.py into proper submodules under engine/, output/, etc.
from .launcher import main as launcher_main


def main(argv=None):
    """Entry point for comfydbg CLI."""
    if argv is not None:
        sys.argv = ["comfydbg"] + list(argv)
    rc = launcher_main()
    sys.exit(rc or 0)


if __name__ == "__main__":
    main()
