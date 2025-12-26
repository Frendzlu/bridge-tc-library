def test_imports():
    import importlib
    importlib.import_module('bridge_movement')
    importlib.import_module('bridge_movement.movements')
    importlib.import_module('bridge_movement.tournament')
    importlib.import_module('bridge_movement.examples.mitchell_example')
    assert True

