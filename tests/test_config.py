import os
from grid.core.config import create_template

def test_config_generation(tmp_path):
    os.chdir(tmp_path)
    create_template()
    assert os.path.exists("config.grid")
