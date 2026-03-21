"""
comfydbg.engine - Subprocess execution and data processing for ComfyUI operations.

Manages pip, git, and gh CLI interactions. Parses JSON responses from PyPI and GitHub APIs.

Future modules (to be extracted from launcher.py):
  pip_runner.py    - pip install/uninstall/show operations
  git_runner.py    - git/gh CLI operations
  pypi.py          - PyPI API version queries
  github.py        - GitHub release/tag queries
  recipes.py       - Build recipes for non-standard packages
"""
