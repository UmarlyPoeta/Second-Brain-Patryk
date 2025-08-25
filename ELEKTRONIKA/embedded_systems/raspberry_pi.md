# Raspberry Pi - Platforma Embedded

## Hardware Raspberry Pi
- **Procesor**: ARM Cortex (różne modele)
- **Architektura**: 32-bit lub 64-bit ARM
- **RAM**: Od 256MB do 8GB (zależnie od modelu)
- **Storage**: MicroSD card, opcjonalnie eMMC
- **GPIO**: 40-pin header (modele nowsze)

## Modele Raspberry Pi

### Raspberry Pi 4 Model B
- **CPU**: Cortex-A72 quad-core 1.5GHz
- **RAM**: 2GB, 4GB, lub 8GB LPDDR4
- **USB**: 2x USB 3.0, 2x USB 2.0
- **Ethernet**: Gigabit Ethernet
- **WiFi**: 802.11ac dual-band
- **Bluetooth**: 5.0

### Raspberry Pi Zero 2W
- **CPU**: ARM Cortex-A53 quad-core 1GHz
- **RAM**: 512MB LPDDR2
- **Rozmiar**: 65mm × 30mm
- **WiFi**: 802.11n
- **Bluetooth**: 4.2

### Raspberry Pi Pico
- **Mikrokontroler**: RP2040 (dual-core ARM Cortex-M0+)
- **Pamięć**: 264KB SRAM, 2MB Flash
- **GPIO**: 26 multifunkcyjnych pinów
- **Cena**: Bardzo niska (~$4)

## System operacyjny

### Raspberry Pi OS (wcześniej Raspbian)
```bash
# Instalacja przez Raspberry Pi Imager
# Konfiguracja SSH, WiFi, użytkownika
sudo raspi-config
```

### Alternatywne systemy
- **Ubuntu**: Pełna dystrybucja Linux
- **Arch Linux ARM**: Minimalna dystrybucja
- **RetroPie**: System do gier retro
- **OpenELEC/LibreELEC**: Media center

## GPIO (General Purpose Input/Output)

### Pinout Raspberry Pi
```
3V3  (1) (2)  5V
GPIO2(3) (4)  5V
GPIO3(5) (6)  GND
GPIO4(7) (8)  GPIO14
GND  (9) (10) GPIO15
GPIO17(11)(12) GPIO18
GPIO27(13)(14) GND
GPIO22(15)(16) GPIO23
3V3 (17)(18) GPIO24
GPIO10(19)(20) GND
GPIO9(21)(22) GPIO25
GPIO11(23)(24) GPIO8
GND (25)(26) GPIO7
...
```

### Kontrola GPIO przez terminal
```bash
# Włączenie GPIO jako wyjście
echo "18" > /sys/class/gpio/export
echo "out" > /sys/class/gpio/gpio18/direction
echo "1" > /sys/class/gpio/gpio18/value

# Wyłączenie GPIO
echo "0" > /sys/class/gpio/gpio18/value
echo "18" > /sys/class/gpio/unexport
```

## Programowanie w Python

### Biblioteka RPi.GPIO
```python
import RPi.GPIO as GPIO
import time

# Konfiguracja
GPIO.setmode(GPIO.BCM)  # lub GPIO.BOARD
GPIO.setup(18, GPIO.OUT)

# Miganie LED
for i in range(10):
    GPIO.output(18, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(18, GPIO.LOW)
    time.sleep(0.5)

GPIO.cleanup()
```

### Biblioteka gpiozero
```python
from gpiozero import LED, Button
from time import sleep

led = LED(18)
button = Button(2)

while True:
    if button.is_pressed:
        led.on()
    else:
        led.off()
    sleep(0.1)
```

### Obsługa PWM
```python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

# Utworzenie obiektu PWM (pin 18, częstotliwość 1000Hz)
pwm = GPIO.PWM(18, 1000)
pwm.start(0)  # Rozpoczęcie z duty cycle 0%

try:
    while True:
        # Wzrost jasności
        for duty_cycle in range(0, 101, 5):
            pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(0.1)
        # Spadek jasności
        for duty_cycle in range(100, -1, -5):
            pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(0.1)
except KeyboardInterrupt:
    pass

pwm.stop()
GPIO.cleanup()
```

## Komunikacja szeregowa

### UART Configuration
```bash
# Włączenie UART w /boot/config.txt
enable_uart=1

# Wyłączenie konsoli szeregowej
sudo systemctl disable serial-getty@ttyS0.service
```

### Python Serial
```python
import serial
import time

ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)

# Wysłanie danych
ser.write(b'Hello Arduino\n')

# Odczyt danych
if ser.in_waiting > 0:
    data = ser.readline().decode().strip()
    print(f"Odebrano: {data}")

ser.close()
```

## I2C i SPI

### I2C Configuration
```bash
# Włączenie I2C
sudo raspi-config
# Interface Options → I2C → Enable

# Instalacja narzędzi
sudo apt install i2c-tools

# Skanowanie urządzeń I2C
i2cdetect -y 1
```

### I2C w Python
```python
import smbus
import time

bus = smbus.SMBus(1)  # I2C bus 1
address = 0x48        # Adres urządzenia

# Odczyt bajtu
data = bus.read_byte(address)

# Zapis bajtu
bus.write_byte(address, 0xFF)

# Odczyt rejestru
value = bus.read_byte_data(address, 0x00)
```

### SPI Configuration
```bash
# Włączenie SPI w raspi-config
sudo raspi-config
# Interface Options → SPI → Enable
```

### SPI w Python
```python
import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, Device 0
spi.max_speed_hz = 1000000

# Wysłanie i odczyt danych
response = spi.xfer2([0x01, 0x02, 0x03])
print(response)

spi.close()
```

## Raspberry Pi Pico - MicroPython

### Podstawowy kod MicroPython
```python
from machine import Pin, PWM
import time

# Konfiguracja LED i przycisku
led = Pin(25, Pin.OUT)
button = Pin(2, Pin.IN, Pin.PULL_UP)

# PWM dla regulacji jasności
pwm_led = PWM(Pin(25))
pwm_led.freq(1000)

while True:
    if not button.value():  # Przycisk wciśnięty (active low)
        # Płynne włączanie i wyłączanie LED
        for duty in range(0, 65536, 1000):
            pwm_led.duty_u16(duty)
            time.sleep_ms(50)
        for duty in range(65536, 0, -1000):
            pwm_led.duty_u16(duty)
            time.sleep_ms(50)
    else:
        led.off()
    
    time.sleep_ms(100)
```

## Camera Module

### Kamera w Python
```python
from picamera2 import Picamera2
import time

picam2 = Picamera2()

# Konfiguracja kamery
camera_config = picam2.create_still_configuration()
picam2.configure(camera_config)

# Uruchomienie kamery
picam2.start()

# Zrobienie zdjęcia
time.sleep(2)  # Czas na autofocus
picam2.capture_file("image.jpg")

# Zatrzymanie kamery
picam2.stop()
```

## Optymalizacja wydajności

### Overclocking
```bash
# W /boot/config.txt
arm_freq=1800
gpu_freq=500
over_voltage=4
```

### Monitoring zasobów
```bash
# Temperatura CPU
vcgencmd measure_temp

# Częstotliwość CPU
vcgencmd measure_clock arm

# Napięcie
vcgencmd measure_volts
```

### Zarządzanie pamięcią
```python
# Monitoring pamięci w Python
import psutil

# Użycie RAM
memory = psutil.virtual_memory()
print(f"RAM: {memory.percent}% used")

# Użycie CPU
cpu = psutil.cpu_percent(interval=1)
print(f"CPU: {cpu}% used")
```

## Automatyzacja i usługi systemowe

### Systemd service
```bash
# /etc/systemd/system/myapp.service
[Unit]
Description=My Python App
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/myapp
ExecStart=/usr/bin/python3 /home/pi/myapp/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Aktywacja usługi
sudo systemctl enable myapp.service
sudo systemctl start myapp.service
```

### Cron jobs
```bash
# Edycja crontab
crontab -e

# Uruchomienie skryptu co 5 minut
*/5 * * * * /usr/bin/python3 /home/pi/script.py
```

## Bezpieczeństwo

### Konfiguracja SSH
```bash
# Zmiana domyślnego hasła
passwd

# Konfiguracja SSH key
ssh-keygen -t rsa -b 4096
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

# Wyłączenie hasła SSH w /etc/ssh/sshd_config
PasswordAuthentication no
```

### Firewall
```bash
# Instalacja UFW
sudo apt install ufw

# Konfiguracja podstawowa
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw enable
```

## Powiązane tematy
- [[arduino_podstawy|Arduino - Podstawy]]
- [[mikrokontrolery_vs_mikroprocesory|Mikrokontrolery vs Mikroprocesory]]
- [[io_cyfrowe_analogowe|Wejścia/Wyjścia Cyfrowe i Analogowe]]
- [[protokoly_komunikacyjne|Protokoły Komunikacyjne]]
- [[linux_embedded|Linux w systemach embedded]]