from flask import Flask, jsonify, request
from flask_cors import CORS
from WeatherService import estimate_solar_conditions, get_neighborhoods_by_location

app = Flask(__name__)
CORS(app)

@app.route('/solar-conditions', methods=['GET'])
def get_solar_conditions_by_city():
    lat = request.args.get('lat', type=float, default=-23.510411)  
    log = request.args.get('log', type=float, default=-46.527280)  

    if not lat or not log:
        return jsonify({"error": "Parâmetros 'cidade' e 'estado' são obrigatórios"}), 400

    try:
        neighborhoods = get_neighborhoods_by_location(lat, log)
        logging_info = f"Request para Nominatim com lat={lat}, log={log} e neighborhoods={neighborhoods}"
        print(logging_info)  # Log the request information
        data = estimate_solar_conditions(lat, log)
        return jsonify({"data" : data, 'neighborhoods': neighborhoods})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/neighborhoods', methods=['GET'])
def get_neighborhoods():
    lat = request.args.get('lat', type=float, default=-23.510411)  
    log = request.args.get('log', type=float, default=-46.527280)  

    if not lat or not log:
        return jsonify({"error": "Parâmetros 'lat' e 'log' são obrigatórios"}), 400

    try:
        neighborhoods = get_neighborhoods_by_location(lat, log)
        return jsonify(neighborhoods)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

