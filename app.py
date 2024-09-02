from flask import Flask, request, jsonify
from shapely.geometry import shape, Point
import json

app = Flask(__name__)

# Cargamos el archivo GeoJSON (reemplaza 'tu_archivo.geojson' con la ruta correcta)
with open('tu_archivo.geojson') as f:
    data = json.load(f)
    polygon = shape(data['features'][0]['geometry'])
    print(polygon)

@app.route('/check_coordinates', methods=['GET'])
def check_coordinates():
    if request.method == 'GET':
        try:
            #coordinates = request.json['coordinates']
            coordinates = [-123.1109401,49.02]
            point = Point(coordinates)
            is_inside = polygon.contains(point)
            return jsonify({"inside_polygon": is_inside})
        except Exception as e:
            return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
    