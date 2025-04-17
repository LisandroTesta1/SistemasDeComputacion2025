// archivo: modify_json.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <jansson.h> // necesitas instalar libjansson-dev

int main() {
    json_t *root;
    json_error_t error;

    root = json_load_file("gdp_data.json", 0, &error);
    if (!root) {
        fprintf(stderr, "Error leyendo JSON: %s\n", error.text);
        return 1;
    }

    // Obtener y aumentar "date"
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

    json_decref(root);
    printf("Archivo modificado y guardado como: gdp_data_modified.json\n");
    return 0;
}
