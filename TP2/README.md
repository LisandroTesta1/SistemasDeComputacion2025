# SistemasDeComputacion2025

Consigna:

Utilizando la API del Banco Mundial para obtener información sobre el índice GINI de Argentina

- En una primera iteración, realizar un programa en python que muestre el índice GINI de argentina para los años comprendidos entre 2006 y 2020, luego de haber generado un archivo JSON con la información obtenida de la API, un año por vez. Ademas, diseñar un programa en c que aumente en uno el año del dato mostrado, devolviendo el archivo JSON modificado al programa en python para que el mismo obtenga y muestre los datos para el nuevo dato del año.

- En una segunda iteración, agregar un programa en assembler, llamado por el programa en c, para que realice la modificación del dato del año del json generado por el programa en python.


Comandos para consola necesarios:

- Primera iteración

Compilar:
	gcc modify_json.c -o modify_json -ljansson

Ejecutar:
	python3 gini_flow.py

- Segunda iteración

Compilar:
	nasm -f elf32 -g -F dwarf increment_date.asm -o increment_date.o

Enlazar:
	gcc -m32 -g -o modify_json_it_2 modify_json_it_2.c increment_date.o -ljansson
	
Ejecutar:
	python3 gini_flow_it_2.py
