from utils.logger import get_logger
from .perception import Perception
from .action import ActionExecutor
from .memory import Memory
from .decision import QLearningDecision
from utils.config import WORKSPACE_DIR, SUPPORTED_FILE_TYPES, REWARDS

logger = get_logger("Agent")

class SelfLearningAgent:
    def __init__(self, workspace_dir=WORKSPACE_DIR):
        self.workspace_dir = workspace_dir
        self.perception = Perception(workspace_dir)
        self.action_executor = ActionExecutor(workspace_dir)
        self.memory = Memory()
        
        # Determine available actions (moving to folders defined in supported file types)
        # Adding a 'misc' or 'unknown' action could be beneficial
        available_folders = list(SUPPORTED_FILE_TYPES.keys()) + ["misc"]
        self.decision = QLearningDecision(actions_list=available_folders)

    def calculate_reward(self, file_state, action_taken):
        """
        A rule-based reward function to train the agent.
        """
        ext = file_state.get("extension", "").lower()
        
        correct_folder = "misc"
        for folder, exts in SUPPORTED_FILE_TYPES.items():
            if ext in exts:
                correct_folder = folder
                break

        if action_taken == correct_folder:
            return REWARDS.get("successful_move", 10)
        else:
            return REWARDS.get("failed_move", -5)

    def run_cycle(self):
        """Runs one full perception-decision-action-learning cycle."""
        logger.info("Starting agent task cycle...")
        
        # 1. Perception
        current_state = self.perception.observe()
        if not current_state:
            logger.info("Workspace is clean. No files to process.")
            return

        for file_state in current_state:
            # 2. Decision
            chosen_action = self.decision.choose_action(file_state)
            
            # 3. Action
            success = self.action_executor.execute("move_file", 
                                                   filepath=file_state["filepath"], 
                                                   destination_folder=chosen_action)
            
            # 4. Learning & Memory
            if success:
                reward = self.calculate_reward(file_state, chosen_action)
                self.decision.learn(file_state, chosen_action, reward)
                self.memory.store_experience(file_state, chosen_action, reward, None)
            
        # Save learned policy periodically
        self.decision.save_q_table()
        logger.info("Agent cycle completed successfully.")
