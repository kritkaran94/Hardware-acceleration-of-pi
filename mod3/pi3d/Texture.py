#from __future__ import absolute_import, division, print_function, unicode_literals
from __future__ import print_function
import ctypes
import sys, os
from PIL import Image
from pi3d.constants import *
from pi3d.util.Ctypes import c_ints


MAX_SIZE = 1920
DEFER_TEXTURE_LOADING = True
WIDTHS = [4, 8, 16, 32, 48, 64, 72, 96, 128, 144, 192, 256,
           288, 384, 512, 576, 640, 720, 768, 800, 960, 1024, 1080, 1920]

def round_up_to_power_of_2(x):
  p = 1
  while p <= x:
    p += p
  return p

class Texture(Loadable):
  def __init__(self, file_string, blend=False, flip=False, size=0,
               defer=DEFER_TEXTURE_LOADING, mipmap=True, m_repeat=False):        
    super(Texture, self).__init__()
    try:
      if '' + file_string == file_string:
        self.is_file = True 
        if file_string[0] == '/': 
          self.file_string = file_string
        else:
          for p in sys.path:
            if os.path.isfile(p + '/' + file_string):
              self.file_string = p + '/' + file_string
              break
      else:
        self.file_string = file_string 
        self.is_file = False
    except:
      self.file_string = file_string
      self.is_file = False
    self.blend = blend
    self.flip = flip
    self.size = size
    self.mipmap = mipmap
    self.m_repeat = GL_MIRRORED_REPEAT if m_repeat else GL_REPEAT
    self.byte_size = 0
    self._loaded = False
    if defer:
      self.load_disk()
    else:
      self.load_opengl()

  def __del__(self):
    super(Texture, self).__del__()
    try:
      from pi3d.Display import Display
      if Display.INSTANCE:
        Display.INSTANCE.textures_dict[str(self._tex)][1] = 1
        Display.INSTANCE.tidy_needed = True
    except:
      pass 

  def tex(self):
    self.load_opengl()
    return self._tex

  def _load_disk(self):
    if self._loaded:
      return

    if self.is_file:
      s = self.file_string + ' '
      im = Image.open(self.file_string)
    else:
      s = 'PIL.Image '
      im = self.file_string

    self.ix, self.iy = im.size
    s += '(%s)' % im.mode
    self.alpha = (im.mode == 'RGBA' or im.mode == 'LA')

    if self.mipmap:
      resize_type = Image.BICUBIC
    else:
      resize_type = Image.NEAREST

    if self.iy > self.ix and self.iy > MAX_SIZE:
      im = im.resize((int((MAX_SIZE * self.ix) / self.iy), MAX_SIZE))
      self.ix, self.iy = im.size
    n = len(WIDTHS)
    for i in xrange(n-1, 0, -1):
      if self.ix == WIDTHS[i]:
        break
      if self.ix > WIDTHS[i]:
        im = im.resize((WIDTHS[i], int((WIDTHS[i] * self.iy) / self.ix)),
                        resize_type)
        self.ix, self.iy = im.size
        break

    if VERBOSE:
      print('Loading ...{}'.format(s))

    if self.flip:
      im = im.transpose(Image.FLIP_TOP_BOTTOM)

    RGBs = 'RGBA' if self.alpha else 'RGB'
    if im.mode != RGBs:
      im = im.convert(RGBs)
    self.image = im.tostring('raw', RGBs)
    self._tex = ctypes.c_int()
    if self.is_file and 'fonts/' in self.file_string:
      self.im = im
      
    self._loaded = True

  def _load_opengl(self):
    opengles.glGenTextures(4, ctypes.byref(self._tex), 0)
    from pi3d.Display import Display
    if Display.INSTANCE:
      Display.INSTANCE.textures_dict[str(self._tex)] = [self._tex, 0]
    opengles.glBindTexture(GL_TEXTURE_2D, self._tex)
    RGBv = GL_RGBA if self.alpha else GL_RGB
    opengles.glTexImage2D(GL_TEXTURE_2D, 0, RGBv, self.ix, self.iy, 0, RGBv,
                          GL_UNSIGNED_BYTE,
                          ctypes.string_at(self.image, len(self.image)))

    opengles.glEnable(GL_TEXTURE_2D)
    opengles.glGenerateMipmap(GL_TEXTURE_2D)
    opengles.glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    if self.mipmap:
      opengles.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                               GL_LINEAR_MIPMAP_NEAREST)
      opengles.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                               GL_LINEAR)
    else:
      opengles.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                               GL_NEAREST)
      opengles.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                               GL_NEAREST)
    opengles.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S,
                             self.m_repeat)
    opengles.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T,
                             self.m_repeat)


  def _unload_opengl(self):
    opengles.glDeleteTextures(1, ctypes.byref(self._tex))

  def __getstate__(self):
    if not self._loaded:
      self._load_disk()
      
    return {
      'blend': self.blend,
      'flip': self.flip,
      'size': self.size,
      'mipmap': self.mipmap,
      'file_string': self.file_string,
      'ix': self.ix,
      'iy': self.iy,
      'alpha': self.alpha,
      'image': self.image,
      '_tex': self._tex,
      '_loaded': self._loaded,
      'opengl_loaded': False,
      'disk_loaded': self.disk_loaded,
      'm_repeat': self.m_repeat
      }

class TextureCache(object):
  def __init__(self, max_size=None): 
    self.clear()

  def clear(self):
    self.cache = {}

  def create(self, file_string, blend=False, flip=False, size=0, **kwds):
    key = file_string, blend, flip, size
    texture = self.cache.get(key, None)
    if not texture:
      texture = Texture(*key, **kwds)
      self.cache[key] = texture

    return texture
