# comfydbg Command Reference

## Startup Commands

### `comfydbg` (default)
Skip `comfyui-frontend-package`, install remaining requirements, launch ComfyUI.

### `comfydbg skip [PKG ...]`
Install requirements.txt excluding listed packages. Shows version comparison for skipped packages.

```cmd
comfydbg skip                                    # skip frontend
comfydbg skip comfyui-frontend-package torch     # skip multiple
comfydbg skip -- --listen 0.0.0.0                # pass args to main.py
```

### `comfydbg full [-F]`
Install all requirements.txt as-is. `-F` for force-reinstall (bypasses pip cache).

### `comfydbg force [PKG[==VER] ...]`
Uninstall then reinstall specified packages. Default: `comfyui-frontend-package`.

## Package Management

### `comfydbg install <PKG> [options]`
Install a single package with version rollback and source selection.

| Flag | Description |
|------|-------------|
| `-1`, `-2`, `-3` | Rollback N versions from current (shortcuts) |
| `-CN NUM` | Rollback NUM versions from currently installed |
| `-HN NUM` | Select NUMth from newest available (head) |
| `-G`, `--git` | Install from GitHub git tag |
| `-W`, `--wheel` | Install from GitHub release wheel assets |
| `-U`, `--uninstall` | Uninstall first (clears cached state) |

## Diagnostics

### `comfydbg version [--all] [PKG ...]`
Show ComfyUI version, git state, and package comparison.

### `comfydbg detect <FILE> [--save OUT]`
Extract workflow version fingerprint from image (.png, .webp) or .json file.

### `comfydbg bisect {start,good,bad,skip,exclude,restore,status,reset}`
Binary search for broken custom nodes. Typically 5-6 rounds for ~60 nodes.

See `comfydbg -h` and `comfydbg <command> -h` for full details.
