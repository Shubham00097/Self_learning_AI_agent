import os
from utils.logger import get_logger
from utils.config import WORKSPACE_DIR

logger = get_logger("FileCleanupTask")

def run_cleanup_task(workspace_dir=WORKSPACE_DIR):
    """
    A simpler rule-based task that removes empty directories in the workspace.
    """
    logger.info(f"Initializing File Cleanup Task in {workspace_dir}")
    
    if not os.path.exists(workspace_dir):
        logger.warning("Workspace does not exist. Nothing to clean.")
        return

    removed_count = 0
    for dirpath, dirnames, filenames in os.walk(workspace_dir, topdown=False):
        # Do not remove the base workspace dir itself
        if dirpath == workspace_dir:
            continue
            
        if not dirnames and not filenames:
            logger.info(f"Removing empty directory: {dirpath}")
            try:
                os.rmdir(dirpath)
                removed_count += 1
            except Exception as e:
                logger.error(f"Failed to remove {dirpath}: {e}")

    logger.info(f"File Cleanup Task Completed! Removed {removed_count} empty directories.")

if __name__ == "__main__":
    run_cleanup_task()
