"""
ComfyUI version history tracking.

Queries PyPI and GitHub for version history of ComfyUI packages.
Future: Track local install history for rollback support.
"""


def get_pypi_history(package_name, limit=50):
    """Get version history from PyPI for a package.

    Returns list of (version, upload_date) tuples, newest first.
    """
    # TODO: Extract from launcher.py get_pypi_versions()
    raise NotImplementedError("Will be extracted from launcher.py in v0.2.0")


def get_github_history(repo, limit=50):
    """Get release history from GitHub for a repo.

    Returns list of (tag, published_date) tuples, newest first.
    """
    # TODO: Extract from launcher.py get_github_releases()
    raise NotImplementedError("Will be extracted from launcher.py in v0.2.0")
