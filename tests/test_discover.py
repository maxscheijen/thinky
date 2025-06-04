import tempfile
from pathlib import Path

from thinky._discover import ModuleData, _get_module_data_from_path


def test_get_module_data_from_path():
    with tempfile.TemporaryDirectory() as tmp_dir:
        base_path = Path(tmp_dir)
        pkg_path = base_path / "pkg"
        mod_path = pkg_path / "mod"
        mod_path.mkdir(parents=True)

        result = _get_module_data_from_path(mod_path)
        expected_module_str = "pkg.mod"
        expected_extra_sys_path = mod_path.parent.resolve()
        expected_module_paths = mod_path.resolve()

        assert isinstance(result, ModuleData)
        assert result.module_import_str == expected_module_str
        assert result.extra_sys_path == expected_extra_sys_path
        assert result.module_paths == expected_module_paths
