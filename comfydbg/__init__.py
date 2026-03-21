"""
comfydbg - ComfyUI startup manager, version detective, and troubleshooting toolkit.

Manages pip installs with package-level control, detects version mismatches
between workflows and installed packages, and isolates problematic custom nodes
via binary search.

Usage:
    comfydbg                        # default: skip problematic packages, launch ComfyUI
    comfydbg version                # show installed versions
    comfydbg detect image.webp      # extract workflow version fingerprint
    comfydbg bisect start           # find broken custom node
    comfydbg install pkg -HN 3      # install 3rd from newest on PyPI
"""

from ._version import __version__, get_version, get_base_version, VERSION, BASE_VERSION

__all__ = [
    "__version__",
    "get_version",
    "get_base_version",
    "VERSION",
    "BASE_VERSION",
]
