from flask import Flask, request, jsonify
from shapely.geometry import shape, Point
import json

app = Flask(__name__)

@app.route('/check_coordinates', methods=['POST'])
def check_coordinates():
    if request.method == 'POST':
        try:
            # Get the GeoJSON and coordinates from the request
            data = request.json
            geojson = data.get('geojson')
            coordinates = data.get('coordinates')
            # Validate input
            if not geojson or not coordinates:
                return jsonify({"error": "Missing geojson or coordinates"}), 400

            # Create polygon from GeoJSON
            polygon = shape(geojson['features'][0]['geometry'])

            # Create point from coordinates
            point = Point(coordinates)

            # Check if point is inside polygon
            is_inside = polygon.contains(point)

            return jsonify({"inside_polygon": is_inside})
        except Exception as e:
            return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
