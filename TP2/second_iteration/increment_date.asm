    ## @file increment_float.asm
    ## @brief Rutina en ensamblador x86 que convierte un número en coma flotante a entero y lo incrementa.
    ## @details Esta función toma un número `float` como parámetro (dentro de stack), lo convierte a `int`,
    ##          lo incrementa en 1 y devuelve el resultado en `EAX`. Se utiliza en conjunto con el programa en C.

    .globl increment_float               ## Declaración global para el linker
    .type increment_float, @function    ## Indicamos que es una función

    ## @brief Función que incrementa un número flotante.
    ## @param [in] float valor en coma flotante pasado por la pila (posición 8(%ebp)).
    ## @return entero incrementado (en EAX).
increment_float:
    push    %ebp                        ## Guardar base pointer actual
    mov     %esp, %ebp                  ## Crear nuevo stack frame

    sub     $8, %esp                    ## Reservar espacio en la pila

    fld     DWORD PTR 8(%ebp)           ## Cargar float del argumento (primer parámetro)
    fistp   DWORD PTR -4(%ebp)          ## Convertir float a entero y almacenarlo en la pila

    mov     eax, DWORD PTR -4(%ebp)     ## Mover entero convertido a EAX
    add     eax, 1                      ## Incrementar en 1

    leave                              ## Restaurar stack frame (mov esp, ebp + pop ebp)
    ret                                ## Retornar (EAX contiene el resultado)
