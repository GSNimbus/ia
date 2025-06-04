from flask import Flask, request, jsonify
from predictor import predict_precipitation
import random
from predictor import predict_precipitation # Importa a nova função

app = Flask(__name__)

# Simulando um Enum de tipo de alerta
RISCO_ALERTA = ["CHUVA", "VENTO", "CALOR", "FRIO", "UMIDADE"] # Mantenha se ainda for usar para outros riscos

# Endpoint /alerta
@app.route('/alerta', methods=['POST'])
def gerar_alerta():
    previsao_api_data = request.get_json()

    if not previsao_api_data:
        return jsonify({"error": "Request body não pode ser vazio e deve ser JSON"}), 400

    # Chama a função de predição do modelo
    resultado_precipitacao = predict_precipitation(previsao_api_data)

    if "error" in resultado_precipitacao:
        # Se houve erro na predição, retorna o erro
        return jsonify(resultado_precipitacao), 400 # Ou 500 dependendo do erro

    precipitacao_prevista = resultado_precipitacao.get("predicted_precipitation")

    # Lógica para determinar o alerta com base na precipitação prevista
    # Esta é uma lógica de exemplo, ajuste conforme necessário
    risco_calculado = "CHUVA" # Default para chuva se houver precipitação
    tipo_alerta_calculado = "BAIXO_RISCO"
    print(precipitacao_prevista)
    mensagem_alerta = f"Previsão de precipitação: {precipitacao_prevista[0]:.2f} mm."

    if precipitacao_prevista is None: # Segurança caso algo inesperado ocorra
        risco_calculado = "INDETERMINADO"
        tipo_alerta_calculado = "INDETERMINADO"
        mensagem_alerta = "Não foi possível determinar a precipitação."
    elif precipitacao_prevista > 10: # Exemplo: mais de 10mm é alto risco
        tipo_alerta_calculado = "ALTO_RISCO"
        mensagem_alerta = f"Atenção: Chuva forte prevista ({precipitacao_prevista:.2f} mm)."
    elif precipitacao_prevista > 5: # Exemplo: mais de 5mm é médio risco
        tipo_alerta_calculado = "MEDIO_RISCO"
        mensagem_alerta = f"Atenção: Chuva moderada prevista ({precipitacao_prevista:.2f} mm)."
    elif precipitacao_prevista > 3: # Qualquer precipitação acima de 0
        tipo_alerta_calculado = "BAIXO_RISCO"
        mensagem_alerta = f"Previsão de chuva leve ({precipitacao_prevista:.2f} mm)."
    else: # Sem precipitação prevista
        risco_calculado = "SEM_CHUVA" # Ou outro indicador
        tipo_alerta_calculado = "SEM_RISCO_CHUVA"
        mensagem_alerta = "Sem previsão de chuva."
        # Aqui você poderia adicionar lógica para outros tipos de alerta (vento, calor, etc.)
        # usando os dados de previsao_api_data e random.choice como antes, se desejar.


    # Montando o alerta final
    alerta = {
        "risco": risco_calculado,
        "tipo": tipo_alerta_calculado,
        "mensagem": mensagem_alerta,
        "debug_info_precipitacao": float(precipitacao_prevista) if precipitacao_prevista is not None else None
    }

    # Você pode adicionar outros dados aleatórios aqui se ainda precisar deles
    # para outros tipos de risco não cobertos pelo modelo de precipitação.
    # Exemplo:
    # if risco_calculado not in ["CHUVA", "SEM_CHUVA"]:
    #     alerta["risco"] = random.choice(RISCO_ALERTA) # Escolhe outros riscos
    #     alerta["tipo"] = random.choice(["BAIXO_RISCO", "MEDIO_RISCO", "ALTO_RISCO"])
    #     alerta["mensagem"] = random.choice([
    #         "Ventos fortes podem ocorrer.",
    #         "Temperaturas elevadas ao longo do dia.",
    #         "Umidade do ar abaixo do ideal."
    #     ])

    return jsonify(alerta), 200

# Rodar o servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
