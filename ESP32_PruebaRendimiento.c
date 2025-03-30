unsigned long tiempoInicio;   // Referencia del tiempo de inicio del programa.
unsigned long tiempoFin;      // Tiempo al finalizar el programa.
unsigned long duracion;       // Tiempo total de ejecucion del bucle una vez.

// Delay que no depende de la frecuencia de trabajo de la cpu, para 80MHz y 1960000 ciclos, genera un delay de 500 milisegundos
void delayCpu(uint32_t ciclos) {
    volatile uint32_t count = 0;
    while (count < ciclos) {
        count++;
    }
}

// Delay de 5 segundos para una frecuencia de 80MHz
void delayCpu2(){
    delayCpu(1960000);
    delayCpu(1960000);
    delayCpu(1960000);
    delayCpu(1960000);
    delayCpu(1960000);
    delayCpu(1960000);
    delayCpu(1960000);
    delayCpu(1960000);
    delayCpu(1960000);
    delayCpu(1960000);
}

// Configuracion para el pin del led y velocidad para la comunicacion serial
void setup() {
    pinMode(2, OUTPUT);
    Serial.begin(115200);
}

// Funcion de parpadeo para el led
void loop() {

    tiempoInicio = micros();              // Guarda el tiempo antes de ejecutar el código

    digitalWrite(2, HIGH);                // Enciende el LED
  
    delayCpu2();                          // Delay de 5 segundos
  
    digitalWrite(2, LOW);                 // Apaga el LED

    delayCpu2();                          // Delay de 5 segundos

    tiempoFin = micros();                 // Guarda el tiempo después de ejecutar el código
  
    duracion = tiempoFin - tiempoInicio;  // Calcula la duración

    Serial.print("Frecuencia de la cpu actual: ");
    Serial.print(getCpuFrequencyMhz());   // Muestra la frecuencia en MHz
    Serial.println(" MHz");
    
    Serial.print("Tiempo de ejecucion: ");
    Serial.print(duracion/1000);          // Muestra el tiempo de ejecucion en milisegundos
    Serial.println(" milisegundos");

    delay(10);                            // Pequeño delay para evitar saturación en el puerto serie
}