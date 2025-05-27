from flask import Flask, jsonify, request
from flask_cors import CORS
from WeatherService import estimate_solar_conditions, get_neighborhoods_by_location

app = Flask(__name__)
CORS(app)

@app.route('/solar-conditions', methods=['GET'])
def get_solar_conditions_by_city():
    cidade = 'São Paulo'  # Default city
    estado = 'São Paulo'

    if not cidade or not estado:
        return jsonify({"error": "Parâmetros 'cidade' e 'estado' são obrigatórios"}), 400

    try:
        data = estimate_solar_conditions(cidade, estado)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/neighborhoods', methods=['GET'])
def get_neighborhoods():
    # lat = request.args.get('lat')
    # log = request.args.get('log')
    #-23.510411, -46.527280
    lat = -23.510411
    log = -46.527280

    if not lat or not log:
        return jsonify({"error": "Parâmetros 'lat' e 'log' são obrigatórios"}), 400

    try:
        neighborhoods = get_neighborhoods_by_location(lat, log)
        return jsonify(neighborhoods)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

