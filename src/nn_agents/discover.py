import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Union


@dataclass
class ModuleData:
    module_import_str: str
    extra_sys_path: Path
    module_paths: List[Path]


def get_module_data_from_path(path: Path) -> ModuleData:
    """Derives module import information from a given file or directory path.

    Args:
        path (Path): A file or directory pointing to a Python module or package.
                     If it's a file, it should be a .py file. If it's `__init__.py`,
                     its parents directory is treated as the module.

    Returns:
        ModuleData: An object containing:
            - module_import_str (str): The dotted import path of the module.
            - extra_sys_path (Path): A directory to be added to the `sys.path`.
            - module_paths (List[Path]): The sequence of directories from the top-level
              package down to the module.
    """

    use_path = path.resolve()
    module_path = use_path

    if use_path.is_file() and use_path.stem == "__init__":
        module_path = use_path.parent

    module_paths = [module_path]
    extra_sys_path = module_path.parent

    for parent in module_path.parents:
        init_path = parent / "__init__.py"
        if init_path.is_file():
            module_paths.insert(0, parent)
            extra_sys_path = parent.parent
        else:
            break

    module_str = ".".join(p.stem for p in module_paths)
    return ModuleData(
        module_import_str=module_str,
        extra_sys_path=extra_sys_path.resolve(),
        module_paths=module_paths,
    )


@dataclass()
class ImportData:
    module_data: ModuleData
    import_string: str


def get_agents(path: Union[Path, None] = None):
    if not path:
        raise ValueError

    if not path.exists():
        raise ValueError("Path doesnt exist")

    mod_data = get_module_data_from_path(path)
    sys.path.insert(0, str(mod_data.extra_sys_path))

    import_string = mod_data.module_import_str
    return ImportData(module_data=mod_data, import_string=import_string)


if __name__ == "__main__":
    path = Path("~/projects/cli-python/src/cli_python/nn_agents")
    get_agents(path)
