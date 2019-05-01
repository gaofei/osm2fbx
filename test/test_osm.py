from osm2fbx.osm.module import *

def test_get_coords(id, path):
    p = DataPreprocessor()
    manager = OSManager(path, p)
    data = manager.get_coords_from_wayid(id)
    print(data)

test_get_coords(117914843, 'assets/map.osm')
