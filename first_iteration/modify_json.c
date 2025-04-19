/**
 * @file modify_json_it_2.c
 * @brief Programa en C que lee un archivo JSON, incrementa el valor del campo "date" y guarda el resultado en otro archivo.
 * @details Este programa utiliza la biblioteca Jansson para manipular archivos JSON. Lee "gdp_data.json", incrementa el campo "date"
 *          y guarda el resultado en "gdp_data_modified.json".
 */

 #include <stdio.h>
 #include <stdlib.h>
 #include <string.h>
 #include <jansson.h>
 
 /**
  * @brief Función principal del programa.
  * 
  * @return int Código de salida del programa (0 si se ejecutó correctamente, otro valor si hubo errores).
  */
 int main() {
     json_t *root;             ///< Objeto raíz del archivo JSON.
     json_error_t error;       ///< Objeto para almacenar errores de lectura del JSON.
 
     // Cargar archivo JSON original
     root = json_load_file("gdp_data.json", 0, &error);
     if (!root) {
         fprintf(stderr, "Error leyendo JSON: %s\n", error.text);
         return 1;
     }
 
     // Obtener e incrementar el valor del campo "date"
     json_t *date = json_object_get(root, "date");
     if (json_is_integer(date)) {
         int year = json_integer_value(date);
         json_object_set_new(root, "date", json_integer(year + 1));
     }
 
     // Guardar el archivo modificado
     if (json_dump_file(root, "gdp_data_modified.json", JSON_INDENT(4)) != 0) {
         fprintf(stderr, "Error guardando archivo JSON\n");
         return 1;
     }
 
     json_decref(root); // Liberar memoria del objeto JSON
     printf("Archivo modificado y guardado como: gdp_data_modified.json\n");
     return 0;
 }
 