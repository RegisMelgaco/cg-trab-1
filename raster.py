import matplotlib.pyplot as plt
import numpy as np
import math

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
  
h_matrix = np.matrix([
    [ 2, -2,  1,  1],
    [-3,  3, -2, -1],
    [ 0,  0,  1,  0],
    [ 1,  0,  0,  0]
])

class Curve:
  def __init__(self, p1: Coordinate, p2: Coordinate, t1: Coordinate, t2: Coordinate):
    self.p1 = p1
    self.p2 = p2
    self.t1 = t1
    self.t2 = t2
    self.matrix = np.matrix([
        [p1.x ,p1.y, 0],
        [p2.x ,p2.y, 0],
        [t1.x ,t1.y, 0],
        [t2.x ,t2.y, 0],
    ])

  def __str__(self):
    return f'Curve(p1: {self.p1}, p2: {self.p2}, t1: {self.t1}, t2: {self.t2})'

  def draw(self, canvas: np.matrix, resolution = 15):
    resolution += 1
    step = resolution ** -1
    steps = [step * i for i in range(1, resolution)]
    print(len(steps), steps)

    ps = [(np.matrix([t**3, t**2, t, 1]) * h_matrix * self.matrix).tolist() for t in steps]

    ps = [Coordinate(p[0][0], p[0][1]) for p in ps]
    ps.insert(0, self.p1)
    ps.append(self.p2)

    lines = [Line(ps[i], ps[i+1]) for i in range(len(ps) - 1)]

    for l in lines:
      l.draw(canvas)


def create_graph(name, canvas_size, coordinates, lines):
  canvas = np.zeros(canvas_size)
  lines = [Line(coordinates[l[0]], coordinates[l[1]]) for l in lines]

  for l in lines:
    l.draw(canvas)

  plt.matshow(canvas)
  plt.savefig(f'plots/{name}.png')



if __name__ == "__main__":
  coordinates = {
    "1": Coordinate(0, 0),
    "2": Coordinate(1, 0),
    "3": Coordinate(0, 1),
    "4": Coordinate(1, 1),
  }

  lines = [["2", "3"], ["1", "4"]]

  create_graph("testinho", (100, 100), coordinates, lines)
