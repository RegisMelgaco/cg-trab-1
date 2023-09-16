import matplotlib.pyplot as plt
import numpy as np
import math


class Coordinate:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __str__(self):
    return f'({self.x}, {self.y})'
  
  def __add__(self, other):
    return Coordinate(self.x + other.x, self.y + other.y)
  
  def __sub__(self, other):
    return Coordinate(self.x - other.x, self.y - other.y)
  
  def __mul__(self, other):
    return Coordinate(round(self.x * other), round(self.y * other))
  
  def __repr__(self) -> str:
    return f'({self.x}, {self.y})'
  
  def to_canvas_coordinate_system(self, canvas: np.array):
    shape = canvas.shape

    return Coordinate(round(self.x * shape[0]), round(self.y * shape[1]))


class Line:
  def __init__(self, c1: Coordinate, c2: Coordinate):
    self.c1 = c1
    self.c2 = c2

  def __str__(self):
    return f'[{self.c1}, {self.c2}]'
  
  def __t_range(self, step):
    t = 0
    while t < 1:
      yield t
      t += step

  def draw(self, canvas: np.matrix):
    c1 = self.c1.to_canvas_coordinate_system(canvas)
    c2 = self.c2.to_canvas_coordinate_system(canvas)
    delta = c1 - c2
    line_side = abs(delta.x) if abs(delta.x) > abs(delta.y) else abs(delta.y)
    step = line_side ** -1
    
    dots = [c1 - (delta * t) for t in self.__t_range(step)]
    for d in dots:
      canvas[d.x][d.y] = 1

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
  canvas1 = np.zeros((11, 11))
  canvas2 = np.zeros((21, 21))
  canvas3 = np.zeros((51, 51))

  l1 = Line(Coordinate(.2, .2), Coordinate(.7, .8))
  l2 = Line(Coordinate(.2, .2), Coordinate(.8, .7))
  l3 = Line(Coordinate(.2, .2), Coordinate(.8, .4))
  l4 = Line(Coordinate(.2, .2), Coordinate(.4, .8))
  l5 = Line(Coordinate(.2, .2), Coordinate(.0, .0))

  l1.draw(canvas1)
  l2.draw(canvas1)
  l3.draw(canvas1)
  l4.draw(canvas1)
  l5.draw(canvas1)

  l1.draw(canvas2)
  l2.draw(canvas2)
  l3.draw(canvas2)
  l4.draw(canvas2)
  l5.draw(canvas2)

  l1.draw(canvas3)
  l2.draw(canvas3)
  l3.draw(canvas3)
  l4.draw(canvas3)
  l5.draw(canvas3)

  plt.matshow(canvas1)
  plt.show()
  plt.matshow(canvas2)
  plt.show()
  plt.matshow(canvas3)
  plt.show()