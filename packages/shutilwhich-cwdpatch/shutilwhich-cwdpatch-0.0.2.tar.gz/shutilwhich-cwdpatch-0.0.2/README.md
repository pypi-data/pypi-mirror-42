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

Simply import shutilwhich-cwdpatch before importing `shutil.which` or `shutilwhich`:

```py
import shutilwhich_cwdpatch
from shutil import which
```
