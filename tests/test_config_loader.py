
from pathlib import Path

from onap_data_provider.config_loader import ConfigLoader


def test_config_loader_no_dirs():
    config_loader = ConfigLoader([Path(Path(__file__).parent, "test-data.yml")])
    configs = list(config_loader.load())
    assert len(configs) == 1

    config_loader = ConfigLoader([Path(Path(__file__).parent, "test-data.yml"),
                                  Path(Path(__file__).parent, "test-data-version.yml")])
    configs = list(config_loader.load())
    assert len(configs) == 2

def test_config_loader_dir():
    config_loader = ConfigLoader([Path(Path(__file__).parent, "config_dirs")])
    configs = list(config_loader.load())
    assert len(configs) == 2

def test_config_loader_both_dirs_and_files():
    config_loader = ConfigLoader([Path(Path(__file__).parent, "test-data.yml"),
                                  Path(Path(__file__).parent, "test-data-version.yml"),
                                  Path(Path(__file__).parent, "config_dirs")])
    configs = list(config_loader.load())
    assert len(configs) == 4
