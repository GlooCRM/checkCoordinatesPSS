from flask import Flask, request, jsonify
from shapely.geometry import shape, Point, Polygon
import json

app = Flask(__name__)

@app.route('/check_coordinates', methods=['POST'])
def check_coordinates():
    if request.method == 'POST':
        try:
            # Get the GeoJSON and coordinates from the request
            data = request.json
            geojson_str = data.get('geojson')
            coordinates_str = data.get('coordinates')
            
            # Validate input
            if not geojson_str or not coordinates_str:
                return jsonify({"error": "Missing geojson or coordinates"}), 400

            # Parse GeoJSON string
            geojson = json.loads(geojson_str)
            
            # Create polygon from GeoJSON
            polygon = shape(geojson['features'][0]['geometry'])

            # Ensure the polygon is valid
            if not polygon.is_valid:
                polygon = polygon.buffer(0)

            # Parse coordinates string
            try:
                lon,lat = map(float, coordinates_str.split(','))
            except ValueError:
                return jsonify({"error": "Invalid coordinate format"}), 400
            
            # Create point from coordinates (note the order: lon, lat)
            point = Point(lon, lat)

            # Check if point is inside polygon
            is_inside = polygon.contains(point)

            # If not inside, check if it's on the boundary
            if not is_inside:
                is_inside = polygon.touches(point)

            # Additional checks
            is_within = polygon.buffer(1e-7).contains(point)
            distance = point.distance(polygon)

            return jsonify({
                "inside_polygon": is_inside,
                "is_within_buffer": is_within,
                "distance_to_polygon": distance,
                "point": {"lat": lat, "lon": lon},
                "polygon_bounds": polygon.bounds,
                "polygon_area": polygon.area,
                "polygon_valid": polygon.is_valid,
                "polygon_exterior_coords": list(polygon.exterior.coords)
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
