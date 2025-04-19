## @file gini_flow_it_2.py
#  @brief Programa principal que obtiene el índice de Gini desde la API del Banco Mundial y permite navegar año a año.
#  @details El programa guarda los datos en JSON, llama a un programa en C para incrementar el año, y permite al usuario avanzar, reiniciar o salir del flujo.

import requests
import json
import subprocess
import os

## @brief Año de inicio del flujo.
START_YEAR = 2006

## @brief Año máximo permitido.
MAX_YEAR = 2020

## @brief Archivo JSON original donde se guarda el primer resultado.
JSON_ORIGINAL = "gdp_data.json"

## @brief Archivo JSON modificado por el programa en C.
JSON_MODIFIED = "gdp_data_modified.json"

## @brief Obtiene datos del índice de Gini desde la API del Banco Mundial para un año específico.
#  @param year Año para el que se desea consultar el índice.
#  @param filename Nombre del archivo donde se guardarán los datos.
#  @return Un diccionario con los datos del índice de Gini o None si no se encuentran datos.
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

## @brief Muestra por consola los datos del índice de Gini.
#  @param gini_data Diccionario con la información del índice de Gini.
def print_gini_info(gini_data):
    print("\n--- Datos del Índice de Gini ---")
    print(json.dumps(gini_data, indent=4, ensure_ascii=False))

## @brief Ejecuta el programa en C encargado de incrementar el campo "date" en el archivo JSON.
def call_c_modifier():
    print("\n→ Ejecutando programa en C para incrementar el año...")
    subprocess.run(["./modify_json_it_2"])

## @brief Lee el valor del campo "date" del archivo JSON modificado.
#  @param filename Nombre del archivo modificado.
#  @return El año leído del archivo o None si no se encuentra el archivo o el campo.
def read_modified_date(filename=JSON_MODIFIED):
    if not os.path.exists(filename):
        print("Archivo modificado no encontrado.")
        return None
    with open(filename, "r") as f:
        data = json.load(f)
    return data.get("date", None)

## @brief Reinicia el flujo desde el año inicial.
#  @return Diccionario con los datos del índice de Gini del año inicial.
def reiniciar():
    print(f"\n Reiniciando desde el año {START_YEAR}...")
    return fetch_gini(START_YEAR)

## @brief Función principal que ejecuta el flujo interactivo.
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
