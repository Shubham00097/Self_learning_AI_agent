import os

# Base directory for the agent's operations
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE_DIR = os.path.join(BASE_DIR, "demo_workspace")

# Logging Configuration
LOG_FILE = os.path.join(BASE_DIR, "agent.log")
LOG_LEVEL = "INFO"

# RL Agent Configuration
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.9
EXPLORATION_RATE = 1.0
EXPLORATION_DECAY = 0.99
MIN_EXPLORATION_RATE = 0.01

# Task specific config for file sorting
SUPPORTED_FILE_TYPES = {
    "images": [".jpg", ".png", ".jpeg", ".gif"],
    "documents": [".pdf", ".docx", ".txt", ".xlsx"],
    "archives": [".zip", ".tar.gz", ".rar"],
    "code": [".py", ".js", ".html", ".css", ".md", ".json"]
}

# Rewards for reinforcement learning
REWARDS = {
    "successful_move": 10,
    "failed_move": -5,
    "invalid_action": -1,
    "already_organized": -1
}
