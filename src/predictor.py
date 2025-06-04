import pickle
import pandas as pd
from datetime import datetime
import os

# Define o caminho para o arquivo do modelo
# O script está em /home/gustavo/gsnimbus/ia/src/
# O modelo está em /home/gustavo/gsnimbus/ia/modelo_precipitacao.pkl
MODEL_FILENAME = "modelo_precipitacao.pkl"
# Navega um diretório acima de 'src' para chegar à raiz do projeto 'ia'
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(PROJECT_ROOT, MODEL_FILENAME)

model = None
try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    print(f"Modelo {MODEL_FILENAME} carregado com sucesso de {MODEL_PATH}")
except FileNotFoundError:
    print(f"ERRO CRÍTICO: Arquivo do modelo não encontrado em {MODEL_PATH}. Verifique o caminho e o nome do arquivo.")
except Exception as e:
    print(f"ERRO CRÍTICO: Falha ao carregar o modelo {MODEL_FILENAME} de {MODEL_PATH}. Erro: {e}")

def predict_precipitation(api_data: dict):
    """
    Prevê a precipitação com base nos dados da API e features de tempo.

    Args:
        api_data (dict): Um dicionário contendo os dados da API.
                         Esperado ter chaves: "temperature2_m", "relative_humidity2_m", "wind_speed10_m".

    Returns:
        dict: Um dicionário com a precipitação prevista ou uma mensagem de erro.
              Ex: {"predicted_precipitation": 0.5} ou {"error": "Mensagem de erro"}
    """
    if model is None:
        return {"error": "Modelo de previsão não está carregado. Verifique os logs do servidor."}

    try:
        # Extrair dados da API
        temperatura = api_data.get("temperature2_m")
        umidade = api_data.get("relative_humidity2_m")
        vento = api_data.get("wind_speed10_m")

        if temperatura is None or umidade is None or vento is None:
            missing_fields = []
            if temperatura is None: missing_fields.append("temperature2_m")
            if umidade is None: missing_fields.append("relative_humidity2_m")
            if vento is None: missing_fields.append("wind_speed10_m")
            return {"error": f"Dados de entrada incompletos. Campos obrigatórios faltando: {', '.join(missing_fields)}"}

        # Criar features de tempo
        now = datetime.now()
        mes = now.month
        dia_do_ano = now.timetuple().tm_yday
        hora_do_dia = now.hour

        # Preparar os dados para o modelo
        # A ordem e os nomes das colunas devem ser EXATAMENTE os mesmos que o modelo espera.
        # Suposição de features e ordem:
        feature_names = ['temperatura_ar_c', 'umidade_relativa_pct', 'vento_velocidade_ms', 'mes', 'dia_do_ano', 'hora_do_dia']
        
        input_values = [[
            float(temperatura),
            float(umidade),
            float(vento),
            int(mes),
            int(dia_do_ano),
            int(hora_do_dia)
        ]]
        
        input_df = pd.DataFrame(input_values, columns=feature_names)

        # Fazer a predição
        # A predição pode ser um array numpy, então pegamos o primeiro elemento.
        prediction_result = model.predict(input_df)
        
        # O resultado da predição pode ser um array, pegue o valor escalar se apropriado
        predicted_value = prediction_result[0] if hasattr(prediction_result, '__iter__') else prediction_result

        return {"predicted_precipitation": predicted_value}

    except ValueError as ve:
        print(f"Erro de valor ao preparar dados para predição: {ve}")
        return {"error": f"Erro ao converter dados de entrada: {ve}. Verifique se os valores são numéricos."}
    except Exception as e:
        print(f"Erro inesperado durante a predição: {e}")
        return {"error": f"Erro inesperado durante a predição: {e}"}

if __name__ == '__main__':
    # Exemplo de como usar a função (para teste local)
    print("\n--- Testando a função predict_precipitation ---")
    if model is not None:
        sample_api_data_ok = {
            "temperature2_m": 22.5,
            "relative_humidity2_m": 70.0,
            "wind_speed10_m": 5.0
        }
        resultado_ok = predict_precipitation(sample_api_data_ok)
        print(f"Predição com dados OK: {resultado_ok}")

        sample_api_data_parcial = {
            "temperature2_m": 20.0,
            "relative_humidity2_m": 65.0
            # "wind_speed10_m" faltando
        }
        resultado_parcial = predict_precipitation(sample_api_data_parcial)
        print(f"Predição com dados parciais: {resultado_parcial}")
        
        sample_api_data_invalid_type = {
            "temperature2_m": "alta", # Tipo inválido
            "relative_humidity2_m": 70.0,
            "wind_speed10_m": 5.0
        }
        resultado_invalid_type = predict_precipitation(sample_api_data_invalid_type)
        print(f"Predição com tipo de dado inválido: {resultado_invalid_type}")

    else:
        print("Modelo não carregado, não é possível executar os testes de predição.")

    # Teste para verificar o caminho do modelo
    print(f"Caminho absoluto esperado para o modelo: {MODEL_PATH}")
    print(f"O arquivo do modelo existe? {'Sim' if os.path.exists(MODEL_PATH) else 'Não'}")
