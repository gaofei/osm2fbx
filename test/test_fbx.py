import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from osm2fbx.fbx.module import *
from osm2fbx.osm.module import *
from pytest import approx

path = "assets/map.osm"
offset = 10000000
oi = OSMImporter(path, offset)
structure = oi.get_osm_structure()
manager, scene = FbxCommon.InitializeSdkObjects()


def test_way_structure():
    ws = WayStructure(structure, 10, "red")
    vs = ws.get_way_vertex()

    assert 506252744 in vs


def test_streetbuilder():
    sb = StreetBuilder(manager, scene, structure)
    sb.draw_scene(10, 20.0, "red")


def test_fbx_export():
    FbxCommon.SaveScene(manager, scene, "./assets/result.fbx")
