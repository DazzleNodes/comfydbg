# Roadmap

## Phase 1: Foundation (current -- v0.1.x)

- [x] Targeted pip management (skip, force, install with rollback)
- [x] Multi-source package install (PyPI, GitHub git, GitHub wheel)
- [x] Build recipe system for non-standard packages
- [x] Version comparison and mismatch detection
- [x] Workflow fingerprinting from images (PNG, WebP) and JSON
- [x] Custom node bisect (binary search for broken nodes)
- [x] begin.cmd drop-in replacement
- [ ] `comfydbg pin` -- snapshot working environment (pip freeze + custom node git states)
- [ ] `comfydbg restore` -- rollback to pinned state
- [ ] Torch CUDA index URL handling in `full -F`

## Phase 2: Intelligence (v0.2.x)

- [ ] `comfydbg recover` -- auto-match workflow versions and install
- [ ] Rich terminal output (tables, panels, progress bars)
- [ ] Refactor launcher.py into engine/ modules
- [ ] Symlink handling integration (temp_renamer for git operations)
- [ ] comfy-core CNR version mapping (vs git tags)
- [ ] AI-enhanced diagnostics (dependency conflict explanation)

## Phase 3: Ecosystem (v0.3.x)

- [ ] VRAM analysis and GPU diagnostics (integrate rtx5090-gpu-tools patterns)
- [ ] Model validation and compatibility checking
- [ ] Custom node health dashboard
- [ ] Cross-platform support (Linux, macOS)
- [ ] HTML diagnostic reports

## Phase 4: Community (v0.4.x)

- [ ] ComfyUI Manager integration
- [ ] Shared version compatibility database
- [ ] Community-contributed build recipes
- [ ] CI/CD integration helpers
