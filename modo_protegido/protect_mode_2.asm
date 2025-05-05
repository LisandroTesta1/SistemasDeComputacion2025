[org 0x7C00]
[bits 16]

;-------------------------------------------------------------------;
;                   Modo Real (bits 16)                        ;
;-------------------------------------------------------------------;
CODE_16:
    cli               ; Desactivar interrupciones
    
    ; Activar el bit PE (Protection Enable) en CR0
    mov eax, cr0      ; Se carga el registro de control cr0 en eax
    or eax, 0x1       ; Se activo el bit 0 que habilita el modo protegido
    mov cr0, eax      ; Almacena el valor de eax en cr0

    lgdt [gdt_descriptor]

    jmp CODE_32       ; Salto a modo protegido

;-------------------------------------------------------------------;
;       GDT - Código y datos en regiones separadas de memoria       ;
;-------------------------------------------------------------------;
gdt_start:
    ; Descriptor nulo
    dq 0x0000000000000000

    ; Descriptor de código: base=0x00000000, límite=0x0FFF (4 KB)
    dw 0x0FFF              ; Límite 15:0
    dw 0x0000              ; Base 15:0
    db 0x00                ; Base 23:16
    db 10011010b           ; Acceso: ejecutable, solo lectura
    db 01000000b           ; Flags: 32-bit, sin granulación
    db 0x00                ; Base 31:24

    ; Descriptor de datos: base=0x00100000, límite=0x0FFF (4 KB)
    dw 0x0FFF              ; Límite 15:0
    dw 0x0000              ; Base 15:0
    db 0x10                ; Base 23:16 = 0x00100000 >> 16
    db 10000000b           ; Acceso: datos, solo lectura
    db 01000000b           ; Flags: 32-bit, sin granulación
    db 0x00                ; Base 31:24

gdt_end:

gdt_descriptor:
    dw gdt_end - gdt_start - 1
    dd gdt_start

;-------------------------------------------------------------------;
;                   Modo protegido (bits 32)                        ;
;-------------------------------------------------------------------;
[bits 32]
CODE_32:
    ; Cargar selector del segmento de datos (0x10)
    mov ax, 0x10
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax
    mov esp, 0x00100000 + 0x0F00

    ; Intentar escribir en memoria dentro del segmento de solo lectura
    mov dword [0x00100000], 0xDEADBEEF ; <-- Esta instrucción no debería estar permitida lógicamente

hang:
    jmp hang
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Boot sector signature
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
times 510 - ($ - $$) db 0
dw 0xAA55
