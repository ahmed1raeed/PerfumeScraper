import importlib
import pkgutil

SITES = []

for module in pkgutil.iter_modules(__path__):
    if module.name == "__init__":
        continue

    mod = importlib.import_module(f"{__name__}.{module.name}")

    if hasattr(mod, "SITE"):
        SITES.append(mod.SITE)