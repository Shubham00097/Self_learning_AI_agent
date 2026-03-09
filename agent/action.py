import os
import shutil
from utils.logger import get_logger

logger = get_logger("Action")

class ActionExecutor:
    def __init__(self, workspace_dir):
        self.workspace_dir = workspace_dir

    def execute(self, action_type, **kwargs):
        """
        Executes a given action.
        Returns True if successful, False otherwise.
        """
        if action_type == "move_file":
            return self.move_file(kwargs.get("filepath"), kwargs.get("destination_folder"))
        else:
            logger.warning(f"Unknown action type: {action_type}")
            return False

    def move_file(self, filepath, destination_folder):
        """Moves a file to a destination folder within the workspace."""
        if not filepath or not destination_folder:
            return False

        try:
            dest_dir = os.path.join(self.workspace_dir, destination_folder)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            
            filename = os.path.basename(filepath)
            dest_path = os.path.join(dest_dir, filename)
            
            logger.info(f"Moving file {filename} to {destination_folder}")
            shutil.move(filepath, dest_path)
            return True
        except Exception as e:
            logger.error(f"Failed to move file {filepath}: {e}")
            return False
