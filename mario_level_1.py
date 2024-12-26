#!/usr/bin/env python
__author__ = 'justinarmstrong'

from data.tools import load_all_gfx

"""
This is an attempt to recreate the first level of
Super Mario Bros for the NES.
"""

import sys
import pygame as pg
from data.main import main
import ctypes

def is_admin():
    """Check if the script is running with admin privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def elevate_to_admin():
    """Restart the script with admin privileges."""
    if not is_admin():
        # Relaunch the script with admin privileges
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()

if __name__=='__main__':
    elevate_to_admin()
    main()
    pg.quit()
    sys.exit()