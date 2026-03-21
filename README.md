# comfydbg

[![PyPI](https://img.shields.io/pypi/v/comfydbg?color=green)](https://pypi.org/project/comfydbg/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: GPL v3](https://img.shields.io/badge/license-GPL%20v3-green.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
[![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)](#requirements)

**ComfyUI startup manager, version detective, and troubleshooting toolkit.**

## The Problem

ComfyUI's package ecosystem moves fast. A `pip install -r requirements.txt` can silently upgrade your frontend, break your workflows, and leave you debugging version mismatches for hours. Custom nodes inject frontend JavaScript that can corrupt the canvas. And when something breaks, you're left manually bisecting through dozens of packages and nodes to find the culprit.

**comfydbg** gives you targeted package control, version fingerprinting from workflow images, and automated binary search for broken custom nodes.

## Quick Start

```bash
pip install comfydbg
```

Then from your ComfyUI directory:

```bash
# Start ComfyUI, skipping problematic frontend package
comfydbg

# Check what's installed vs what's required
comfydbg version

# Find which custom node is breaking your canvas
comfydbg bisect start
```

## Features

- **Targeted pip management**: Skip, force-reinstall, or rollback individual packages without touching the rest of your environment
- **Version rollback**: Step back through PyPI or GitHub release history with `-1`, `-2`, `-3` or `-HN N` (Nth from newest)
- **GitHub source install**: Install from GitHub releases when PyPI is broken, with automatic build recipes for non-standard packages (e.g., `comfyui-frontend-package`)
- **Workflow fingerprinting**: Extract version info embedded in ComfyUI output images (.png, .webp) -- shows frontend version, backend version, and custom node versions
- **Mismatch detection**: Compare workflow requirements against installed packages, flag what's changed
- **Custom node bisect**: Binary search through 60+ custom nodes in ~6 rounds to find which one is causing canvas corruption, crashes, or errors
- **Version comparison**: Side-by-side view of installed vs required versions with `[MISMATCH]` and `[MISSING]` flags

## Commands

```bash
# Startup (skip frontend, install rest, launch ComfyUI)
comfydbg                                           # default behavior
comfydbg skip pkg1 pkg2 -- --listen 0.0.0.0        # skip specific packages
comfydbg full                                      # install everything from requirements.txt
comfydbg full -F                                   # force-reinstall everything (nuclear option)
comfydbg force comfyui-frontend-package==1.39.19   # force specific version

# Package management with rollback
comfydbg install comfyui-frontend-package -1       # one version back from current
comfydbg install comfyui-frontend-package -HN 3    # 3rd from newest on PyPI
comfydbg install comfyui-frontend-package -G       # from GitHub release
comfydbg install comfyui-frontend-package -U -HN 5 # uninstall first, 5th from top

# Diagnostics
comfydbg version                                   # show key package versions
comfydbg version --all                             # all packages from requirements.txt
comfydbg detect output/my_image.webp               # workflow fingerprint from image
comfydbg detect workflow.json --save extracted.json # extract + save workflow

# Custom node bisect (find the broken node)
comfydbg bisect start                              # begin binary search
comfydbg bisect good                               # canvas works -> culprit in other half
comfydbg bisect bad                                # canvas broken -> culprit in this half
comfydbg bisect exclude soundflow                  # remove crashing node, continue
comfydbg bisect restore                            # put excluded nodes back
comfydbg bisect reset                              # clean up
```

For detailed parameter descriptions, see [docs/parameters.md](docs/parameters.md).

## How Bisect Works

Like `git bisect`, but for custom nodes. ComfyUI's `--whitelist-custom-nodes` flag lets us enable half the nodes at a time without moving files. Each round halves the candidate set:

```
Round 1: 63 nodes -> test 31  (good/bad?)
Round 2: 31 nodes -> test 15  (good/bad?)
Round 3: 15 nodes -> test 7   (good/bad?)
Round 4: 7 nodes  -> test 3   (good/bad?)
Round 5: 3 nodes  -> test 1   (good/bad?)
Round 6: Found it! -> smart-resolution-calc
```

If a node crashes ComfyUI on startup (e.g., `soxr` nanobind error), use `comfydbg bisect exclude <node>` to move it aside and continue.

## How Detect Works

ComfyUI embeds workflow metadata in output images. `comfydbg detect` extracts this and compares against your current install:

```
===========================================================================
  Workflow Version Fingerprint
  Source: 2026-03-20_06-41-48_qwen_1.webp
===========================================================================
  Backend:    0.15.1               Installed:       0.17.2  [MISMATCH]
  Frontend:   1.41.20              Installed:      1.39.19  [MISMATCH]

  Package                             Workflow         Installed        Status
  ----------------------------------- ---------------- ---------------- --------
  ComfyUI-GGUF                        cf0573351a       1.1.10           [CHANGED]
  RES4LYF                             7750bf7800       7750bf7800       [MATCH]
  comfyui_essentials                  1.1.0            1.1.0            [MATCH]
  rgthree-comfy                       1.0.2509092031   1.0.2509092031   [MATCH]

  Recovery suggestions:
    Backend:  git checkout v0.15.1
    Frontend: comfydbg force comfyui-frontend-package==1.41.20
===========================================================================
```

## Requirements

- **Windows 10 or 11** (ComfyUI is primarily Windows-based)
- **Python 3.10+**
- **ComfyUI** installed via git clone (not the standalone build)
- **gh CLI** optional (for GitHub release queries and bisect)

## Installation

```bash
# From PyPI
pip install comfydbg

# From source (development)
git clone https://github.com/djdarcy/comfydbg.git
cd comfydbg
pip install -e ".[dev]"
```

### As a begin.cmd replacement

Create a `comfydbg.cmd` in your ComfyUI directory:

```cmd
@echo off
call venv\scripts\activate
python -m comfydbg %*
```

Then use `comfydbg` instead of `begin` for all startup and package management.

## Roadmap

- [x] Targeted pip management (skip, force, install with rollback)
- [x] Version comparison and mismatch detection
- [x] Workflow fingerprinting from images (PNG, WebP)
- [x] Custom node bisect
- [x] GitHub release install with build recipes
- [ ] `comfydbg pin` / `comfydbg restore` -- snapshot and rollback working environments
- [ ] `comfydbg recover` -- auto-match workflow versions and install
- [ ] AI-enhanced diagnostics (dependency conflict explanation, crash analysis)
- [ ] Rich terminal output (tables, panels, progress bars)
- [ ] Cross-platform support (Linux, macOS)

See [ROADMAP.md](ROADMAP.md) for the full plan.

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

comfydbg, Copyright (C) 2026 Dustin Darcy

Licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html) (GPL-3.0) -- see [LICENSE](LICENSE)
