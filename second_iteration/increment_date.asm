    .globl increment_float
    .type increment_float, @function

increment_float:
    push    %ebp
    mov     %esp, %ebp

    sub     $8, %esp             # espacio en pila

    fld     DWORD PTR 8(%ebp)    # cargar float
    fistp   DWORD PTR -4(%ebp)   # convertir a int

    mov     eax, DWORD PTR -4(%ebp) # mover a eax
    add     eax, 1               # sumar uno

    leave
    ret
