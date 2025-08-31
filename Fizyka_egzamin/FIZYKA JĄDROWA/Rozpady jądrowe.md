# 87. Rozpady jądrowe

## Radioaktywność

**Definicja:** Spontaniczne przekształcenia niestabilnych jąder atomowych z emisją promieniowania.

**Prawo rozpadu:**
$$N(t) = N_0 e^{-λt}$$

gdzie:
- N₀ - początkowa liczba jąder
- λ - stała rozpadu
- t - czas

## Podstawowe typy rozpadów

### Rozpad α (alfa)

**Reakcja:**
$$^A_Z X → ^{A-4}_{Z-2} Y + ^4_2 He^{2+}$$

**Właściwości:**
- **Emisja jądra helu** (cząstka α)  
- **Typowe dla ciężkich jąder** (A > 200)
- **Energia α:** 4-9 MeV
- **Zasięg w powietrzu:** kilka cm

**Przykład:** ²²⁶Ra → ²²²Rn + α

### Rozpad β⁻ (beta minus)

**Reakcja:**
$$^A_Z X → ^A_{Z+1} Y + e^- + \bar{ν_e}$$

**Mechanizm:** Neutron → proton + elektron + antyneutrino
$$n → p + e^- + \bar{ν_e}$$

**Właściwości:**
- **Ciągłe widmo energii** elektronów (0 do Emax)
- **Typowe dla jąder** z nadmiarem neutronów
- **Zasięg:** metry w powietrzu

**Przykład:** ¹⁴C → ¹⁴N + e⁻ + ν̄ₑ

### Rozpad β⁺ (beta plus)

**Reakcja:**
$$^A_Z X → ^A_{Z-1} Y + e^+ + ν_e$$

**Mechanizm:** Proton → neutron + pozyton + neutrino
$$p → n + e^+ + ν_e$$

**Właściwości:**
- **Tylko dla jąder** z nadmiarem protonów
- **Próg energetyczny:** 1,022 MeV (2mₑc²)
- **Pozyton annihiluje** z elektronem → 2γ (511 keV każdy)

### Wychwyt elektronu (EC)

**Reakcja:**
$$^A_Z X + e^- → ^A_{Z-1} Y + ν_e$$

**Właściwości:**
- **Alternatywa dla β⁺** przy niskich energiach
- **Charakterystyczne promieniowanie X** z dziur w powłokach
- **Neutrino monoenergetyczne**

### Rozpad γ (gamma)

**Emisja fotonów** przy przejściach między poziomami energetycznymi jądra

**Właściwości:**
- **Dyskretne energie** fotonów
- **Wysoka przenikliwość** (brak ładunku i masy)
- **Towarzyszy innym rozpadom**

## Charakterystyczne czasy

### Okres połowicznego rozpadu (T₁/₂)
$$T_{1/2} = \frac{\ln 2}{λ} = \frac{0,693}{λ}$$

### Średni czas życia (τ)
$$τ = \frac{1}{λ}$$

**Związek:** $T_{1/2} = τ \ln 2$

### Aktywność (A)
$$A = λN = \frac{dN}{dt}$$

**Jednostki:**
- **Becquerel (Bq):** 1 rozpad/sekundę
- **Curie (Ci):** 3,7×10¹⁰ Bq

## Łańcuchy rozpadowe

**Przykład - szereg radowy uranu:**
²³⁸U → ²³⁴Th → ²³⁴Pa → ²³⁴U → ... → ²⁰⁶Pb (stabilny)

**Równowaga świecka:**
$$λ_1 N_1 = λ_2 N_2 = λ_3 N_3 = ...$$

## Przykłady liczbowe

**Węgiel ¹⁴C:**
- **T₁/₂ = 5730 lat**
- **λ = 1,21×10⁻⁴ rok⁻¹**
- **Aktywność w organizmach żywych:** 15,3 Bq/g węgla

**Radon ²²²Rn:**
- **T₁/₂ = 3,8 dni**  
- **Produkt rozpadu radu**
- **Zagrożenie w budynkach** (akumulacja w piwnicach)

## Datowanie radiometryczne

**Wzór wieku:**
$$t = \frac{1}{λ} \ln\left(\frac{N_0}{N}\right) = \frac{T_{1/2}}{\ln 2} \ln\left(\frac{N_0}{N}\right)$$

**Metody:**
- **¹⁴C:** do 50 000 lat (materiały organiczne)
- **K-Ar:** miliony lat (skały wulkaniczne)  
- **U-Pb:** miliardy lat (najstarsze skały)

## Zastosowania

**Medycyna:**
- **Diagnostyka:** ⁹⁹ᵐTc, ¹³¹I
- **Terapia:** ⁶⁰Co, ¹³¹I, ⁹⁰Sr

**Energetyka:**
- **Elektrownie jądrowe** (²³⁵U, ²³⁹Pu)
- **Reaktory badawcze**

**Nauka:**
- **Znaczniki radioaktywne** w biochemii
- **Datowanie** próbek geologicznych

![[rozpady_jądrowe.pdf]]
