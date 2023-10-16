from flask import Flask, request
import os

import raster


app = Flask(__name__)


@app.route("/raster", methods=['POST'])
def create_plot():
    resolution = request.json['resolution']
    edges = request.json['edges']
    polies = request.json['polies']
    curves = request.json['curves']

    coordinates = {}
    for k, c in request.json['coordinates'].items():
        coordinates[k] = raster.Coordinate(c['x'], c['y'])

    raster.create_graph(resolution, coordinates, edges, curves, polies)

    return {'msg': 'success'}

@app.route("/plots", methods=['GET'])
def list_plots():
    l = os.listdir('./plots')

    return {'plots': l}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 5000), debug=True)