import os
from utils.logger import get_logger

logger = get_logger("Perception")

class Perception:
    def __init__(self, workspace_dir):
        self.workspace_dir = workspace_dir
        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def observe(self):
        """
        Scans the workspace directory and returns a state representation.
        State is a list of file info dictionaries.
        """
        logger.debug(f"Scanning workspace: {self.workspace_dir}")
        state = []
        for file in os.listdir(self.workspace_dir):
            filepath = os.path.join(self.workspace_dir, file)
            if os.path.isfile(filepath):
                _, ext = os.path.splitext(file)
                state.append({
                    "filename": file,
                    "filepath": filepath,
                    "extension": ext.lower()
                })
        return state
