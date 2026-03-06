"""
Built-in file sorter plugin.
Monitors file events and logs sorting actions.
Full sorting logic will be ported from tasks/file_sorting.py in Phase 3.
"""

import logging

logger = logging.getLogger("plugin.file_sorter")

PLUGIN_NAME = "file_sorter"
PLUGIN_VERSION = "1.0.0"


def run(event: dict, context: dict) -> None:
    """
    Process a file system event for sorting.

    Args:
        event: Dict with 'type', 'path', and 'is_directory' keys.
        context: Dict with workspace and runtime context.
    """
    logger.info(f"file_sorter: processed event {event.get('type', 'unknown')}")
