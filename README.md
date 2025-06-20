# Metsamask: Metsamaski arvutus kaugseire andmete alusel

## Projekti ülevaade

Metsamask on Pythonil põhinev tööriist, mis on loodud metsamaskide arvutamiseks kaugseire andmete, täpsemalt LiDAR punktipilvede abil. Protsess hõlmab olemasolevate digitaalsete maastikumudelite (DTM) kasutamist ja LiDAR-andmete organiseerimist tõhusaks töötlemiseks Eesti Põhikaardi (EPK10T) ruudustiku süsteemi alusel.

## Omadused

* **LiDAR andmete töötlemine:** Käitleb LiDAR andmeid, mis on organiseeritud aasta ja EPK10T ruutude kaupa.
* **DTM integratsioon:** Kasutab Maa-ameti eelnevalt arvutatud 5-meetrise resolutsiooniga digitaalseid maastikumudeleid (DTM).
* **Automatiseeritud töövoog:** Lihtsustab metsamaskide genereerimise protsessi toorandmetest.

## Paigaldus

`metsamask` keskkonna seadistamiseks järgige neid samme:

1.  **Looge Conda keskkond:**
    ```bash
    conda create -n "metsamask" python=3.13 -y
    ```
2.  **Aktiveerige keskkond:**
    ```bash
    conda activate "metsamask"
    ```
3.  **Paigaldage sõltuvused:**
    ```bash
    pip install -r req.txt
    ```
    *Veenduge, et teie projekti kataloogis on `req.txt` fail, mis sisaldab kõiki vajalikke Pythoni sõltuvusi (nt `laspy`, `numpy`, `pandas`, `rasterio` jne).*

## Andmehalduse

### Lidari andmed

LiDAR `.laz` failid peaksid olema organiseeritud aastate kaupa alamkataloogidesse, mis asuvad peamises LiDAR-kataloogis. `config.json` failis tuleb selle peamise kataloogi tee määrata võtme `"lidar_laz_dir"` all.

**Näide kataloogipuust:**