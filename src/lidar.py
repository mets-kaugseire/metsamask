import laspy
import pandas
import numpy as np
import requests


def read_las_file(file_path):
    """Read a LAS file and return its point data."""
    try:
        with laspy.open(file_path) as las_file:
            las_data = las_file.read()
            return pandas.DataFrame({
                "x": np.array(las_data.x),
                "y": np.array(las_data.y),
                "z": np.array(las_data.z),
                'classification': np.array(las_data.classification),
                'return_number': np.array(las_data.return_number)
            })
    except Exception as e:
        raise RuntimeError(f"Failed to read LAS file: {e}") from e

def read_las_directory(file_dir):
    """Read all LAS files in a directory and return their point data."""
    import os
    point_data = []
    for file_name in os.listdir(file_dir):
        if file_name.endswith('.laz') or file_name.endswith('.las'):
            file_path = os.path.join(file_dir, file_name)
            try:
                data = read_las_file(file_path)
                point_data.append(data)
            except RuntimeError as e:
                print(f"Error reading {file_name}: {e}")
    return pandas.concat(point_data, ignore_index=True) if point_data else pandas.DataFrame()

def download_las_file(url, save_path):
    """Download a LAS file from a URL and save it to the specified path."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded and saved to {save_path}")
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to download file: {e}") from e

def create_laz_url_path(kaardiruut, andmetyyp):
    params = {'lang_id': '1',
              'plugin_act': 'otsing',
              'kaardiruut': kaardiruut,
              'andmetyyp': 'lidar_laz_' + andmetyyp,
              'dl': '1',
              'f': kaardiruut + '_' + andmetyyp + '.laz',
              'no_cache': '6855405e8f958',
              'page_id': '614'}

    return f"https://geoportaal.maaamet.ee/index.php?{requests.compat.urlencode(params)}"


