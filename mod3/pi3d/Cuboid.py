from __future__ import absolute_import, division, print_function, unicode_literals
class Cuboid(Shape):
  def __init__(self,  camera=None, light=None, w=1.0, h=1.0, d=1.0,
               name="", x=0.0, y=0.0, z=0.0,
               rx=0.0, ry=0.0, rz=0.0, cx=0.0, cy=0.0, cz=0.0, tw=1.0, th=1.0, td=1.0):
    super(Cuboid, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
                                1.0, 1.0, 1.0, cx, cy, cz)

    if VERBOSE:
      print("Creating cuboid ...")

    self.width = w
    self.height = h
    self.depth = d
    self.ssize = 36
    self.ttype = GL_TRIANGLES

    ww = w / 2.0
    hh = h / 2.0
    dd = d / 2.0

    self.vertices = ((-ww, hh, dd), (ww, hh, dd), (ww, -hh, dd), (-ww, -hh, dd),
        (ww, hh, dd),  (ww, hh, -dd),  (ww, -hh, -dd), (ww, -hh, dd),
        (-ww, hh, dd), (-ww, hh, -dd), (ww, hh, -dd),  (ww, hh, dd),
        (ww, -hh, dd), (ww, -hh, -dd), (-ww, -hh, -dd),(-ww, -hh, dd),
        (-ww, -hh, dd),(-ww, -hh, -dd),(-ww, hh, -dd), (-ww, hh, dd),
        (-ww, hh, -dd),(ww, hh, -dd),  (ww, -hh, -dd), (-ww,-hh,-dd))
    self.normals = ((0.0, 0.0, 1),    (0.0, 0.0, 1),   (0.0, 0.0, 1),  (0.0, 0.0, 1),
        (1, 0.0, 0),  (1, 0.0, 0),    (1, 0.0, 0),     (1, 0.0, 0),
        (0.0, 1, 0),  (0.0, 1, 0),    (0.0, 1, 0),     (0.0, 1, 0),
        (0.0, -1, 0), (0,- 1, 0),     (0.0, -1, 0),    (0.0, -1, 0),
        (-1, 0.0, 0),  (-1, 0.0, 0),  (-1, 0.0, 0),    (-1, 0.0, 0),
        (0.0, 0.0, -1),(0.0, 0.0, -1),(0.0, 0.0, -1),  (0.0, 0.0, -1))

    self.indices = ((1, 0, 3), (1, 3, 2), (5, 4, 7),  (5, 7, 6),
        (9, 8, 11),  (9, 11, 10), (13, 12, 15), (13, 15, 14),
        (19, 18, 17),(19, 17, 16),(20, 21, 22), (20, 22, 23))

    tw = tw / 2.0
    th = th / 2.0
    td = td / 2.0

    self.tex_coords = ((0.5+tw, 0.5-th),        (0.5-tw, 0.5-th),        (0.5-tw, 0.5+th),        (0.5+tw, 0.5+th)
        (0.5+td, 0.5-th),        (0.5-td, 0.5-th),        (0.5-td, 0.5+th),        (0.5+td, 0.5+th),
        (0.5-tw, 0.5-th),        (0.5+tw, 0.5-th),        (0.5+tw, 0.5+th),        (0.5-tw, 0.5+th), 
        (0.5+tw, 0.5+td),        (0.5-tw, 0.5+td),        (0.5-tw, 0.5-td),        (0.5+tw, 0.5-td), 
        (0.5-td, 0.5+th),        (0.5+td, 0.5+th),        (0.5+td, 0.5-th),        (0.5-td, 0.5-th),
        (0.5-tw, 0.5-th),        (0.5+tw, 0.5-th),        (0.5+tw, 0.5+th),        (0.5-tw, 0.5+th)) 
    self.buf = []
    self.buf.append(Buffer(self, self.vertices, self.tex_coords, self.indices, self.normals))

