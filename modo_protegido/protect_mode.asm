[org 0x7C00]          ; Dirección típica para bootloaders

;------------------------Modo Real---------------------;
[bits 16]             ; Estamos en modo real

CODE_16:
    cli               ; Desactivar interrupciones
    
    ; Activar el bit PE (Protection Enable) en CR0
    mov eax, cr0      ; Se carga el registro de control cr0 en eax
    or eax, 0x1       ; Se activo el bit 0 que habilita el modo protegido
    mov cr0, eax      ; Almacena el valor de eax en cr0

    jmp CODE_32       ; Salto a modo protegido

;----------------------Modo Protegido-------------------;
[bits 32]           ; Estamos en modo protegido

CODE_32:
;--------------------------------------;
;-------Codigo en modo protegio--------;
;--------------------------------------;