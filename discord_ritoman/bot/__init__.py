from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module
from discord.ext.commands.core import Command

__all__ = ["bot_command"]

# iterate through the modules in the current package
package_dir = str(Path(__file__).resolve().parent)
for (_, module_name, _) in iter_modules([package_dir]):

    # import the module and iterate through its attributes
    module = import_module(f"{__name__}.{module_name}")
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)

        if isinstance(attribute, Command) and module_name != "bot":
            # Add the class to this package's variables
            __all__.append(module_name)
