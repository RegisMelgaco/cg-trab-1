from flask import Flask, request

import raster


app = Flask(__name__)

@app.route("/raster", methods=['POST'])
def create_img():
    name = request.json['name']
    resolution = request.json['resolution']
    lines = request.json['lines']

    coordinates = {}
    for k, c in request.json['coordinates'].items():
        coordinates[k] = raster.Coordinate(c['x'], c['y'])

    raster.create_graph(name, resolution, coordinates, lines)

    return {'url': f'/plots/{name}.png'}
