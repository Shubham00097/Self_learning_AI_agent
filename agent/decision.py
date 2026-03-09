import random
import json
import os
from utils.config import LEARNING_RATE, DISCOUNT_FACTOR, EXPLORATION_RATE, EXPLORATION_DECAY, MIN_EXPLORATION_RATE
from utils.logger import get_logger

logger = get_logger("Decision")

class QLearningDecision:
    def __init__(self, actions_list):
        self.q_table = {}
        self.actions_list = actions_list
        self.exploration_rate = EXPLORATION_RATE
        self.learning_rate = LEARNING_RATE
        self.discount_factor = DISCOUNT_FACTOR
        self.q_table_file = 'q_table.json'
        self.load_q_table()

    def get_state_key(self, state):
        """Convert state dictionary to a hashable string key for Q-table."""
        # For simplicity, state is determined by the file extension we are trying to categorize
        return state.get("extension", "unknown")

    def choose_action(self, state):
        """Choose action using epsilon-greedy policy."""
        state_key = self.get_state_key(state)
        
        if state_key not in self.q_table:
            self.q_table[state_key] = {action: 0.0 for action in self.actions_list}

        if random.uniform(0, 1) < self.exploration_rate:
            action = random.choice(self.actions_list)
            logger.debug(f"Exploring: chose random action {action} for state {state_key}")
        else:
            action = max(self.q_table[state_key], key=self.q_table[state_key].get)
            logger.debug(f"Exploiting: chose best action {action} with Q-value {self.q_table[state_key][action]} for state {state_key}")
            
        return action

    def learn(self, state, action, reward, next_state=None):
        """Update Q-value based on the reward received using Q-learning formula."""
        state_key = self.get_state_key(state)
        
        if state_key not in self.q_table:
            self.q_table[state_key] = {a: 0.0 for a in self.actions_list}

        old_value = self.q_table[state_key][action]
        # In this simple agent, moving a file completes an episode so next max Q is 0
        next_max = 0 
        
        new_value = (1 - self.learning_rate) * old_value + self.learning_rate * (reward + self.discount_factor * next_max)
        self.q_table[state_key][action] = new_value
        logger.debug(f"Updated Q-value for {state_key}, action {action}: {old_value:.2f} -> {new_value:.2f} (Reward: {reward})")

        # Decay exploration rate
        self.exploration_rate = max(MIN_EXPLORATION_RATE, self.exploration_rate * EXPLORATION_DECAY)

    def save_q_table(self):
        try:
            with open(self.q_table_file, 'w') as f:
                json.dump(self.q_table, f, indent=4)
            logger.debug("Saved Q-table to disk.")
        except Exception as e:
            logger.error(f"Failed to save Q-table: {e}")

    def load_q_table(self):
        if os.path.exists(self.q_table_file):
            try:
                with open(self.q_table_file, 'r') as f:
                    self.q_table = json.load(f)
                logger.debug("Loaded external Q-table from disk.")
            except Exception as e:
                logger.error(f"Failed to load Q-table: {e}")
