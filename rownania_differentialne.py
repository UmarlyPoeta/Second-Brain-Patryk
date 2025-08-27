#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Równania różniczkowe - tematy do notatek w Obsidian

Ten plik zawiera listę tematów do stworzenia notatek o równaniach różniczkowych
w języku polskim dla vault Obsidian.
"""

# Tematy podstawowe - Podstawowe pojęcia
podstawowe_pojecia = [
    "Definicja równania różniczkowego",
    "Klasyfikacja równań różniczkowych", 
    "Rząd i stopień równania różniczkowego",
    "Rozwiązania ogólne i szczególne",
    "Warunki początkowe i brzegowe"
]

# Równania różniczkowe pierwszego rzędu
pierwszego_rzedu = [
    "Równania o zmiennych rozdzielonych",
    "Równania jednorodne pierwszego rzędu", 
    "Równania liniowe pierwszego rzędu",
    "Równania Bernoulliego",
    "Równania Riccatiego",
    "Równania dokładne",
    "Czynnik całkujący",
    "Zastosowania geometryczne równań pierwszego rzędu"
]

# Równania różniczkowe drugiego rzędu
drugiego_rzedu = [
    "Równania liniowe jednorodne o stałych współczynnikach",
    "Równania liniowe niejednorodne - metoda współczynników nieoznaczonych",
    "Równania liniowe niejednorodne - metoda uzmienniania stałych", 
    "Równania Eulera",
    "Oscylator harmoniczny",
    "Równania z tłumieniem"
]

# Układy równań różniczkowych
uklady_rownan = [
    "Układy liniowe jednorodne",
    "Macierz fundamentalna rozwiązań",
    "Wartości własne i wektory własne w układach",
    "Stabilność rozwiązań układów"
]

# Metody numeryczne
metody_numeryczne = [
    "Metoda Eulera",
    "Metoda Runge-Kutta",
    "Metody wielokrokowe",
    "Stabilność metod numerycznych"
]

# Zastosowania praktyczne
zastosowania = [
    "Modele wzrostu populacji",
    "Drgania mechaniczne", 
    "Obwody elektryczne RLC",
    "Przewodnictwo ciepła",
    "Reakcje chemiczne",
    "Modele epidemiologiczne",
    "Dynamika predator-ofiara",
    "Równania różniczkowe w ekonomii"
]

# Lista wszystkich tematów do utworzenia
wszystkie_tematy = (
    podstawowe_pojecia + 
    pierwszego_rzedu + 
    drugiego_rzedu + 
    uklady_rownan + 
    metody_numeryczne + 
    zastosowania
)

print(f"Łączna liczba tematów do opracowania: {len(wszystkie_tematy)}")
print("\nWszystkie tematy:")
for i, temat in enumerate(wszystkie_tematy, 1):
    print(f"{i:2d}. {temat}")