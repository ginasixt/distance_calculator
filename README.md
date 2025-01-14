# Patient Distance Calculator

Dieses Projekt berechnet die Entfernung von Patientenadressen zur Praxisadresse und visualisiert die Ergebnisse in einem Balkendiagramm. Es verwendet die OpenStreetMap Nominatim API zur Geokodierung der Adressen und die Haversine-Formel zur Berechnung der Entfernungen.

## Projektstruktur

```
.
├── __pycache__/
├── distance.py
├── gui.py
├── venv/
│   ├── .gitignore
│   ├── bin/
│   ├── include/
│   ├── lib/
│   └── pyvenv.cfg
└── README.md
```

## Voraussetzungen

- Python 3.9 oder höher
- Virtuelle Umgebung (empfohlen)

## Installation

1. **Repository klonen**:
    ```sh
    git clone https://github.com/ginasixt/distance_calculator.git
    cd distance_calculator
    ```

2. **Virtuelle Umgebung erstellen und aktivieren**:
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # Auf Windows: venv\Scripts\activate
   ```

3. **Pakete installieren**:
   ```sh
   pip install tkinter pandas geopy matplotlib
   ```

4. **Zertifikate installieren (nur für macOS)**:
   ```sh
   /Applications/Python3\ 3.x/Install\ Certificates.command
   ```


## Verwendung

1. **Programm starten**:
   ```sh
   python gui.py
   ```

2. **GUI verwenden**:
   - Geben Sie die Koordinaten der Praxis ein.
   - Laden Sie die Rohdaten hoch (Excel-Datei vom Patientensystem ausgespruckt).
   - Klicken Sie auf "Calculate Distances", um die Entfernungen zu berechnen und das Balkendiagramm anzuzeigen.

## Dateien

### `distance.py`

Diese Datei enthält die Hauptlogik zur Verarbeitung der Daten, Geokodierung der Adressen und Berechnung der Entfernungen.

- **Funktionen**:
  - `read_data(file_path)`: Liest die Excel-Datei und extrahiert die Patientendaten.
  - `get_coordinates(address)`: Verwendet die Nominatim API, um die Koordinaten einer Adresse zu erhalten.
  - `add_coordinates(data)`: Fügt den Patientendaten die Koordinaten hinzu.
  - `calculate_distance(lat1, lon1, lat2, lon2)`: Berechnet die Entfernung zwischen zwei Punkten auf der Erde mit der Haversine-Formel.
  - `plot_distances(data)`: Erstellt ein Balkendiagramm der Entfernungen.

### `gui.py`

Diese Datei enthält die GUI-Logik, die es dem Benutzer ermöglicht, die Rohdaten hochzuladen und die Adresse der Praxis einzugeben.

- **Klassen**:
  - `DistanceApp`: Erstellt die GUI und enthält Methoden zum Hochladen der Datei und Berechnen der Entfernungen.

## Beispiel

1. **Excel-Datei**:
   - Die Excel-Datei sollte wie folgt strukturiert sein, :
     - Erste Zeile: Leer, Patienten-ID, Nachname, Vorname
     - Zweite Zeile: Leer, Postleitzahl, Stadt (mehrere Spalten möglich, wenn Stadt Spalten enden, dann Komma), Straße(mehrere Spalten möglich), Hausnummer, Buchstabe.


Leere Zeilen und automatisch erstellten Blöcke und Überschriften vom Patientensystem werden ignoriert

2. **GUI**:
   - Geben Sie die Koordinaten ihrer Praxis ein
   - Laden Sie die Excel-Datei hoch.
   - Klicken Sie auf "Calculate Distances", um die Entfernungen zu berechnen und das Balkendiagramm anzuzeigen.

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Siehe die `venv/lib/python3.13/site-packages/geographiclib-2.0.dist-info/LICENSE`-Datei für Details.

## Autoren

- [Gina Netal](https://github.com/ginasixt)
