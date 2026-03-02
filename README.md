# hzl_robotics-esp32
**hzl_robotics-esp32** Aquí tienes la traducción al español de la documentación, manteniendo el formato Markdown y la estructura técnica original.

hzl_robotics-esp32
hzl_robotics-esp32 es un framework de Python diseñado para interactuar con un ESP32 a través de USB Serial.

Permite controlar los pines GPIO del ESP32 utilizando una sintaxis de Python limpia y familiar, manteniendo al mismo tiempo una API estilo Arduino.

Este proyecto está diseñado como un **puente pedagógico** entre la programación en Python y el desarrollo de sistemas embebidos.

## 🎯 Propósito

Este framework NO pretende reemplazar el desarrollo de firmware nativo o C++.

En su lugar, está construido para:
- Reducir la barrera de entrada para principiantes.
- Enseñar fundamentos de electrónica sin la complejidad de C++.
- Mantener nombres de funciones estilo Arduino para una transición fluida.
- Permitir la integración con herramientas basadas en PC como OpenCV, bots de Discord, APIs, etc.

El ESP32 actúa como un coprocesador de E/S (I/O), mientras que Python ejecuta la lógica de alto nivel en la computadora.

## 📦 Instalación
```bash
pip install hzl-robotics-esp32
```

## 🚀 Ejemplo

  

```python
from  src.hzl_robotics_esp32  import  ESP32
import  time
import  math

esp32  =  ESP32("COM5")

@esp32.setup
def  setup():
	esp32.pinMode(2, 1)
	esp32.ledcAttach(4, 1000, 8)
	
@esp32.loop
def  loop():
	for  i  in  range(256):
		corrected  =  int((i  /  255) **  2.2  *  255)
		esp32.ledcWrite(4, corrected)
		time.sleep(0.01)

	for  i  in  range(255, -1, -1):
		corrected  =  int((i  /  255) **  2.2  *  255)
		esp32.ledcWrite(4, corrected)
		time.sleep(0.01)
try:
	esp32.start()
	while  True:
		time.sleep(1)
except  KeyboardInterrupt:
	esp32.stop()
```
Este ejemplo controla progresivamente el brillo de un LED usando PWM con corrección gamma.
## 🔧 Funciones de Configuración (Setup)
```python
# Configurar pin
esp32.pinMode(pin, mode)

# Configurar pin PWM
esp32.ledcAttach(pin, freq, res)
```

## 🔁 Funciones de Bucle (Loop)
```python
#digitalRead:
value = esp32.digitalRead(pin)

# digitalWrite:
esp32.digitalWrite(pin, value)

#analogRead:
value = esp32.analogRead(pin)

#analogWrite:
esp32.ledcWrite(pin, value)
```

## 🧵 Control de Hilos (Threads)
```python
# Inicia el hilo del bucle y la configuración del esp32
esp32.start()

# Detiene el hilo del bucle
esp32.stop()
```
Para mantener el bucle en ejecución, incluya siempre:
```python
try:
	esp32.start()
	while  True:
		time.sleep(1)
except  KeyboardInterrupt:
	esp32.stop()
```

## ⚠️ Limitaciones Importantes
Este framework introduce:

- Latencia de USB serial.
- Jitter (inestabilidad) en la comunicación.
- Temporización no determinista debido a la programación del sistema operativo.

Debido a esto:

❌ NO usar para robots de producción. <br>
❌ NO usar para control de motores en tiempo real. <br>
❌ NO usar para sensores de tiempo crítico (ultrasónicos, encoders precisos, etc.).

Este framework es ideal para:

✅ Experimentos con LEDs y PWM. <br>
✅ Botones y sensores simples. <br>
✅ Potenciómetros. <br>
✅ Aprendizaje de lógica digital. <br>
✅ Integración de ESP32 con visión artificial (Computer Vision) o APIs web.