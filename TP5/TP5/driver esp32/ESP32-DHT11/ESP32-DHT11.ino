#include "DHT.h"

// Pin de datos conectado al DHT11 definido para el puerto GPIO4 de la esp32
#define DHTPIN 4
// Definimos el tipo de sensor       
#define DHTTYPE DHT11  

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  //Se lee los datos del sensor y se guardan
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  // Verificamos si la lectura ha fallado
  if (isnan(h) || isnan(t)) {
    Serial.println("Error al leer del sensor");
    return;
  }

  // Enviamos los datos como "temperatura,humedad"
  Serial.print(t);
  Serial.print(",");
  Serial.println(h);

  // Esperamos 1 segundo
  delay(1000);  
}
