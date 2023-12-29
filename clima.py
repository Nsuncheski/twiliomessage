import requests

# Coordenadas para Munro, Vicente López, Buenos Aires, Argentina
lat = -34.519508
lon = -58.516771

# URL del endpoint
url = "https://ws.smn.gob.ar/map_items/forecast/1"

# Parámetros de la solicitud
params = {
    "lat": lat,
    "lon": lon,
    "name": "San Isidro"
}

# Realizar la solicitud GET
response = requests.get(url, params=params)

# Verificar si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Parsear la respuesta JSON
    data = response.json()

    # Acceder a los datos que necesitas
    # Por ejemplo, la información climática actual
    weather_info = data.get("weather")
    print("Información climática actual:")
    print(f"Temperatura: {weather_info.get('temp')}°C")
    print(f"Sensación térmica: {weather_info.get('st')}°C")
    print(f"Humedad: {weather_info.get('humidity')}%")
    # Agrega más campos según tus necesidades

    # También puedes acceder al pronóstico
    forecast_info = data.get("forecast")
    print("\nPronóstico:")
    for forecast_day, forecast_data in forecast_info.get("forecast", {}).items():
        print(f"Día {forecast_day}:")
        print(f"Temperatura mínima: {forecast_data.get('temp_min')}°C")
        print(f"Temperatura máxima: {forecast_data.get('temp_max')}°C")
        # Agrega más campos del pronóstico según tus necesidades

else:
    print(f"Error en la solicitud. Código de estado: {response.status_code}")
    print(response.text)
