# 83. Zastosowania półprzewodników, przyrządy półprzewodnikowe

## Złącze p-n

**Budowa:** Połączenie półprzewodnika typu p z typem n

**Zjawiska na granicy:**
1. **Dyfuzja nośników** - elektrony z n do p, dziury z p do n
2. **Powstanie warstwy zubożonej** - obszar bez ruchomych nośników
3. **Pole elektryczne** w warstwie zubożonej
4. **Bariera potencjału** ≈ 0,7 V (Si), 0,3 V (Ge)

### Charakterystyka prądowo-napięciowa

**Równanie diody:**
$$I = I_s\left(e^{eU/kT} - 1\right)$$

gdzie:
- Is - prąd nasycenia wstecznego
- U - napięcie przyłożone

**Kierunek przewodzenia:** p → n (anoda → katoda)

## Dioda półprzewodnikowa

**Zastosowania:**
- **Prostowanie** prądu przemiennego
- **Stabilizacja** napięcia (diody Zenera)
- **Emisja światła** (LED)
- **Detekcja światła** (fotodiody)

### Dioda LED
**Zasada:** Rekombinacja promieniowa elektronów i dziur
$$hf = E_g$$

**Kolory LED:**
- Czerwony: GaAs (Eg ≈ 1,4 eV)
- Zielony: GaP (Eg ≈ 2,3 eV)  
- Niebieski: GaN (Eg ≈ 3,4 eV)

### Dioda Zenera
**Zasada:** Przebicie tunelowe przy napięciu wstecznym
- **Stabilizacja napięcia** w obwodach
- **Napięcie Zenera:** 2,7V - 200V

## Tranzystor bipolarny (BJT)

**Budowa:** Trzy warstwy n-p-n lub p-n-p
- **Emiter (E)** - silnie domieszkowany
- **Baza (B)** - cienka, słabo domieszkowana  
- **Kolektor (C)** - umiarkowanie domieszkowany

**Zasada działania:**
1. Złącze E-B spolaryzowane w kierunku przewodzenia
2. Elektrony wstrzykiwane z emitera do bazy
3. Większość elektronów dociera do kolektora
4. Mały prąd bazy kontroluje duży prąd kolektora

**Współczynnik wzmocnienia prądowego:**
$$β = \frac{I_C}{I_B}$$ (typowo 50-200)

## Tranzystor polowy (FET)

**Rodzaje:**
- **JFET** - złączowy  
- **MOSFET** - metal-oxide-semiconductor

### MOSFET
**Budowa:**
- **Źródło (S)** i **dren (D)** - obszary silnie domieszkowane
- **Kanał** - między S i D
- **Bramka (G)** - izolowana elektrodą metalową

**Zasada działania:**
- Napięcie na bramce kontroluje przewodność kanału
- **Enhancement mode:** kanał tworzony przez pole elektryczne
- **Depletion mode:** kanał istniejący, zwężany przez pole

## Układy scalone (IC)

**Technologia:**
- **Fotolitografia** - tworzenie wzorów na skali nanometrów
- **Implantacja jonów** - kontrolowane domieszkowanie
- **Epitaksja** - narastanie warstw

**Skale integracji:**
- **SSI:** < 100 tranzystorów
- **MSI:** 100-3000 tranzystorów
- **LSI:** 3000-100000 tranzystorów
- **VLSI:** > 100000 tranzystorów

## Ogniwa fotowoltaiczne

**Zasada działania:**
1. **Absorpcja fotonów** o energii hf ≥ Eg
2. **Generacja par elektron-dziura**
3. **Separacja nośników** przez pole w złączu p-n
4. **Przepływ prądu** w obwodzie zewnętrznym

**Sprawność:**
$$η = \frac{P_{out}}{P_{in}} \times 100\%$$

**Typowe sprawności:**
- Si monokrystaliczny: 15-20%
- Si polikrystaliczny: 12-16%
- CdTe: 16-22%
- Perowskity: do 25%

## Detektory promieniowania

### Fotodioda
**Działanie w spolaryzacji wstecznej**
- Fotony tworzą pary elektron-dziura
- Prąd proporcjonalny do natężenia światła

### Fototranzystor
**Wzmocnienie** sygnału świetlnego
- Wysoka czułość
- Wolniejsza odpowiedź niż fotodioda

## Przykład liczbowy

**Ogniwo Si (300K):**
- **Eg = 1,12 eV**
- **Napięcie jałowe:** Voc ≈ 0,6 V
- **Prąd zwarcia:** Isc = 35 mA/cm²
- **Sprawność:** η ≈ 18%
