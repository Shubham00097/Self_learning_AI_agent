from utils.logger import get_logger

logger = get_logger("Memory")

class Memory:
    def __init__(self):
        self.experiences = []

    def store_experience(self, state, action, reward, next_state):
        """Stores a single experience tuple."""
        experience = {
            "state": state,
            "action": action,
            "reward": reward,
            "next_state": next_state
        }
        self.experiences.append(experience)
        logger.debug(f"Stored experience. Total experiences: {len(self.experiences)}")

    def get_recent_experiences(self, n=10):
        return self.experiences[-n:]
