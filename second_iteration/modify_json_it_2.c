#include <stdio.h>
#include <stdlib.h>
#include <jansson.h>

// Declaración de función externa (ensamblador)
extern int increment_float(float value);

int main() {
    json_t *root;
    json_error_t error;

    root = json_load_file("gdp_data.json", 0, &error);
    if (!root) {
        fprintf(stderr, "Error al leer JSON: %s\n", error.text);
        return 1;
    }

    json_t *date_value = json_object_get(root, "date");
    if (!json_is_number(date_value)) {
        fprintf(stderr, "Campo 'date' no válido\n");
        json_decref(root);
        return 1;
    }

    float date_float = (float)json_number_value(date_value);
    int new_date = increment_float(date_float);

    json_object_set_new(root, "date", json_integer(new_date));

    if (json_dump_file(root, "gdp_data_modified.json", JSON_INDENT(4)) != 0) {
        fprintf(stderr, "Error al escribir JSON modificado\n");
        json_decref(root);
        return 1;
    }

    json_decref(root);
    printf("El año ha sido incrementado a: %d\n", new_date);
    return 0;
}
