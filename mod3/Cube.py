from ctypes.util import find_library
from os import environ
from pi3d.constants import egl
from pi3d.constants import gl
from pi3d.constants import gl2
from pi3d.constants import glext
from pi3d.constants import gl2ext
from pi3d import Display
from pi3d import Shader
from pi3d import Texture
from pi3d import Cuboid
import pyxlib
import platform

EGL_DEFAULT_DISPLAY = 0
EGL_NO_CONTEXT = 0
EGL_NO_DISPLAY = 0
EGL_NO_SURFACE = 0
EGL_FALSE = 0
DISPMANX_PROTECTION_NONE = 0


PLATFORM_PI = 0
PLATFORM_OSX = 1
PLATFORM_WINDOWS = 2
PLATFORM_LINUX = 3
PLATFORM_ANDROID = 4

def _load_library(name):
  if name:
    try:
      import ctypes
      return ctypes.CDLL(name)
    except:
      from pi3d.util import Log
      Log.logger(__name__).error("Couldn't load library %s", name)

def _linux():
  platform = PLATFORM_LINUX  
  bcm_name = find_library('bcm_host')
  if bcm_name:
    platform = PLATFORM_PI
    bcm = _load_library(bcm_name)
  else:
    bcm = None

  opengles = _load_library(find_library('GLESv2')) # :)
  openegl = _load_library(find_library('EGL'))  # :)
  
  return platform, bcm, openegl, opengles 

def _darwin():
  pass

_PLATFORMS = {
  'linux': _linux,
  'darwin': _darwin
  }

def _detect_platform_and_load_libraries():
  

  platform_name = platform.system().lower()
  loader = _PLATFORMS.get(platform_name, None)
  if not loader:
    raise Exception("Couldn't understand platform %s" % platform_name)

  return loader()

PLATFORM, bcm, openegl, opengles = _detect_platform_and_load_libraries()

display = Display.create(x=50,y=50)
shader = Shader("star") 
tex = Texture("textures/water.jpg") 
box = Cuboid(x=0,y=0,z=2.2) 
box.set_draw_details(shader,[tex]) 

tm = 0.0
dt = 0.01
sc = 0.0
ds = 0.001

while display.loop_running():
   box.set_custom_data(48, [tm, sc, -0.5 * sc])
   tm += dt
   sc = (sc + ds) % 10.0
   box.rotateIncX(0.01)
   box.rotateIncY(0.071)
   box.draw()
