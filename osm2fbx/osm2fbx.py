from fbx.module import *
from osm.module import *


if __name__ == '__main__':
    oi = OSMImporter('assets/map.osm', 1000)
    structure = oi.get_osm_structure()
    sc = SceneCreator(structure)
    sc.draw_scene()
    sc.save_scene()