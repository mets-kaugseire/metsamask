import laspy
import pandas
import numpy as np

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