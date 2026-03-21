"""
Subprocess execution utilities for comfydbg.

Runs pip, git, and gh commands and parses their output.
Handles timeouts, error propagation, and JSON parsing.

Adapted from the wtf-restarted project's PowerShell runner pattern.
Future: Extract pip/git operations from launcher.py into this module.
"""

import subprocess
import sys
import json
from typing import Optional, Dict, Any


def run_command(cmd, timeout=30, capture=True, cwd=None):
    """Run a shell command and return the result.

    Args:
        cmd: Command as list of strings
        timeout: Timeout in seconds
        capture: If True, capture stdout/stderr
        cwd: Working directory

    Returns:
        subprocess.CompletedProcess, or dict with 'error' key on failure
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture,
            text=True,
            timeout=timeout,
            cwd=cwd,
        )
        return result
    except subprocess.TimeoutExpired:
        return {"error": f"Command timed out after {timeout}s: {' '.join(cmd)}"}
    except FileNotFoundError:
        return {"error": f"Command not found: {cmd[0]}"}
    except Exception as e:
        return {"error": f"Command failed: {e}"}


def run_pip(*pip_args, timeout=60):
    """Run a pip command using the current Python interpreter.

    Returns subprocess.CompletedProcess or error dict.
    """
    return run_command(
        [sys.executable, "-m", "pip"] + list(pip_args),
        timeout=timeout,
    )


def run_git(*git_args, timeout=15, cwd=None):
    """Run a git command.

    Returns subprocess.CompletedProcess or error dict.
    """
    return run_command(
        ["git"] + list(git_args),
        timeout=timeout,
        cwd=cwd,
    )


def run_gh(*gh_args, timeout=15):
    """Run a GitHub CLI command.

    Returns subprocess.CompletedProcess or error dict.
    """
    return run_command(
        ["gh"] + list(gh_args),
        timeout=timeout,
    )


def run_gh_json(*gh_args, timeout=15) -> Optional[Any]:
    """Run a GitHub CLI command and parse JSON output.

    Returns parsed JSON or None on failure.
    """
    result = run_gh(*gh_args, timeout=timeout)
    if isinstance(result, dict) and "error" in result:
        return None
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None
