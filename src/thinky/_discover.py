import importlib
import logging
import pkgutil
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

from thinky import AGENT_DIR_PATH

logger = logging.getLogger(__name__)


@dataclass
class ModuleData:
    module_import_str: str
    extra_sys_path: Path
    module_paths: Path


def _get_module_data_from_path(path: Path) -> ModuleData:
    """Derives module import information from a given directory path."""
    logger.debug(f"Using path: {path}")
    use_path = path.resolve()
    logger.debug(f"Importing agents from: {use_path}")
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

    if not path:
        path = get_agent_path()

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


def get_agent_path(path: Optional[Path] = None) -> Path:
    if path is None:
        if AGENT_DIR_PATH is None:
            raise RuntimeError(
                f"Missing required environment variable: {AGENT_DIR_PATH}"
            )
        else:
            path = Path(AGENT_DIR_PATH)
    return path
