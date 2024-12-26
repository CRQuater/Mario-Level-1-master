__author__ = 'justinarmstrong'

from data.tools import resource_path

"""
This module initializes the display and creates dictionaries of resources.
"""

import os
import pygame as pg
from data import tools
from data import constants as c

ORIGINAL_CAPTION = c.ORIGINAL_CAPTION


os.environ['SDL_VIDEO_CENTERED'] = '1'
pg.init()
pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP, pg.QUIT])
pg.display.set_caption(c.ORIGINAL_CAPTION)
SCREEN = pg.display.set_mode(c.SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()


FONTS = tools.load_all_fonts(os.path.join("resources","fonts"))
MUSIC = tools.load_all_music(os.path.join("resources","music"))
# FONTS = resource_path("resources/fonts")
# MUSIC = resource_path("resources/music")
GFX   = tools.load_all_gfx(os.path.join("resources","graphics"))
SFX   = tools.load_all_sfx(os.path.join("resources","sound"))
# GFX = resource_path("resources/graphics")
# SFX = resource_path("resources/sound")


