## @file gini_flow_it_2.py
#  @brief Consulta y gestión interactiva del índice de Gini de Argentina (2006–2020) usando la API del Banco Mundial.
#  @details Este script en Python obtiene el índice de Gini para Argentina, guarda el resultado en un archivo JSON,
#           y permite avanzar año por año (hasta 2020) llamando a un programa en C que modifica el valor del año.

import requests
import json
import subprocess
import os

## Año inicial de consulta
START_YEAR = 2006
## Año máximo permitido
MAX_YEAR = 2020
## Nombre del archivo original JSON
JSON_ORIGINAL = "gdp_data.json"
## Nombre del archivo JSON modificado por el programa en C
JSON_MODIFIED = "gdp_data_modified.json"

##
# @brief Obtiene datos del índice de Gini desde la API del Banco Mundial.
# @param year Año para el cual se desea consultar el índice de Gini.
# @param filename Nombre del archivo JSON donde se guardarán los datos.
# @return Diccionario con los datos del índice de Gini o None si no se encontraron datos válidos.
def fetch_gini(year, filename=JSON_ORIGINAL):
    url = f"https://api.worldbank.org/v2/country/ar/indicator/SI.POV.GINI?date={year}&format=json"
    response = requests.get(url)
    data = response.json()

    if data and isinstance(data, list) and len(data) > 1 and data[1]:
        entry = data[1][0]
        result = {
            "indicator": entry.get("indicator", {}).get("id", "unknown"),
            "indicator_name": entry.get("indicator", {}).get("value", "Índice Gini"),
            "country": entry.get("country", {}).get("value", "Argentina"),
            "date": int(entry.get("date", year)),
            "value": entry.get("value", None)
        }

        with open(filename, "w") as f:
            json.dump(result, f, indent=4)

        return result
    else:
        print(f"No se encontraron datos válidos para el año {year}.")
        return None

##
# @brief Imprime los datos del índice de Gini en formato legible.
# @param gini_data Diccionario con los datos del índice Gini.
def print_gini_info(gini_data):
    print("\n--- Datos del Índice de Gini ---")
    print(json.dumps(gini_data, indent=4, ensure_ascii=False))

##
# @brief Llama al programa en C encargado de modificar el archivo JSON e incrementar el año.
def call_c_modifier():
    print("\n→ Ejecutando programa en C para incrementar el año...")
    subprocess.run(["./modify_json"])

##
# @brief Lee el archivo JSON modificado y obtiene el nuevo valor del campo "date".
# @param filename Nombre del archivo modificado.
# @return Año (entero) leído desde el archivo o None si no se encuentra.
def read_modified_date(filename=JSON_MODIFIED):
    if not os.path.exists(filename):
        print("Archivo modificado no encontrado.")
        return None
    with open(filename, "r") as f:
        data = json.load(f)
    return data.get("date", None)

##
# @brief Reinicia el proceso desde el año 2006.
# @return Diccionario con los datos del índice Gini del año inicial.
def reiniciar():
    print(f"\n Reiniciando desde el año {START_YEAR}...")
    return fetch_gini(START_YEAR)

##
# @brief Función principal del programa. Maneja el flujo de ejecución y la interacción con el usuario.
if __name__ == "__main__":
    
    current_data = fetch_gini(START_YEAR)
    if current_data:
        print_gini_info(current_data)

        while True:
            user_input = input('\nEscribe "siguiente" para continuar, "reiniciar" para volver al 2006 o "salir" para terminar: ').strip().lower()

            if user_input == "salir":
                print("Saliendo del programa.")
                break

            elif user_input == "reiniciar":
                current_data = reiniciar()
                if current_data:
                    print_gini_info(current_data)

            elif user_input == "siguiente":
                if current_data["date"] >= MAX_YEAR:
                    print(f"\n Ya alcanzaste el año límite ({MAX_YEAR}).")
                    next_action = input('Escribe "reiniciar" para volver a 2006 o "salir" para terminar: ').strip().lower()
                    if next_action == "reiniciar":
                        current_data = reiniciar()
                        if current_data:
                            print_gini_info(current_data)
                    elif next_action == "salir":
                        print("Saliendo del programa.")
                        break
                    else:
                        print("Comando no reconocido.")
                        continue
                else:
                    call_c_modifier()
                    new_year = read_modified_date()
                    if new_year and new_year <= MAX_YEAR:
                        new_data = fetch_gini(new_year)
                        if new_data:
                            current_data = new_data
                            print_gini_info(current_data)
                        else:
                            print("No se pudo obtener información para el nuevo año.")
                    else:
                        print(f"Año fuera de rango o no válido (>{MAX_YEAR}).")
                        break

            else:
                print("Comando no reconocido. Usa 'siguiente', 'reiniciar' o 'salir'.")
