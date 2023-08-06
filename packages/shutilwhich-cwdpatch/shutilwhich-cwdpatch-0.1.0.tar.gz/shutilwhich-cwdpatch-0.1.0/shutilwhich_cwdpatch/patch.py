from .__main__ import which

try:
    from shutil import which as _which
    import shutil
    shutil.which = which
except (ImportError, ModuleNotFoundError):
    pass

try:
    import shutilwhich
    shutilwhich.which = which
except ModuleNotFoundError:
    pass
