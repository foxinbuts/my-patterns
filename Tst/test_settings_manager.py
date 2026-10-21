from src.Core.validator import operation_exception
from src.Logics.settings_manager import settings_manager


def test_not_raise_settings_manager_load():
    manager = settings_manager()

    try:
        manager.load()
        assert True
    except operation_exception:
        assert False
    except:
        assert False

"""
Проверить загрузку настроек. Настройки не пустые.
"""
def test_not_empty_settings_manager_load():
    manager = settings_manager()

    try:
        manager.load()
    except:
        assert False

    assert manager.settings is not None

def test_equals_settings_manager_create():
    instanse1 = settings_manager()
    instanse2 = settings_manager()

    assert instanse1 == instanse2

def test_is_loaded_settings_manager_true():
    manager = settings_manager()

    try:
        manager.load()
    except:
        assert False

    assert manager.is_loaded

def test_equals_settings_manager_data():
    instanse1 = settings_manager()
    instanse2 = settings_manager()

    assert instanse1.settings == instanse2.settings
