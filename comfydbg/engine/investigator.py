"""
ComfyUI environment investigator.

Orchestrates environment checks: pip packages, git state, custom nodes,
CUDA/torch availability, and workflow compatibility.

Future: Extract investigation logic from launcher.py cmd_version/cmd_detect.
"""


def run_investigation(comfyui_path=None):
    """Investigate the current ComfyUI installation state.

    Returns a dict with:
      - pip_packages: installed package versions
      - git_state: current branch/tag, dirty status
      - custom_nodes: list of installed nodes with versions
      - torch_cuda: CUDA availability and version info
      - mismatches: packages where installed != required
    """
    # TODO: Extract from launcher.py cmd_version + cmd_detect
    raise NotImplementedError("Will be extracted from launcher.py in v0.2.0")
