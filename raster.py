import matplotlib.pyplot as plt
import numpy as np
import math
from PIL import Image
import os


class Coordinate:
  def __init__(self, x, y):
    self.x = x
    self.y = y

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
    
    delta_x = abs(p1.x - p2.x)
    delta_y = abs(p1.y - p2.y)

    xs, ys = [], []

    # Horizontal line
    if delta_x == 0:
        ys = range(p1.y, p2.y+1) if p1.y < p2.y else range(p1.y, p2.y-1, -1)
        xs = map(lambda x: p1.x, ys)
        
    else:
        a = (p1.y - p2.y) / (p1.x - p2.x)
        b = p1.y - a*p1.x

        # |Δx| > |Δy|
        if delta_x > delta_y:
            xs = range(p1.x, p2.x+1) if p1.x < p2.x else range(p1.x, p2.x-1, -1)
            ys = map(lambda x: (x * a) + b, xs)

        # |Δy| >= |Δx|
        else:
            ys = range(p1.y, p2.y+1) if p1.y < p2.y else range(p1.y, p2.y-1, -1)
            xs = map(lambda y: (y-b)/a, ys)

    for p in zip(xs, ys):
      canvas[round(p[0])][round(p[1])] = 100
  
class Geometry:
  def __init__(self, lines):
    print(lines)
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
      canvas[c.x][c.y] = 100

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
    step = resolution ** -1
    steps = [step * i for i in range(1, resolution)]

    ps = [(np.matrix([t**3, t**2, t, 1]) * h_matrix * self.matrix).tolist() for t in steps]

    ps = [Coordinate(p[0][0], p[0][1]) for p in ps]
    ps.insert(0, self.p1)
    ps.append(self.p2)

    lines = [Line(ps[i], ps[i+1]) for i in range(len(ps) - 1)]

    for l in lines:
      l.draw(canvas)


def create_graph(name, canvas_size, coordinates, edges, curves, polies):
  canvas = np.zeros(canvas_size)
  
  es = {}
  for k in edges:
    e = edges[k]
    p1 = coordinates[str(e['p1'])]
    p2 = coordinates[str(e['p2'])]
    e = Line(p1, p2)
    es[k] = e
    e.draw(canvas)

  for c in curves:
    c = curves[c]
    p1 = coordinates[str(c['p1'])]
    p2 = coordinates[str(c['p2'])]
    t1 = coordinates[str(c['t1'])]
    t2 = coordinates[str(c['t2'])]
    res = c['res']

    Curve(p1, p2, t1, t2).draw(canvas, res)

  for p in polies:
    Geometry([es[str(e)] for e in polies[p]]).draw(canvas)

  if not os.path.exists('plots'):
    os.makedirs('plots')

  print(canvas)
  img = Image.fromarray(canvas.astype(np.uint8))
  img.save(f'plots/{name}.png')



if __name__ == "__main__":
  coordinates = {
    "1": Coordinate(0, 0),
    "2": Coordinate(1, 0),
    "3": Coordinate(0, 1),
    "4": Coordinate(1, 1),
  }

  lines = {'1': {'p1': 1, 'p2': 2}}

  create_graph("testinho", (100, 100), coordinates, lines, {}, {})
