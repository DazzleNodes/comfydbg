"""Custom spinner themes for Rich console status indicators.

Each theme is a dict with 'interval' (ms) and 'frames' (list of single chars).
"""

# Spinner themes for different operations
THEMES = {
    "pip": {"interval": 100, "frames": list("/-\\|")},
    "pypi": {"interval": 80, "frames": list(".oOo")},
    "github": {"interval": 80, "frames": list(".oOo")},
    "bisect": {"interval": 120, "frames": list(">>=>")},
}
