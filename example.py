from src.hzl_robotics_esp32 import ESP32
import time
import math

esp32 = ESP32("COM5")

@esp32.setup
def setup():
    esp32.pinMode(2, 1)
    esp32.ledcAttach(4, 1000, 8)

@esp32.loop
def loop():
    for i in range(256):
        corrected = int((i / 255) ** 2.2 * 255)
        esp32.ledcWrite(4, corrected)
        time.sleep(0.01)

    # Bajada
    for i in range(255, -1, -1):
        corrected = int((i / 255) ** 2.2 * 255)
        esp32.ledcWrite(4, corrected)
        time.sleep(0.01)

try:   
    esp32.start()
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    esp32.stop()