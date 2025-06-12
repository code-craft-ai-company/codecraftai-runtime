import os
import sys
pkg_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'source', 'packages'))
if pkg_dir not in sys.path:
    sys.path.insert(0, pkg_dir)
