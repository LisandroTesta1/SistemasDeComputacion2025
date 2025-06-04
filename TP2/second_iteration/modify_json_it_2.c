/**
 * @file modify_json_float.c
 * @brief Programa en C que lee un archivo JSON, incrementa el campo "date" usando una función en ensamblador para x86,
 * @details El campo "date" es leído como número (float), se incrementa mediante una función externa en ensamblador,
 *          y se guarda el resultado como entero en un nuevo archivo JSON.
 */

 #include <stdio.h>
 #include <stdlib.h>
 #include <jansson.h>
 
 /// @brief Función externa en ensamblador que incrementa un valor float.
 /// @param value Valor en coma flotante a incrementar.
 /// @return Valor incrementado como entero.
 extern int increment_float(float value);
 
 /**
  * @brief Función principal del programa.
  * @return 0 si se ejecuta correctamente, 1 en caso de error.
  */
 int main() {
     json_t *root;
     json_error_t error;
 
     // Cargar archivo JSON
     root = json_load_file("gdp_data.json", 0, &error);
     if (!root) {
         fprintf(stderr, "Error al leer JSON: %s\n", error.text);
         return 1;
     }
 
     // Obtener valor del campo "date"
     json_t *date_value = json_object_get(root, "date");
     if (!json_is_number(date_value)) {
         fprintf(stderr, "Campo 'date' no válido\n");
         json_decref(root);
         return 1;
     }
 
     // Convertir a float y llamar a función externa
     float date_float = (float)json_number_value(date_value);
     int new_date = increment_float(date_float);
 
     // Actualizar campo "date" con el nuevo valor
     json_object_set_new(root, "date", json_integer(new_date));
 
     // Guardar el archivo modificado
     if (json_dump_file(root, "gdp_data_modified.json", JSON_INDENT(4)) != 0) {
         fprintf(stderr, "Error al escribir JSON modificado\n");
         json_decref(root);
         return 1;
     }
 
     // Liberar recursos y finalizar
     json_decref(root);
     printf("El año ha sido incrementado a: %d\n", new_date);
     return 0;
 }
 