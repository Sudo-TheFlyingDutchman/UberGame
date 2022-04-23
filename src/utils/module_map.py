from os import listdir
from os.path import dirname, basename, isfile, splitext
from glob import glob
from inspect import isclass


class ModuleMeta(type):
    def __getattr__(cls, item):
        return getattr(cls.map, item)


class ModuleMap(metaclass=ModuleMeta):
    map: dict = {}

    def __class_getitem__(cls, item):
        return cls.map[item]

    def __init_subclass__(cls, **kwargs):
        cls.map = cls._find_subclasses(cls._import_modules(file=kwargs['file'], package=kwargs['package']),
                                       base_class=kwargs['base_class'])

    @classmethod
    def _find_subclasses(cls, modules, base_class):
        return {module: list(
            filter(lambda value: isclass(value) and issubclass(value, base_class) and value is not base_class,
                   vars(imported_module).values()))
                for module, imported_module in modules
                }

    @classmethod
    def _import_modules(cls, file, package):
        modules = listdir(dirname(file))
        return [(splitext(basename(module))[0],
                 __import__('.'.join([package, splitext(basename(module))[0]]), fromlist='*'))
                for module in modules if not basename(module).startswith('__')]
