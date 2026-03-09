# Self-Learning AI Agent for Task Automation

An autonomous AI agent that learns to automate repetitive computer tasks using a perception-decision-action pipeline. Currently, the agent specializes in organizing file systems using a Reinforcement Learning (Q-learning) approach.

## Project Overview

This project implements a self-learning agent capable of perceiving its environment (a workspace directory), deciding how to handle each file based on its extension, and executing the action (moving the file to the correct category folder). It learns from a reward system over multiple episodes.

## System Architecture

The agent follows an intelligent loop:
- **Perception (`agent/perception.py`)**: Observes the current system state, scanning for files and their properties.
- **Decision (`agent/decision.py`)**: Uses Q-learning to choose the best action based on an epsilon-greedy policy. Epsilon decays over time, shifting the agent from exploration to exploitation.
- **Action (`agent/action.py`)**: Safely executes the chosen command (e.g., moving a file).
- **Memory (`agent/memory.py`)**: Stores experiences to track learning progress over time.
- **Agent Orchestrator (`agent/agent.py`)**: Connects all components and applies a rule-based reward function to update the Q-table.

## Installation

1. **Clone the repository** (or download the source).
2. **Requirements**: The code relies entirely on Python's Standard Library. You do not need to install external packages.
3. Run using Python 3.x.

## Usage

You can run the agent through the CLI entry point `main.py`.

### 1. File Sorting Agent (Learning Task)
Automatically sort files into categorical folders (`images`, `documents`, `code`, `archives`, etc.).
```bash
python main.py --task sort --episodes 10 --workspace ./demo_workspace
```

### 2. Workspace Cleanup (Rule-Based Task)
Recursively removes empty directories from the workspace.
```bash
python main.py --task cleanup --workspace ./demo_workspace
```

### 3. Run Both
```bash
python main.py --task both --episodes 10 --workspace ./demo_workspace
```

## Example Demo

1. Add some unstructured files to a `demo_workspace/` directory (e.g., `test.txt`, `image.png`, `script.py`).
2. Run `python main.py --task sort --workspace demo_workspace`.
3. Watch as the agent learns the correct folders (it may make mistakes in episode 1 during exploration, but will perfect its policy as episodes increase).
4. The learned Q-table policy is automatically saved to `q_table.json`.

## Future Improvements

- Add support for Complex State Representation (e.g., file sizes, creation dates).
- Upgrade Decision engine to Deep Reinforcement Learning (DQN) for more complex, continuous environments.
- Add more Actions (compress files, send email reports, delete old logs).
- Implement a dashboard to visualize the agent's memory and learning curve in real-time.
