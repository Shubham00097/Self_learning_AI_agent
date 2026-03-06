import logging
import importlib.util
from pathlib import Path
from typing import Dict, Any, List

logger = logging.getLogger("agent.plugin_registry")

PLUGINS_DIR = Path.home() / ".sg_agent" / "plugins"


class PluginRegistry:
    """Auto-discovers and manages plugins from a plugins directory."""

    def __init__(self, plugins_dir: Path = PLUGINS_DIR):
        """
        Initialize the PluginRegistry.

        Args:
            plugins_dir: Directory to scan for plugin .py files.
        """
        self.plugins_dir = plugins_dir
        self.plugins_dir.mkdir(parents=True, exist_ok=True)
        self._plugins: Dict[str, Dict[str, Any]] = {}

    def discover(self) -> int:
        """
        Scan the plugins directory and load all valid plugins.

        Returns:
            The number of plugins successfully loaded.
        """
        self._plugins.clear()

        for plugin_file in self.plugins_dir.glob("*.py"):
            self._load_plugin(plugin_file)

        logger.info(f"Discovered {len(self._plugins)} plugin(s)")
        return len(self._plugins)

    def _load_plugin(self, plugin_path: Path) -> bool:
        """
        Load a single plugin from a .py file.

        Args:
            plugin_path: Path to the plugin file.

        Returns:
            True if the plugin was loaded successfully.
        """
        try:
            module_name = plugin_path.stem
            spec = importlib.util.spec_from_file_location(
                module_name, str(plugin_path)
            )
            if spec is None or spec.loader is None:
                logger.warning(f"Cannot create module spec for {plugin_path}")
                return False

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Validate the required interface
            for attr in ("PLUGIN_NAME", "PLUGIN_VERSION", "run"):
                if not hasattr(module, attr):
                    logger.warning(
                        f"Plugin {module_name} missing required attribute: {attr}"
                    )
                    return False

            if not callable(module.run):
                logger.warning(f"Plugin {module_name}: 'run' is not callable")
                return False

            self._plugins[module.PLUGIN_NAME] = {
                "name": module.PLUGIN_NAME,
                "version": module.PLUGIN_VERSION,
                "run": module.run,
                "path": str(plugin_path),
            }
            logger.info(
                f"Loaded plugin: {module.PLUGIN_NAME} v{module.PLUGIN_VERSION}"
            )
            return True

        except Exception as e:
            logger.error(f"Failed to load plugin from {plugin_path}: {e}")
            return False

    def run_plugin(
        self, name: str, event: Dict[str, Any], context: Dict[str, Any]
    ) -> bool:
        """
        Execute a specific plugin by name.

        Args:
            name: The PLUGIN_NAME of the plugin to run.
            event: Event data dict to pass to the plugin.
            context: Context data dict to pass to the plugin.

        Returns:
            True if the plugin executed successfully.
        """
        if name not in self._plugins:
            logger.warning(f"Plugin not found: {name}")
            return False

        try:
            self._plugins[name]["run"](event, context)
            return True
        except Exception as e:
            logger.error(f"Plugin {name} failed: {e}")
            return False

    def run_all(
        self, event: Dict[str, Any], context: Dict[str, Any]
    ) -> Dict[str, bool]:
        """
        Execute all loaded plugins.

        Args:
            event: Event data dict to pass to each plugin.
            context: Context data dict to pass to each plugin.

        Returns:
            Dict mapping plugin names to success/failure status.
        """
        results = {}
        for name in self._plugins:
            results[name] = self.run_plugin(name, event, context)
        return results

    def list_plugins(self) -> List[Dict[str, str]]:
        """
        List all loaded plugins.

        Returns:
            List of dicts with 'name', 'version', and 'path' for each plugin.
        """
        return [
            {"name": p["name"], "version": p["version"], "path": p["path"]}
            for p in self._plugins.values()
        ]
