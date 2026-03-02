import serial
import struct
import threading
import time

START = 0xAA
DEVICE_ID = 0x01

class ESP32:

    def __init__(self, port, baudrate=115200):
        self.ser = serial.Serial(port, baudrate, timeout=0.5)
        
        self.ser.setDTR(False)
        self.ser.setRTS(False)

        time.sleep(1.5)  # ← importante
        self.ser.reset_input_buffer()
        self._setup_func = None
        self._loop_func = None
        self._running = False
        self._loop_thread = None

    # ================= CORE =================

    def _checksum(self, cmd, length, payload):
        chk = DEVICE_ID ^ cmd ^ length
        for b in payload:
            chk ^= b
        return chk & 0xFF

    def _send(self, cmd, payload=b'', expect_response=False):
        length = len(payload)
        chk = self._checksum(cmd, length, payload)

        packet = bytes([START, DEVICE_ID, cmd, length]) + payload + bytes([chk])
        self.ser.write(packet)

        if not expect_response:
            return None

        return self._read_response(cmd)

    def _read_response(self, cmd):
        header = self.ser.read(4)
        if len(header) < 4:
            raise TimeoutError("No response")

        start, dev_id, resp_cmd, length = header

        if start != START:
            raise ValueError("Invalid start byte")

        payload = self.ser.read(length)
        chk = self.ser.read(1)[0]

        calc_chk = self._checksum(resp_cmd, length, payload)

        if chk != calc_chk:
            raise ValueError("Checksum error")

        if resp_cmd != (cmd | 0x80):
            raise ValueError("Unexpected response")

        return payload
    
    def start_monitor(self):
        self._monitor_running = True
        self._monitor_thread = threading.Thread(target=self._monitor)
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def _monitor(self):
        while self._monitor_running:
            if self.ser.in_waiting:
                byte = self.ser.read(1)

                if byte[0] == START:
                    # Es paquete binario → dejar que _read_response lo maneje
                    self.ser.seek(self.ser.tell() - 1)
                    continue
                else:
                    # Es texto debug
                    line = byte + self.ser.readline()
                    print("ESP32:", line.decode(errors="ignore").strip())

    # ================= DECORADORES =================

    def setup(self, func):
        self._setup_func = func
        return func

    def loop(self, func):
        self._loop_func = func
        return func

    def start(self):
        self.start_monitor()
        if self._setup_func:
            self._setup_func()

        if self._loop_func:
            self._running = True
            self._loop_thread = threading.Thread(target=self._run_loop)
            self._loop_thread.daemon = True  # ← importante
            self._loop_thread.start()

    def stop(self):
        self._running = False
        if self._loop_thread:
            self._loop_thread.join()

    def _run_loop(self):
        while self._running:
            self._loop_func()

    # ================= API =================

    def digitalWrite(self, pin, value):
        self._send(0x02, bytes([pin, value]))

    def digitalRead(self, pin):
        resp = self._send(0x03, bytes([pin]), True)
        return resp[0]

    def analogWrite(self, pin, value):
        payload = bytes([pin]) + struct.pack(">H", value)
        self._send(0x04, payload)

    def analogRead(self, pin):
        resp = self._send(0x05, bytes([pin]), True)
        return struct.unpack(">H", resp)[0]

    def pinMode(self, pin, mode):
        self._send(0x06, bytes([pin, mode]))

    def ledcAttach(self, pin, freq, resolution):
        payload = bytes([pin]) + struct.pack(">I", freq) + bytes([resolution])
        self._send(0x07, payload)

    def ledcWrite(self, pin, duty):
        payload = bytes([pin]) + struct.pack(">H", duty)
        self._send(0x08, payload)
