# shutilwhich-cwdpatch

Patch for `shutil.which` and `shutilwhich` that doesn't prepend CWD in search on Windows.


# Install

```bash
conda install -c defaults -c conda-forge shutilwhich-cwdpatch
```

or

```bash
pip install shutilwhich-cwdpatch
```


# Usage:

Simply import `patch` submodule before importing `shutil.which` or `shutilwhich` to patch them:

```py
import shutilwhich_cwdpatch.patch
from shutil import which
```

Or use `which` without patching:

```py
from shutilwhich_cwdpatch import which
```
