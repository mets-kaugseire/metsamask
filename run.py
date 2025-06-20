from src.load_config import *
from src.lidar import *
from pathlib import Path

if __name__ == "__main__":
    # Define the path to the JSON file
    json_file_path = 'config.json'
    print(dir())
    
    try:
        # Load the JSON data
        data = load_json(json_file_path)
        print("Konfiguratsioon loetud edukalt:")
        print(data)
    except Exception as e:
        print(f"Viga: {e}")

    las_path = Path(data['lidar_laz_dir']) / "2008_tava" / "51281"


    point_data = read_las_directory(las_path)
    print(f"Loetud punktide arv: {len(point_data)}")
    
    point_data['x_i'] = point_data['x'].round(-1).astype(int)
    point_data['y_i'] = point_data['y'].round(-1).astype(int)
    print(point_data.head())
