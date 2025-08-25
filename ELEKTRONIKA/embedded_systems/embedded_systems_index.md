# Systemy Wbudowane - Kompendium Wiedzy

Witaj w kompendium wiedzy o systemach wbudowanych! Ta kolekcja notatek obejmuje wszystkie kluczowe aspekty rozwoju systemów embedded, od podstaw po zaawansowane techniki.

## 📋 Spis treści

### 🔧 Podstawy
- **[[arduino_podstawy|Arduino - Podstawy]]** - Hardware, IDE, programowanie podstawowe
- **[[raspberry_pi|Raspberry Pi]]** - Hardware, Linux, GPIO, Python programming  
- **[[mikrokontrolery_vs_mikroprocesory|Mikrokontrolery vs Mikroprocesory]]** - Różnice, architektury, zastosowania

### ⚡ Hardware i Interfejsy
- **[[io_cyfrowe_analogowe|Wejścia/Wyjścia Cyfrowe i Analogowe]]** - GPIO, ADC, DAC, PWM, filtrowanie
- **[[protokoly_komunikacyjne|Protokoły Komunikacyjne]]** - UART, SPI, I2C, CAN, Ethernet, WiFi
- **[[sensory_i_aktuatory|Sensory i Aktuatory]]** - Temperatura, odległość, ruch, silniki, LED
- **[[interfejsy_sprzętowe|Interfejsy Sprzętowe]]** - Poziomy napięć, pull-up/down, konwertery

### 💻 Programowanie i Rozwój
- **[[embedded_programming|Programowanie Embedded]]** - Dobre praktyki, debugowanie, CLI, OTA
- **[[memory_management|Zarządzanie Pamięcią]]** - Flash, RAM, EEPROM, stack, heap, optymalizacja
- **[[rtos_freertos|RTOS i FreeRTOS]]** - Systemy czasu rzeczywistego, zadania, semafory
- **[[power_management|Zarządzanie Zasilaniem]]** - Sleep modes, optymalizacja energetyczna

### 🔬 Zaawansowane Tematy
- **[[signal_processing|Przetwarzanie Sygnałów]]** - DSP, filtry, FFT w embedded
- **[[wireless_protocols|Protokoły Bezprzewodowe]]** - WiFi, Bluetooth, LoRa, Zigbee
- **[[security_embedded|Bezpieczeństwo w Embedded]]** - Szyfrowanie, autentykacja, secure boot
- **[[testing_embedded|Testowanie Systemów Embedded]]** - Unit testing, HIL, automatyzacja

### 🛠️ Narzędzia i Metodologie
- **[[debugging_embedded|Debugowanie Embedded]]** - JTAG, SWD, logic analyzer
- **[[version_control|Kontrola Wersji w Embedded]]** - Git workflows, branching, CI/CD
- **[[pcb_design|Projektowanie PCB]]** - Schematic, layout, EMI/EMC
- **[[documentation_embedded|Dokumentacja Projektów]]** - Specyfikacje, diagramy, user manuals

### 🏗️ Projekty i Ćwiczenia
- **[[projekty_i_cwiczenia|Projekty i Ćwiczenia Laboratoryjne]]** - Kompletne projekty z kodem
- **[[troubleshooting|Rozwiązywanie Problemów]]** - Typowe błędy i ich rozwiązania
- **[[best_practices|Najlepsze Praktyki]]** - Coding standards, review process

---

## 🎯 Jak korzystać z tego kompendium

### Dla początkujących
1. Zacznij od [[arduino_podstawy|Arduino - Podstawy]]
2. Przeczytaj o [[mikrokontrolery_vs_mikroprocesory|różnicach MCU vs MPU]]
3. Poznaj [[io_cyfrowe_analogowe|podstawy I/O]]
4. Wypróbuj [[sensory_i_aktuatory|podstawowe sensory]]

### Dla średniozaawansowanych  
1. Pogłęb wiedzę o [[protokoly_komunikacyjne|protokołach komunikacyjnych]]
2. Naucz się [[embedded_programming|dobrych praktyk programowania]]
3. Zrozum [[memory_management|zarządzanie pamięcią]]
4. Rozpocznij pracę z [[rtos_freertos|RTOS]]

### Dla zaawansowanych
1. Opanuj [[signal_processing|przetwarzanie sygnałów]]
2. Zajmij się [[security_embedded|bezpieczeństwem]]
3. Naucz się [[debugging_embedded|zaawansowanego debugowania]]
4. Rozwijaj [[pcb_design|umiejętności projektowania PCB]]

---

## 💡 Kluczowe pojęcia

### Hardware
- **MCU** (Microcontroller Unit) - kompletny system na jednym chipie
- **GPIO** (General Purpose Input/Output) - uniwersalne piny I/O
- **ADC/DAC** - konwertery analogowo-cyfrowe/cyfrowo-analogowe
- **PWM** - modulacja szerokości impulsu
- **ISR** - procedura obsługi przerwania

### Software  
- **Bare Metal** - programowanie bez systemu operacyjnego
- **RTOS** - system operacyjny czasu rzeczywistego
- **Bootloader** - program ładujący główne oprogramowanie
- **Firmware** - oprogramowanie wbudowane w hardware
- **Cross-compilation** - kompilacja na inną architekturę

### Protokoły
- **UART** - asynchroniczna komunikacja szeregowa
- **SPI** - synchroniczna komunikacja szeregowa (master-slave)
- **I2C** - dwuprzewodowa komunikacja z adresowaniem
- **CAN** - magistrala używana w automotive
- **Modbus** - protokół przemysłowy

---

## 🔗 Przydatne zasoby

### Dokumentacja techniczna
- [Arduino Reference](https://www.arduino.cc/reference/)
- [ESP32 Documentation](https://docs.espressif.com/projects/esp-idf/)
- [STM32 HAL Documentation](https://www.st.com/en/development-tools/stm32cubemx.html)
- [Raspberry Pi Documentation](https://www.raspberrypi.org/documentation/)

### Narzędzia rozwojowe
- **Arduino IDE** - proste środowisko dla Arduino
- **PlatformIO** - zaawansowane IDE dla embedded
- **STM32CubeIDE** - oficjalne IDE dla STM32
- **VS Code** - uniwersalny edytor z rozszerzeniami

### Hardware debugging
- **Logic Analyzer** - analiza sygnałów cyfrowych
- **Oscilloscope** - pomiary sygnałów analogowych
- **Multimeter** - podstawowe pomiary elektryczne
- **JTAG/SWD** - debugowanie na poziomie procesora

---

## 📚 Metodologia nauki

### 1. Teoria + Praktyka
- Każdy temat zawiera przykłady kodu
- Teoretyczne podstawy wsparte praktycznymi implementacjami
- Kod można bezpośrednio testować na hardware

### 2. Projektowe podejście
- Wiedza organizowana wokół rzeczywistych projektów
- Od prostych LED do złożonych systemów IoT
- Stopniowe wprowadzanie nowych konceptów

### 3. Cross-reference
- Tematy są połączone linkami
- Łatwe nawigowanie między powiązanymi zagadnieniami
- Budowanie mapy mentalnej wiedzy

### 4. Troubleshooting
- Typowe problemy i ich rozwiązania
- Debug tips i best practices
- Nauka z błędów

---

## 🎯 Cele edukacyjne

Po przejściu przez to kompendium będziesz potrafić:

### Podstawowy poziom
- [ ] Programować Arduino i podstawowe mikrokontrolery
- [ ] Obsługiwać GPIO, ADC, PWM
- [ ] Komunikować się przez UART, SPI, I2C
- [ ] Integrować podstawowe sensory i aktuatory

### Średniozaawansowany poziom
- [ ] Projektować systemy embedded od podstaw
- [ ] Optymalizować kod pod kątem pamięci i wydajności
- [ ] Implementować protokoły komunikacyjne
- [ ] Debugować problemy hardware i software

### Zaawansowany poziom
- [ ] Pracować z RTOS i systemami wielozadaniowymi
- [ ] Projektować bezpieczne systemy embedded
- [ ] Implementować zaawansowane algorytmy DSP
- [ ] Projektować własne PCB

---

## 🤝 Współpraca i rozwój

To kompendium jest żywym dokumentem, który stale się rozwija. Każdy temat może być rozszerzany i aktualizowany o nowe informacje, przykłady i projekty.

### Wskazówki do rozwoju
- Dodawaj nowe przykłady kodu gdy poznasz ciekawe rozwiązania
- Dokumentuj napotkane problemy i ich rozwiązania  
- Rozszerzaj istniejące tematy o nowe informacje
- Twórz cross-linki między powiązanymi zagadnieniami

---

*Ostatnia aktualizacja: 2024*  
*Wersja: 2.0*  

**Powodzenia w nauce systemów wbudowanych! 🚀**