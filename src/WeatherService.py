import unicodedata
import datetime
import logging
import requests
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def estimate_solar_conditions(cidade, estado):
    resposta = latLotCidade(nomeCidade=cidade, estado=estado)

    latitude = resposta.get('latitude')
    longitude = resposta.get('longitude')
    url = "https://api.open-meteo.com/v1/forecast"
    today = datetime.date.today()
    start_date = (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d")  # Incluir o dia anterior
    end_date = today.strftime("%Y-%m-%d")
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ["temperature_2m", "shortwave_radiation"],
        "timezone": "America/Sao_Paulo",
        "start_date": start_date,
        "end_date": end_date
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

def get_neighborhoods_by_location(lat, log):
    """Obtém os bairros próximos a uma localização utilizando a API Nominatim."""
    url = 'https://nominatim.openstreetmap.org/reverse'
    params = {
        "lat": lat,
        "lon": log,
        "format": "jsonv2",
        "addressdetails": 1,
        "extratags": 1
    }
    headers = {
        "User-Agent": "nimbus-ai/1.0 gustavodiasdsc@gmail.com"
    }
    logger.info(f"Request para Nominatim com params={params} e headers={headers}")
    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        logger.error(f"Erro {response.status_code} na API de geolocalização.")
        return {"error": "Falha no request"}, response.status_code

    response_data = response.json()
    data = {}
    data['suburb'] = response_data.get('address', {}).get('suburb', None)
    return data

def latLotCidade(nomeCidade, estado):
    """Obtém a latitude e longitude de uma cidade utilizando a API Open-Meteo."""
    def remover_acentos_inner(texto):
        return ''.join(
            c for c in unicodedata.normalize('NFD', texto)
            if unicodedata.category(c) != 'Mn'
        ).lower()

    list_cidades = str(nomeCidade).split(' ')
    novoNomeCidade = remover_acentos_inner('+'.join(list_cidades))
    estado_normalizado = remover_acentos_inner(estado)

    url = f"https://geocoding-api.open-meteo.com/v1/search?name={novoNomeCidade}&count=10&language=pt&format=json"
    response = requests.get(url)

    if response.status_code != 200:
        logger.error("Falha ao fazer o request para a API de geolocalização.")
        return {"error": "Falha ao fazer o request para a API de geolocalização"}, response.status_code

    data = response.json()
    results = data.get('results', [])

    for result in results:
        if result.get('country') == 'Brasil':
            admin_fields = [
                remover_acentos_inner(result.get('admin1', '').lower()),
                remover_acentos_inner(result.get('admin2', '').lower()),
                remover_acentos_inner(result.get('admin3', '').lower()),
                remover_acentos_inner(result.get('admin4', '').lower())
            ]

            if estado_normalizado in admin_fields:
                latitude = result.get('latitude')
                longitude = result.get('longitude')
                return {'latitude': latitude, 'longitude': longitude}

    logger.error("Local não encontrado com os parâmetros fornecidos.")
    return {"error": "Local não encontrado com os parâmetros fornecidos"}, 404
