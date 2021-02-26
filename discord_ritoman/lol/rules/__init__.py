from discord_ritoman.lol.rules.lol_rule import LoLRule
from discord_ritoman.lol.stats.match_stat import LoLMatchStat
from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module

__all__ = []

# iterate through the modules in the current package
package_dir = Path(__file__).resolve().parent
for (_, module_name, _) in iter_modules([package_dir]):

    # import the module and iterate through its attributes
    module = import_module(f"{__name__}.{module_name}")
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)

        if isinstance(attribute, LoLRule):
            # Add the class to this package's variables
            __all__.append(module_name)
