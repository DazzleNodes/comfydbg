"""Rich console rendering for comfydbg output.

Provides formatted tables, panels, and status displays for:
  - Version comparison tables (version command)
  - Workflow fingerprint displays (detect command)
  - Bisect progress and results (bisect command)
  - Install operation status (install/skip/force/full commands)

Currently: Stub module. launcher.py uses print() directly.
Future: Migrate launcher.py output to Rich-based rendering with THAC0 gating.
"""

# TODO: Extract rendering from launcher.py and convert to Rich tables/panels
# The launcher currently uses plain print() with manual formatting.
# Rich would provide: colored tables, panels, progress bars, spinners.
