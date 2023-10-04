import matplotlib.pyplot as plt
import numpy as np
import math


class Coordinate:
  def __init__(self, x, y):
    self.x = round(x, 4)
    self.y = round(y, 4)

  def __str__(self):
    return f'({self.x}, {self.y})'

  def __add__(self, other):
    if isinstance(other, Coordinate):
      return Coordinate((self.x + other.x), (self.y + other.y))

    return Coordinate((self.x + other), (self.y + other))

  def __mul__(self, other):
    if isinstance(other, Coordinate):
      return Coordinate((self.x * other.x), (self.y * other.y))

    return Coordinate((self.x * other), (self.y * other))

  def __repr__(self) -> str:
    return f'({self.x}, {self.y})'

  def to_canvas_coordinate_system(self, canvas: np.matrix):
    shape = canvas.shape

    c = Coordinate((self.x / 2) + 0.5, (self.y / 2) + 0.5)
    c = Coordinate(round(c.x * shape[0]), round(c.y * shape[1]))

    if c.x >= shape[0]:
      c.x = shape[0]-1

    if c.y >= shape[1]:
      c.y = shape[1]-1

    return c


class Line:
  def __init__(self, p1: Coordinate, p2: Coordinate):
    self.p1 = p1
    self.p2 = p2

  def __str__(self):
    return f'[{self.p1}, {self.p2}]'

  def __t_range(self, step):
    t = 0
    while t < 1:
      yield t
      t += step

  def dim_length(self, canvas):
    delta = (self.p1 + (self.p2 * -1))
    return abs(delta.x) if abs(delta.x) > abs(delta.y) else abs(delta.y)

  def draw(self, canvas: np.matrix):
    p1 = self.p1.to_canvas_coordinate_system(canvas)
    p2 = self.p2.to_canvas_coordinate_system(canvas)
    delta = p1 + (p2 * -1)
    line_side = abs(delta.x) if abs(delta.x) > abs(delta.y) else abs(delta.y)
    if line_side == 0:
      return

    step = line_side ** -1

    dots = [p1 + (delta * t * -1) for t in self.__t_range(step)]
    for d in dots:
      canvas[round(d.y)][round(d.x)] = 1

    return dots


class Geometry:
  def __init__(self, *lines):
    if len(lines) < 3:
      raise Exception("é obigatório possuir 3 linhas ou mais")
    self.lines = lines

  def draw_borders(self, canvas):
    for l in self.lines:
      l.draw(canvas)

  def draw(self, canvas: np.ndarray):
    _canvas = np.zeros(canvas.shape)
    self.draw_borders(_canvas)

    for x in range(len(_canvas)):
      buff, on_interval, on_border = [], False, False
      for y in range(len(_canvas[x])):
        if on_border and _canvas[x][y] != 0:
          continue

        on_border = False

        if _canvas[x][y] != 0:
          on_interval = not on_interval
          on_border = True

        if on_interval:
          buff.append(Coordinate(x, y))

        if not on_interval:
          self._draw_coordinates(_canvas, buff)
          buff = []

    canvas += _canvas

  def _draw_coordinates(self, canvas: np.ndarray, coordinates):
    for c in coordinates:
      canvas[c.x][c.y] = 1

    return coordinates

if __name__ == "__main__":
  canvas1 = np.zeros((10, 10))
  canvas2 = np.zeros((20, 20))
  canvas3 = np.zeros((50, 50))

  for i in range(8):
    i /= 4
    l = Line(Coordinate(0,0) ,Coordinate(math.sin(math.pi * i), math.cos(math.pi * i)))
    l.draw(canvas1)
    l.draw(canvas2)
    l.draw(canvas3)

  # l1 = Line(Coordinate(-.8, -.8), Coordinate(.7, .8))
  # l2 = Line(Coordinate(-.8, -.8), Coordinate(.8, .7))
  # l3 = Line(Coordinate(-.8, -.8), Coordinate(.8, .4))
  # l4 = Line(Coordinate(-.8, -.8), Coordinate(.4, .8))
  # l5 = Line(Coordinate(-.8, -.8), Coordinate(.0, .0))

  # l1.draw(canvas1)
  # l2.draw(canvas1)
  # l3.draw(canvas1)
  # l4.draw(canvas1)
  # l5.draw(canvas1)

  # l1.draw(canvas2)
  # l2.draw(canvas2)
  # l3.draw(canvas2)
  # l4.draw(canvas2)
  # l5.draw(canvas2)

  # l1.draw(canvas3)
  # l2.draw(canvas3)
  # l3.draw(canvas3)
  # l4.draw(canvas3)
  # l5.draw(canvas3)

  plt.matshow(canvas1)
  plt.show()
  plt.matshow(canvas2)
  plt.show()
  plt.matshow(canvas3)
  plt.show()
