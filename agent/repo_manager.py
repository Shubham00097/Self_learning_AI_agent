import logging
import time
import shutil
from pathlib import Path
from typing import Optional, Dict, Any, List

import git

logger = logging.getLogger("agent.repo_manager")

WORKSPACES_DIR = Path.home() / ".sg_agent" / "workspaces"
MAX_CLONE_RETRIES = 3
RETRY_DELAY = 5


class RepoManager:
    """Manages local workspaces for cloned GitHub repositories."""

    def __init__(self, workspaces_dir: Path = WORKSPACES_DIR):
        """
        Initialize the RepoManager.

        Args:
            workspaces_dir: Directory where repositories are stored.
        """
        self.workspaces_dir = workspaces_dir
        self.workspaces_dir.mkdir(parents=True, exist_ok=True)

    def _extract_repo_name(self, url: str) -> str:
        """
        Extract the repository name from a GitHub URL.

        Args:
            url: A GitHub repository URL.

        Returns:
            The repository name without .git suffix.
        """
        return url.rstrip("/").split("/")[-1].replace(".git", "")

    def clone_or_pull(self, url: str) -> Optional[Path]:
        """
        Clone a remote repository or pull updates if it already exists locally.

        Args:
            url: The GitHub repository URL to clone.

        Returns:
            Path to the local repository, or None on failure.
        """
        repo_name = self._extract_repo_name(url)
        repo_path = self.workspaces_dir / repo_name

        if repo_path.exists() and (repo_path / ".git").exists():
            try:
                repo = git.Repo(repo_path)
                repo.remotes.origin.pull()
                logger.info(f"Updated existing repo: {repo_name}")
                return repo_path
            except git.exc.GitCommandError as e:
                logger.warning(f"Failed to pull {repo_name} (offline mode): {e}")
                return repo_path

        # Clone with retry logic
        for attempt in range(1, MAX_CLONE_RETRIES + 1):
            try:
                git.Repo.clone_from(url, str(repo_path))
                logger.info(f"Cloned {url} to {repo_path}")
                return repo_path
            except git.exc.GitCommandNotFound:
                logger.error("Git is not installed. Please install Git and try again.")
                return None
            except git.exc.GitCommandError as e:
                if attempt < MAX_CLONE_RETRIES:
                    logger.warning(
                        f"Clone attempt {attempt}/{MAX_CLONE_RETRIES} failed: {e}. "
                        f"Retrying in {RETRY_DELAY}s..."
                    )
                    time.sleep(RETRY_DELAY)
                else:
                    logger.error(
                        f"Failed to clone {url} after {MAX_CLONE_RETRIES} attempts: {e}"
                    )
                    return None

        return None

    def remove_repo(self, repo_name: str) -> bool:
        """
        Remove a managed workspace by name.

        Args:
            repo_name: Name of the repository to remove.

        Returns:
            True if removed successfully, False otherwise.
        """
        repo_path = self.workspaces_dir / repo_name

        if not repo_path.exists():
            logger.warning(f"Workspace not found: {repo_name}")
            return False

        try:
            shutil.rmtree(repo_path)
            logger.info(f"Removed workspace: {repo_name}")
            return True
        except PermissionError as e:
            logger.error(f"Permission denied removing {repo_name}: {e}")
            return False
        except Exception as e:
            logger.error(f"Failed to remove {repo_name}: {e}")
            return False

    def list_repos(self) -> List[Dict[str, Any]]:
        """
        List all managed repositories in the workspaces directory.

        Returns:
            A list of dicts with 'name' and 'path' for each repository.
        """
        repos = []
        if not self.workspaces_dir.exists():
            return repos

        for child in self.workspaces_dir.iterdir():
            if child.is_dir() and (child / ".git").exists():
                repos.append({"name": child.name, "path": str(child)})

        return repos
