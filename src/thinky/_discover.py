import importlib
import logging
import os
import pkgutil
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union


def _get_default_paths() -> Optional[Path]:
    """
    Attempts to locate a default agent directory from a predefined list of paths.

    Returns:
        Path: The first valid file path found in the list.

    Raises:
        AgentsCLIException: If no valid default agent file path is found.
    """
    potential_paths = []

    for potential_path in potential_paths:
        path = Path(potential_path)
        if path.is_dir():
            return path


@dataclass
class ModuleData:
    module_import_str: str
    extra_sys_path: Path
    module_paths: Path


def _get_module_data_from_path(path: Path) -> ModuleData:
    """Derives module import information from a given directory path."""
    use_path = path.resolve()
    module_str = ".".join(use_path.parts[-2:])

    return ModuleData(
        module_import_str=module_str,
        extra_sys_path=use_path.parent.resolve(),
        module_paths=use_path,
    )


def get_agent_imports(path: Union[Path, None] = None):
    """Dynamically imports all submodules from a given agent directory path.

    This function is useful for ensuring all relevant agent modules are loaded,
    which is important for registration.

    Args:
        path (Union[Path, None], optional): The base path to the agent directory.
            If None, a default path will be resolved using `_get_default_paths()`.

    Raises:
        NNAgentsCLIException: If no valid default path is found.
        Exception: If `_get_module_data_from_path` or dynamic imports fail unexpectedly.
    """

    AGENT_DIR_PATH = "AGENT_DIR_PATH"

    if not path:
        path = _get_default_paths()

    if path is None:
        path_str = os.environ.get(AGENT_DIR_PATH)
        if path_str is None:
            raise RuntimeError(
                f"Missing required environment variable: {AGENT_DIR_PATH}"
            )
        else:
            path = Path(path_str)

    mod_data = _get_module_data_from_path(path)

    search_path = (
        mod_data.module_paths
        if mod_data.module_paths.is_dir()
        else mod_data.module_paths.parent
    )

    for _, module_name, _ in pkgutil.walk_packages(
        [search_path], mod_data.module_import_str + "."
    ):
        try:
            importlib.import_module(module_name)
            logging.debug(f"Imported: {module_name}")
        except (ImportError, ValueError) as e:
            logging.error(f"Import error for module '{module_name}': {e}")
