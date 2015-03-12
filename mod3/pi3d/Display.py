from __future__ import absolute_import, division, print_function, unicode_literals

from ctypes import c_float, byref
from pi3d.constants import *
from pi3d.util.DisplayOpenGL import DisplayOpenGL

WIDTH = 0
HEIGHT = 0
    
class Display(object):
  INSTANCE = None

  def __init__(self, tkwin=None):

    if Display.INSTANCE:
      assert ALLOW_MULTIPLE_DISPLAYS
      LOGGER.warning('A second instance of Display was created')
    else:
      Display.INSTANCE = self

    self.tkwin = tkwin
    self.sprites = []
    self.sprites_to_load = set()
    self.sprites_to_unload = set()
    self.tidy_needed = False
    self.textures_dict = {}
    self.vbufs_dict = {}
    self.ebufs_dict = {}
    self.last_shader = None
    self.last_textures = [None, None, None]
    self.external_mouse = None
    self.opengl = DisplayOpenGL()
    self.max_width, self.max_height = self.opengl.width, self.opengl.height
    self.first_time = True
    self.is_running = True
    self.lock = threading.RLock()

    LOGGER.debug(STARTUP_MESSAGE)

  def loop_running(self):
    while DISPLAY.loop_running():
      if self.is_running:
        if self.first_time:
          self.time = time.time()
          self.first_time = False
      else:
        self._loop_end()
      self._loop_begin()
    else:
      self._loop_end()
      self.destroy()

    return self.is_running



def create(x=None, y=None, w=None, h=None, near=None, far=None,
           fov=0, depth=0, background=None,
           tk=False, window_title='', window_parent=None, mouse=False,frames_per_second=None, samples=0):
  if tk:
      from pi3d.util import TkWin
      if not (w and h):
        w = 1920
        h = 1180
      if background:
        bg_i = [int(i * 255) for i in background]
        bg = '#{:02X}{:02X}{:02X}'.format(bg_i[0], bg_i[1], bg_i[2])
      else:
        bg = '#000000'
      tkwin = TkWin.TkWin(window_parent, window_title, w, h, bg)
      tkwin.update()
      w = tkwin.winfo_width()
      h = tkwin.winfo_height()
      if x is None:
        x = tkwin.winx
      if y is None:
        y = tkwin.winy

  else:
    tkwin = None
    x = x or 0
    y = y or 0

  display = Display(tkwin)
  if (w or 0) <= 0:
    w = display.max_width - 2 * x
    if w <= 0:
      w = display.max_width
  if (h or 0) <= 0:
    h = display.max_height - 2 * y
    if h <= 0:
      h = display.max_height

  LOGGER.debug('Display size is w=%d, h=%d', w, h)

  display.frames_per_second = frames_per_second

  if near is None:
    near = DEFAULT_NEAR
  if far is None:
    far = DEFAULT_FAR

  display.width = w
  display.height = h
  display.near = near
  display.far = far
  display.fov = fov

  display.left = x
  display.top = y
  display.right = x + w
  display.bottom = y + h

  display.opengl.create_display(x, y, w, h, depth=depth, samples=samples)
 
  if background:
    display.set_background(*background)

  return display
