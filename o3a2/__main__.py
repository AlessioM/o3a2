"""
running `python -m o3a2 install` will copy o3a2 into the CWD
allowing the use as a build tool
"""

import sys
import shutil
import os

if len(sys.argv) > 0 and sys.argv[1] == "install":
    src = os.path.join(os.path.dirname(__file__), "o3a2.py")
    dst = os.path.join(os.getcwd(), "o3a2.py")
    print("installing o3a2")
    shutil.copy(src, dst)
