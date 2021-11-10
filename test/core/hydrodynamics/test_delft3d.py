from pathlib import Path

import pytest

from src.core.hydrodynamics.delft3d import Delft3D
from src.core.hydrodynamics.hydrodynamic_protocol import HydrodynamicProtocol


class TestDelft3d:
    def test_init_delft3d(self):
        test_delft3d = Delft3D()
        assert isinstance(test_delft3d, HydrodynamicProtocol)
        assert test_delft3d.time_step is None
        assert test_delft3d.d3d_home is None
        assert test_delft3d.working_dir is None
        assert test_delft3d.definition_file is None
        assert test_delft3d.config_file is None
        assert test_delft3d.x_coordinates is None
        assert test_delft3d.y_coordinates is None
        assert test_delft3d.xy_coordinates is None
        assert test_delft3d.water_depth is None
        assert test_delft3d.space is None
        assert repr(test_delft3d) == "Delft3D()"

    def test_set_d3d_home_sets_other_paths(self):
        test_delft3d = Delft3D()
        ref_path = Path()
        test_delft3d.d3d_home = ref_path
        assert test_delft3d.dflow_dir == ref_path / "dflowfm" / "bin" / "dflowfm"
        assert test_delft3d.dimr_dir == ref_path / "dimr" / "bin" / "dimr_dll"

    def test_model_fm_no_model_raises_valueeror(self):
        test_delft3d = Delft3D()
        with pytest.raises(ValueError) as e_info:
            test_delft3d.model_fm
        assert str(e_info.value) == "Model FM has not been defined."

    def test_model_dimr_no_model_raises_valueeror(self):
        test_delft3d = Delft3D()
        with pytest.raises(ValueError) as e_info:
            test_delft3d.model_dimr
        assert str(e_info.value) == "Model dimr has not been defined."

    def test_settings_returns_expected_values(self):
        expected_text = (
            "Coupling with Delft3D model (incl. DFlow-module) with the following settings:"
            "\n\tDelft3D home dir.  : None"
            "\n\tDFlow file         : None"
        )
        test_delft3d = Delft3D()
        assert test_delft3d.settings == expected_text

    def test_settings_returns_expected_values_config_true(self):
        expected_text = (
            "Coupling with Delft3D model (incl. DFlow- and DWaves-modules) with the following settings:"
            "\n\tDelft3D home dir.  : None"
            "\n\tDFlow file         : None"
            "\n\tConfiguration file : aPath"
        )
        test_delft3d = Delft3D()
        test_delft3d.working_dir = Path()
        test_delft3d.config_file = "aPath"
        assert test_delft3d.settings == expected_text

    def test_set_workdir_as_str_returns_path(self):
        test_delft3d = Delft3D()
        test_delft3d.working_dir = "thisPath"
        assert isinstance(test_delft3d.working_dir, Path)

    def test_set_d3dhome_as_str_returns_path(self):
        test_delft3d = Delft3D()
        test_delft3d.d3d_home = "thisPath"
        assert isinstance(test_delft3d.d3d_home, Path)

    def test_set_definition_file_relative_to_work_dir(self):
        test_delft3d = Delft3D()
        test_delft3d.working_dir = "thisPath"
        test_delft3d.definition_file = "anMdu"
        assert test_delft3d.definition_file == Path("thisPath") / "anMdu"

    def test_set_config_relative_to_work_dir(self):
        test_delft3d = Delft3D()
        test_delft3d.working_dir = "thisPath"
        test_delft3d.config_file = "config"
        assert test_delft3d.config_file == Path("thisPath") / "config"