"""Tests for comfydbg CLI and launcher."""

import os
import pytest
from pathlib import Path
from comfydbg.launcher import (
    parse_requirements,
    normalize_name,
    parse_pkg_arg,
    build_parser,
    _requirements_file,
    _bisect_state_file,
    _custom_nodes_dir,
    _bisect_disabled_dir,
)


class TestNormalizeName:
    def test_basic(self):
        assert normalize_name("comfyui-frontend-package") == "comfyui-frontend-package"

    def test_underscores(self):
        assert normalize_name("comfyui_frontend_package") == "comfyui-frontend-package"

    def test_dots(self):
        assert normalize_name("some.package.name") == "some-package-name"

    def test_mixed(self):
        assert normalize_name("Some_Package.Name") == "some-package-name"

    def test_case(self):
        assert normalize_name("PyYAML") == "pyyaml"


class TestParsePkgArg:
    def test_bare_name(self):
        name, version, orig = parse_pkg_arg("torch")
        assert name == "torch"
        assert version is None

    def test_pinned_version(self):
        name, version, orig = parse_pkg_arg("torch==2.7.0")
        assert name == "torch"
        assert version == "==2.7.0"

    def test_invalid(self):
        name, version, orig = parse_pkg_arg("---invalid")
        assert name is None


class TestParseRequirements:
    def test_basic(self, tmp_requirements):
        reqs = parse_requirements(tmp_requirements)
        assert "comfyui-frontend-package" in reqs
        assert reqs["comfyui-frontend-package"] == "comfyui-frontend-package==1.41.20"
        assert "torch" in reqs
        assert "numpy" in reqs
        assert "pillow" in reqs

    def test_skips_comments(self, tmp_path):
        req_file = tmp_path / "requirements.txt"
        req_file.write_text("# comment\ntorch\n#another\nnumpy\n")
        reqs = parse_requirements(req_file)
        assert len(reqs) == 2
        assert "torch" in reqs

    def test_skips_empty_lines(self, tmp_path):
        req_file = tmp_path / "requirements.txt"
        req_file.write_text("torch\n\n\nnumpy\n")
        reqs = parse_requirements(req_file)
        assert len(reqs) == 2


class TestBuildParser:
    def test_help(self):
        parser = build_parser()
        assert parser.prog == "comfydbg"

    def test_subcommands_exist(self):
        parser = build_parser()
        # These should parse without error
        for cmd in ["skip", "full", "force", "version", "detect", "bisect"]:
            # bisect needs an action
            if cmd == "bisect":
                ns = parser.parse_args(["bisect", "status"])
            elif cmd == "detect":
                ns = parser.parse_args(["detect", "test.json"])
            elif cmd == "install":
                ns = parser.parse_args(["install", "torch"])
            else:
                ns = parser.parse_args([cmd])
            assert ns is not None


class TestVersionCommand:
    def test_version_flag(self):
        """--version should not crash (may not be set up yet)."""
        parser = build_parser()
        # version subcommand, not --version flag
        ns = parser.parse_args(["version"])
        assert hasattr(ns, "func")

    def test_version_all(self):
        parser = build_parser()
        ns = parser.parse_args(["version", "--all"])
        assert ns.all is True

    def test_version_specific_pkg(self):
        parser = build_parser()
        ns = parser.parse_args(["version", "torch"])
        assert ns.packages == ["torch"]


class TestInstallParser:
    def test_rollback_shortcuts(self):
        parser = build_parser()
        ns = parser.parse_args(["install", "pkg", "-1"])
        assert ns.current_nth == 1

    def test_current_nth(self):
        parser = build_parser()
        ns = parser.parse_args(["install", "pkg", "-CN", "5"])
        assert ns.current_nth == 5

    def test_head_nth(self):
        parser = build_parser()
        ns = parser.parse_args(["install", "pkg", "-HN", "3"])
        assert ns.head_nth == 3

    def test_git_flag(self):
        parser = build_parser()
        ns = parser.parse_args(["install", "pkg", "-G"])
        assert ns.git is True

    def test_wheel_flag(self):
        parser = build_parser()
        ns = parser.parse_args(["install", "pkg", "-W"])
        assert ns.wheel is True

    def test_uninstall_flag(self):
        parser = build_parser()
        ns = parser.parse_args(["install", "pkg", "-U"])
        assert ns.uninstall is True


class TestBisectParser:
    def test_actions(self):
        parser = build_parser()
        for action in ["start", "good", "bad", "skip", "exclude", "restore", "status", "reset"]:
            ns = parser.parse_args(["bisect", action])
            assert ns.action == action

    def test_exclude_with_node(self):
        parser = build_parser()
        ns = parser.parse_args(["bisect", "exclude", "soundflow"])
        assert ns.action == "exclude"
        assert ns.node_name == "soundflow"


class TestPathResolution:
    """Ensure runtime paths resolve lazily to CWD, not at import time."""

    def test_requirements_file_uses_cwd(self):
        """_requirements_file() must resolve relative to CWD."""
        assert _requirements_file() == Path.cwd() / "requirements.txt"

    def test_bisect_state_uses_cwd(self):
        assert _bisect_state_file() == Path.cwd() / ".bisect_state.json"

    def test_custom_nodes_uses_cwd(self):
        assert _custom_nodes_dir() == Path.cwd() / "custom_nodes"

    def test_bisect_disabled_uses_cwd(self):
        assert _bisect_disabled_dir() == Path.cwd() / "custom_nodes_bisect_disabled"

    def test_paths_are_lazy_not_import_time(self, tmp_path, monkeypatch):
        """Paths must change when CWD changes (lazy resolution).

        This is the actual bug: if paths are captured at import time,
        they freeze to wherever 'pip install -e .' was run, not where
        the user invokes comfydbg from.
        """
        monkeypatch.chdir(tmp_path)
        assert _requirements_file() == tmp_path / "requirements.txt"
        assert _bisect_state_file() == tmp_path / ".bisect_state.json"
        assert _custom_nodes_dir() == tmp_path / "custom_nodes"

    def test_no_package_dir_in_runtime_paths(self, tmp_path, monkeypatch):
        """Runtime paths must not contain the package install directory."""
        monkeypatch.chdir(tmp_path)
        import comfydbg
        pkg_dir = str(Path(comfydbg.__file__).parent)
        for path_fn in [_requirements_file, _bisect_state_file, _custom_nodes_dir]:
            assert pkg_dir not in str(path_fn()), (
                f"{path_fn()} resolves inside package dir {pkg_dir} -- "
                "should use Path.cwd() not Path(__file__).parent"
            )


class TestCLISmoke:
    """Integration tests that invoke comfydbg as a subprocess."""

    def test_help_exits_zero(self):
        """comfydbg -h should exit 0."""
        import subprocess, sys
        result = subprocess.run(
            [sys.executable, "-m", "comfydbg", "-h"],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0
        assert "comfydbg" in result.stdout

    def test_version_subcommand_from_comfyui_dir(self, tmp_path):
        """comfydbg version should work from a dir with requirements.txt."""
        import subprocess, sys
        # Create a minimal requirements.txt
        (tmp_path / "requirements.txt").write_text("torch\nnumpy\n")
        result = subprocess.run(
            [sys.executable, "-m", "comfydbg", "version"],
            capture_output=True, text=True, timeout=15,
            cwd=str(tmp_path),
        )
        assert result.returncode == 0
        assert "ComfyUI Version Info" in result.stdout

    def test_default_command_no_requirements_errors(self, tmp_path):
        """comfydbg in a dir without requirements.txt should fail with clear error."""
        import subprocess, sys
        result = subprocess.run(
            [sys.executable, "-m", "comfydbg"],
            capture_output=True, text=True, timeout=10,
            cwd=str(tmp_path),
        )
        assert result.returncode != 0
        assert "requirements.txt" in result.stdout or "requirements.txt" in result.stderr
        assert "ComfyUI" in result.stdout or "ComfyUI" in result.stderr

    def test_install_help(self):
        """comfydbg install -h should show install options."""
        import subprocess, sys
        result = subprocess.run(
            [sys.executable, "-m", "comfydbg", "install", "-h"],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0
        assert "-HN" in result.stdout
        assert "-CN" in result.stdout
        assert "-G" in result.stdout

    def test_bisect_status_no_session(self, tmp_path):
        """comfydbg bisect status with no active session should say so."""
        import subprocess, sys
        result = subprocess.run(
            [sys.executable, "-m", "comfydbg", "bisect", "status"],
            capture_output=True, text=True, timeout=10,
            cwd=str(tmp_path),
        )
        assert result.returncode == 0
        assert "No bisect in progress" in result.stdout

    def test_detect_missing_file(self, tmp_path):
        """comfydbg detect on a nonexistent file should error."""
        import subprocess, sys
        result = subprocess.run(
            [sys.executable, "-m", "comfydbg", "detect", "nonexistent.webp"],
            capture_output=True, text=True, timeout=10,
            cwd=str(tmp_path),
        )
        assert result.returncode != 0


class TestDefaultCommandNoRequirements:
    """Test that comfydbg gives a clear error when not in a ComfyUI directory."""

    def test_skip_without_requirements(self, tmp_path, monkeypatch):
        """Default (skip) command should fail gracefully without requirements.txt."""
        monkeypatch.chdir(tmp_path)
        import comfydbg.launcher as launcher
        from types import SimpleNamespace

        args = SimpleNamespace(packages=[], main_args=[])
        # Should raise FileNotFoundError since cmd_skip opens the file
        with pytest.raises(FileNotFoundError):
            launcher.cmd_skip(args)

    def test_main_catches_missing_requirements(self, tmp_path):
        """main() should catch missing requirements and give clear error."""
        import subprocess, sys
        result = subprocess.run(
            [sys.executable, "-m", "comfydbg"],
            capture_output=True, text=True, timeout=10,
            cwd=str(tmp_path),
        )
        assert result.returncode == 1
        assert "requirements.txt" in result.stdout
