from flask import Flask, request
import os

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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 5000), debug=True)