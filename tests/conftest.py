"""Shared test fixtures for comfydbg."""

import pytest
from pathlib import Path


@pytest.fixture(autouse=True)
def ai_output_dir(tmp_path, monkeypatch, request):
    """Redirect prompt-only backend output to a temp directory."""
    if "keep_ai_output" in request.keywords:
        yield Path.home() / ".comfydbg" / "ai"
        return

    ai_dir = tmp_path / ".comfydbg" / "ai"
    ai_dir.mkdir(parents=True)
    monkeypatch.setattr(
        "comfydbg.ai.backends.prompt_only._get_output_dir",
        lambda: ai_dir,
    )
    yield ai_dir


@pytest.fixture
def tmp_requirements(tmp_path):
    """Create a temporary requirements.txt for testing."""
    req_file = tmp_path / "requirements.txt"
    req_file.write_text(
        "comfyui-frontend-package==1.41.20\n"
        "comfyui-workflow-templates==0.9.21\n"
        "torch\n"
        "numpy>=1.25.0\n"
        "Pillow\n"
    )
    return req_file
