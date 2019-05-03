import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from osm2fbx.osm.module import *
from pytest import approx


path = "assets/map.osm"
id = 26658458
sortedby = "lat"


def get_pos_list():
    ps = DataPreprocessor()
    om = OSManager(path, ps)
    pos = om.get_pos_from_coords_by_wayid(id, offset=10, sortedby=sortedby)

    return pos[:]


def get_center_list(left, right):
    center = []
    for idx, __ in enumerate(left):
        _ = tuple(map(lambda x: sum(x)/2, zip(left[idx], right[idx])))
        center.append(_)

    return center[:]


def test_pos_center_is_equal_coord():
    ps = DataPreprocessor()
    om = OSManager(path, ps)
    coords = om.get_coords_from_wayid(id, sortedby)

    left, right = get_pos_list()
    center = get_center_list(left, right)
    for co, ce in zip(coords, center):
        assert co == approx(ce)
