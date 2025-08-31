# Tranzystory

## 🔬 Definicja

**Tranzystor** to półprzewodnikowy element elektroniczny o trzech wyprowadzeniach, działający jako przełącznik lub wzmacniacz sygnałów elektrycznych.

## 🏗️ Tranzystory bipolarne (BJT)

### Budowa i rodzaje

#### Tranzystor NPN
```
     C (Kolektor)
     │
  B ──┤►── Emiter (E)
     │
```
- **Struktura**: N-P-N (krzem)
- **Przewodzenie**: Elektrony
- **Prąd bazy**: Steruje większym prądem kolektora

#### Tranzystor PNP  
```
     C (Kolektor)
     │
  B ──┤◄── Emiter (E)
     │
```
- **Struktura**: P-N-P (krzem)
- **Przewodzenie**: Dziury
- **Polaryzacja**: Odwrotna niż NPN

### Zasada działania

#### Prądy w tranzystorze
```
IE = IB + IC
IC = β × IB
```
Gdzie:
- **IE** - prąd emitera
- **IB** - prąd bazy (sterowniczy)
- **IC** - prąd kolektora (roboczy)
- **β (hFE)** - współczynnik wzmocnienia prądowego (20-500)

#### Napięcia przewodzenia
- **UBE** - napięcie baza-emiter: ~0.7V (krzem)
- **UCE** - napięcie kolektor-emiter: 0.2V (nasycenie) - UCC

### Stany pracy tranzystora

#### Stan odcięcia (OFF)
- **Warunek**: UBE < 0.6V
- **Prądy**: IB ≈ 0, IC ≈ 0
- **Zastosowanie**: Przełącznik otwarty

#### Stan nasycenia (ON)
- **Warunek**: IB > IC/β
- **Napięcia**: UCE ≈ 0.2V
- **Zastosowanie**: Przełącznik zamknięty

#### Stan aktywny (liniowy)
- **Warunek**: UBE ≈ 0.7V, IC = β × IB
- **Zastosowanie**: Wzmacnianie

## 🔄 Tranzystory polowe (FET)

### MOSFET (Metal-Oxide-Semiconductor FET)

#### N-channel MOSFET
```
     D (Drain)
     │
  G ──┤  S (Source)
     │  │
```
- **Sterowanie**: Napięciem bramki (Gate)
- **Typ enhancement**: Wymaga UGS > Vth do przewodzenia
- **Typ depletion**: Przewodzi przy UGS = 0

#### P-channel MOSFET
- **Polaryzacje**: Odwrotne niż N-channel
- **Zastosowanie**: Przełączniki strony wysokiej (high-side)

### Charakterystyka MOSFET
- **RDS(on)**: Opór przewodzenia (mΩ - Ω)
- **VGS(th)**: Napięcie progowe bramki
- **ID(max)**: Maksymalny prąd drenu
- **Pojemności**: CGD, CGS, CDS (ważne przy wysokich częstotliwościach)

## 💡 Popularne typy tranzystorów

### Tranzystory bipolarne małej mocy

#### NPN
- **BC547, BC548, BC549**: Allround, 100mA, 45V
- **2N2222**: Universal NPN, 800mA, 30V
- **2N3904**: Szybki przełącznik, 200mA, 40V

#### PNP
- **BC557, BC558, BC559**: Dopełnienie BC54x
- **2N2907**: Dopełnienie 2N2222
- **2N3906**: Dopełnienie 2N3904

### Tranzystory mocy

#### BJT mocy
- **TIP31C/TIP32C**: NPN/PNP, 3A, 100V
- **2N3055**: NPN, 15A, 60V (klasyk)
- **BD679/BD680**: Darlington, 4A, 100V

#### MOSFET mocy
- **IRF520**: N-channel, 9.7A, 100V
- **IRF9540**: P-channel, 19A, 100V  
- **IRLB8721**: Logic level, 30A, 30V

## ⚡ Układy pracy tranzystorów

### Tranzystor jako przełącznik

#### Przełącznik NPN (low-side)
```
     +VCC
       │
       R (obciążenie)
       │
       ├──── Wyjście
       │
   B ──┤►── E
       │    │
      GND  GND

RB = (Uin - 0.7V) / IB
IB = IC / β
```

#### Przełącznik PNP (high-side)
```
   +VCC ──┬─── Wyjście
          │
      E ──┤◄── B
          │    │
          R    RB
          │    │
         GND  Sterowanie
```

### Obliczenia dla przełącznika

#### Przykład: Sterowanie LED
**Dane**: LED 20mA, VCC = 5V, tranzystor β = 100, sterowanie 3.3V

```
IC = 20mA
IB(potrzebne) = IC/β = 20mA/100 = 0.2mA
IB(dostępne) = (3.3V - 0.7V)/RB
RB = 2.6V / 0.2mA = 13kΩ

Dla pewności: RB = 10kΩ (większy prąd bazy = pewne nasycenie)
```

### Darlington
```
      ──┤►──┤►──
        T1  T2
```
- **Wzmocnienie**: β = β1 × β2
- **Spadek napięcia**: 2 × 0.7V = 1.4V
- **Zastosowanie**: Duże wzmocnienie prądowe

## 🔧 Tranzystor jako wzmacniacz

### Wzmacniacz wspólny emiter
```
+VCC ──┬─── RC ───┬─── Vout
       │          │
      RB         │
       │          │
  Vin ─┴──────┤►──┘
              │
             RE
              │
             GND
```
- **Wzmocnienie napięciowe**: Au ≈ -RC/RE
- **Wzmocnienie prądowe**: Ai ≈ β
- **Inwersja fazy**: Tak

### Wtórnik emiterowy (wspólny kolektor)
```
+VCC ──┬─── RC
       │    
      RB   │
       │    ├──── Vout
  Vin ─┴──┤►│
          │ RE
          │ │
         GND GND
```
- **Wzmocnienie napięciowe**: Au ≈ 1 (brak wzmocnienia)
- **Wzmocnienie prądowe**: Ai ≈ β
- **Impedancja wejściowa**: Wysoka
- **Impedancja wyjściowa**: Niska

## 🌡️ Zagadnienia termiczne

### Moc rozproszona
```
P = VCE × IC (dla BJT)
P = VDS × ID (dla MOSFET)
```

### Temperatura złącza
```
Tj = Ta + (Rθja × P)
```
Gdzie:
- **Tj** - temperatura złącza
- **Ta** - temperatura otoczenia  
- **Rθja** - opór termiczny złącze-otoczenie

### Radiatory
**Kiedy potrzebny**:
- P > 0.5W w obudowie TO-92
- P > 1W w obudowie TO-220  
- Przy wysokich temperaturach otoczenia

**Dobór radiatora**:
```
Rθsa = (Tj(max) - Ta) / P - Rθjc - Rθcs
```

## ⚠️ Częste błędy i problemy

### Zła polaryzacja
- **NPN**: Kolektor > emiter, baza > emiter  
- **PNP**: Emiter > kolektor, emiter > baza
- **MOSFET N**: Drain > source, gate steruje

### Za mały prąd bazy
- **Objaw**: Tranzystor nie nasyce się (UCE > 0.2V)
- **Rozwiązanie**: Zmniejszyć RB

### Przegrzanie
- **Objawy**: Słaba wydajność, uszkodzenie
- **Rozwiązania**: Radiator, niższa częstotliwość przełączania

### Oscylacje
- **Przyczyna**: Pasożytnicze sprzężenie zwrotne
- **Rozwiązanie**: Kondensatory odsprzęgające, rezystor w bazie

## 🧮 Ćwiczenia obliczeniowe

### Zadanie 1: Przełącznik LED
Zaprojektuj przełącznik LED 50mA przy 12V, sterowany sygnałem 5V. Użyj tranzystor β = 150.

### Zadanie 2: Wzmacniacz
Oblicz wzmocnienie wzmacniacza OE przy RC = 2kΩ, RE = 200Ω.

### Zadanie 3: Moc
Tranzystor w obudowie TO-220 (Rθja = 50°C/W) rozprasza 3W przy 25°C. Jaka będzie temperatura złącza?

## 🔧 Testowanie tranzystorów

### Multimetrem (test diodowy)
**BJT NPN**:
1. **B→E**: ~0.7V (jak dioda)
2. **B→C**: ~0.7V (jak dioda)  
3. **E→B**: OL
4. **C→B**: OL
5. **E→C**: OL
6. **C→E**: OL

**Uszkodzone**:
- Zwarcie między wyprowadzeniami
- Brak spadku napięcia B→E i B→C

### Testery tranzystorów
- **Pomiar β (hFE)**
- **Identyfikacja wyprowadzeń**
- **Test sprawności**

## 📚 Powiązane tematy

- [[diody|Diody]]
- [[wzmacniacze_operacyjne|Wzmacniacze Operacyjne]]
- [[sterowniki_silników|Sterowniki Silników]]
- [[arduino_tranzystory|Arduino - Sterowanie Tranzystorami]]
- [[zasilacze_liniowe|Zasilacze Liniowe]]
- [[multimetr|Multimetr - Test Tranzystorów]]

---

#elektronika #tranzystory #BJT #MOSFET #wzmacniacze #przełączniki