import pkgutil
import inspect

__all__ = list()

for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    this_module = loader.find_module(name).load_module(name)

    for name2, value in inspect.getmembers(this_module):
        if name2.startswith('__'):
            continue

        globals()[name2] = value
        __all__.append(name2)