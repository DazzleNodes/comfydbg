"""comfydbg channel definitions for the THAC0 verbosity system.

This module defines the project-specific output channels. The THAC0 library
itself (comfydbg.lib.log_lib) is project-agnostic; channel names and
descriptions are registered here at the application layer.

Channels control which sections of output are visible at different
verbosity levels (-v, -Q, --show).
"""

# Channel name -> (description, default_level)
# Level: -2 = always, -1 = hidden at -QQ, 0 = default, 1 = verbose only
CHANNELS = {
    "version":  ("Package version comparisons", 0),
    "detect":   ("Workflow fingerprint details", 0),
    "bisect":   ("Bisect progress and history", 0),
    "install":  ("Package install operations", 0),
    "pip":      ("Pip command output", 1),
    "system":   ("System info (Python, CUDA, GPU)", 0),
    "progress": ("Spinners and progress indicators", 0),
    "hint":     ("Usage hints and suggestions", 0),
    "error":    ("Error messages", -2),
    "trace":    ("Debug trace output", 1),
    "general":  ("Uncategorized output", 0),
}
