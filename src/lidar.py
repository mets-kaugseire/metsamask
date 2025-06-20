import os
import laspy
import pandas as pd
import numpy as np
import requests
from urllib.parse import urlencode # Paremaks URL-i kodeerimiseks

def read_las_file(file_path: str) -> pd.DataFrame:
    """
    Loeb LAS/LAZ-faili ja tagastab punktandmed Pandas DataFrame'ina.

    Args:
        file_path (str): Tee LAS/LAZ-failini.

    Returns:
        pd.DataFrame: DataFrame, mis sisaldab X, Y, Z koordinaate,
                      klassifikatsiooni ja tagastamise numbrit.

    Raises:
        RuntimeError: Kui faili lugemisel ilmneb viga.
    """
    try:
        with laspy.open(file_path) as las_file:
            las_data = las_file.read()
            # Loome DataFrame'i otse las_data atribuutidest, mis on juba numpy massiivid
            return pd.DataFrame({
                "x": las_data.x,
                "y": las_data.y,
                "z": las_data.z,
                'classification': las_data.classification,
                'return_number': las_data.return_number
            })
    except Exception as e:
        # Püüa kinni kõik vead ja anna informatiivsem veateade
        raise RuntimeError(f"Ebaõnnestus LAS/LAZ-faili lugemine '{file_path}': {e}") from e

def read_las_directory(directory_path: str) -> pd.DataFrame:
    """
    Loeb kõik LAS/LAZ-failid määratud kataloogist ja ühendab nende punktandmed
    üheks Pandas DataFrame'iks.

    Args:
        directory_path (str): Tee kataloogini, mis sisaldab LAS/LAZ-faile.

    Returns:
        pd.DataFrame: Ühendatud DataFrame kõikidest failidest.
                      Tagastab tühja DataFrame'i, kui faile ei leita või viga.
    """
    all_point_data = []
    # Kontrollime, kas kataloog eksisteerib
    if not os.path.isdir(directory_path):
        print(f"Hoiatus: Kataloogi ei leitud '{directory_path}'. Tagastatakse tühi DataFrame.")
        return pd.DataFrame()

    for file_name in os.listdir(directory_path):
        # Kontrollime faililaiendit nii .las kui ka .laz puhul
        if file_name.lower().endswith(('.laz', '.las')):
            file_path = os.path.join(directory_path, file_name)
            try:
                data = read_las_file(file_path)
                all_point_data.append(data)
            except RuntimeError as e:
                print(f"Viga faili '{file_name}' lugemisel: {e}")

    # Ühenda kõik DataFrame'id üheks, kui andmeid on
    if all_point_data:
        return pd.concat(all_point_data, ignore_index=True)
    else:
        print(f"Teates ei leitud LAS/LAZ-faile kataloogist '{directory_path}'.")
        return pd.DataFrame()

def download_file(url: str, save_path: str):
    """
    Laeb faili URL-ist alla ja salvestab selle määratud asukohta.

    Args:
        url (str): Allalaaditava faili URL.
        save_path (str): Tee, kuhu fail salvestada, sealhulgas failinimi.

    Raises:
        RuntimeError: Kui allalaadimine ebaõnnestub või ilmneb võrguviga.
    """
    try:
        # Seadista ajaühendus, et vältida lõputut ootamist
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()  # Tekitab HTTPError-i halbade vastuste korral (4xx või 5xx)

        # Hangi kogu suurus sisu-pikkuse päisest, kui see on olemas
        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192  # 8 KB
        downloaded_size = 0

        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=block_size):
                if chunk:  # filtri välja keep-alive paketid
                    file.write(chunk)
                    downloaded_size += len(chunk)
                    # Valikuline: näita allalaadimise edenemist
                    # progress = (downloaded_size / total_size) * 100 if total_size else 0
                    # print(f"Allalaadimine: {progress:.2f}%", end='\r')
        print(f"Fail edukalt alla laetud ja salvestatud asukohta '{save_path}'")
    except requests.exceptions.Timeout:
        raise RuntimeError(f"Faili allalaadimine ajastati välja '{url}'.") from None
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Ebaõnnestus faili allalaadimine '{url}': {e}") from e
    except IOError as e:
        raise RuntimeError(f"Ebaõnnestus faili salvestamine asukohta '{save_path}': {e}") from e

def create_maaamet_laz_url(kaardiruut: str, andmetyyp: str) -> str:
    """
    Genereerib Maa-ameti Geoportaali LAZ-faili allalaadimise URL-i.

    Args:
        kaardiruut (str): Kaardi ruudu identifikaator EPK2T ruudu numbringa (nt "452659").
        andmetyyp (str): Andmetüüp - kas "tava" või "mets".

    Returns:
        str: Genereeritud allalaadimise URL.
    """
    base_url = "https://geoportaal.maaamet.ee/index.php"
    params = {
        'lang_id': '1',
        'plugin_act': 'otsing',
        'kaardiruut': kaardiruut,
        'andmetyyp': f'lidar_laz_{andmetyyp}',
        'dl': '1',
        'f': f'{kaardiruut}_{andmetyyp}.laz',
        # 'no_cache' parameeter võib vajada dünaamilist genereerimist,
        # kuid praegu on see fikseeritud vastavalt algsele skriptile.
        # See võib olla serveripoolne ajatempel või juhuslik string.
        'no_cache': '6855405e8f958',
        'page_id': '614'
    }
    # Kasutame urllib.parse.urlencode, et tagada parameetrite õige kodeerimine
    return f"{base_url}?{urlencode(params)}"

