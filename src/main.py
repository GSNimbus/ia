# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from WeatherService import estimate_solar_conditions, get_neighborhoods_by_location

# app = Flask(__name__)
# CORS(app)

# @app.route('/solar-conditions', methods=['GET'])
# def get_solar_conditions_by_city():
#     lat = request.args.get('lat', type=float, default=-23.510411)  
#     log = request.args.get('log', type=float, default=-46.527280)  

#     if not lat or not log:
#         return jsonify({"error": "Parâmetros 'cidade' e 'estado' são obrigatórios"}), 400

#     try:
#         neighborhoods = get_neighborhoods_by_location(lat, log)
#         logging_info = f"Request para Nominatim com lat={lat}, log={log} e neighborhoods={neighborhoods}"
#         print(logging_info)  # Log the request information
#         data = estimate_solar_conditions(lat, log)
#         return jsonify({"data" : data, 'neighborhoods': neighborhoods})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/neighborhoods', methods=['GET'])
# def get_neighborhoods():
#     lat = request.args.get('lat', type=float, default=-23.510411)  
#     log = request.args.get('log', type=float, default=-46.527280)  

#     if not lat or not log:
#         return jsonify({"error": "Parâmetros 'lat' e 'log' são obrigatórios"}), 400

#     try:
#         neighborhoods = get_neighborhoods_by_location(lat, log)
#         return jsonify(neighborhoods)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)

from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Simulando um Enum de tipo de alerta
RISCO_ALERTA = ["CHUVA", "VENTO", "CALOR", "FRIO", "UMIDADE"]

# Endpoint /alerta
@app.route('/alerta', methods=['POST'])
def gerar_alerta():
    previsao = request.get_json()

    # Você pode acessar os campos se quiser fazer lógica real:
    temperatura = previsao.get("temperature2M")
    precipitacao = previsao.get("precipitation")
    umidade = previsao.get("relativeHumidity2M")
    vento = previsao.get("windSpeed10M")

    # Gerando dados aleatórios para o alerta
    alerta = {
        "risco": random.choice(RISCO_ALERTA),
        "tipo": random.choice(["BAIXO_RISCO", "MEDIO_RISCO", "ALTO_RISCO"]),
        "mensagem": random.choice([
            "Atenção: chuvas moderadas previstas.",
            "Ventos fortes podem ocorrer.",
            "Temperaturas elevadas ao longo do dia.",
            "Umidade do ar abaixo do ideal."
        ])
        # idBairro não incluído, conforme solicitado
    }

    return jsonify(alerta), 200

# Rodar o servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
