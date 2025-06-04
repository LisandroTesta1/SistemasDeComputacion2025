# SistemasDeComputacion2025

¿Qué es exactamente un módulo del núcleo? Los módulos son fragmentos de código que se pueden cargar y descargar en el kernel según se requiera. Extienden la funcionalidad del kernel sin necesidad de reiniciar el sistema. Por ejemplo, un tipo de módulo es el controlador de dispositivo, que permite que el núcleo acceda al hardware conectado al sistema. Sin módulos, tendríamos que construir kernels monolíticos y agregar nuevas funciones directamente en la imagen del kernel. Además de tener kernels más grandes, esto tiene la desventaja de requerir que reconstruyamos y reiniciemos el kernel cada vez que queramos una nueva funcionalidad.

Desafío #1 
- ¿Qué es checkinstall y para qué sirve?
- ¿Se animan a usarlo para empaquetar un hello world ? 
- Revisar la bibliografía para impulsar acciones que permitan mejorar la seguridad del kernel, concretamente: evitando cargar módulos que no estén firmados. rootkits ? 

Desafío #2
- Debe tener respuestas precisas a las siguientes preguntas y sentencias:
- ¿ Qué funciones tiene disponible un programa y un módulo ?
- Espacio de usuario o espacio del kernel.
- Espacio de datos.
- Drivers. Investigar contenido de /dev.
