from agent.agent import SelfLearningAgent
from utils.logger import get_logger
from utils.config import WORKSPACE_DIR

logger = get_logger("FileSortingTask")

def run_file_sort_task(workspace_dir=WORKSPACE_DIR, episodes=10):
    """
    Runs the file sorting task using the Self-Learning Agent.
    """
    logger.info(f"Initializing File Sorting Task in {workspace_dir}")
    agent = SelfLearningAgent(workspace_dir)
    
    for episode in range(1, episodes + 1):
        logger.info(f"--- Episode {episode} ---")
        agent.run_cycle()
        
    logger.info("File Sorting Task Completed!")

if __name__ == "__main__":
    run_file_sort_task()
