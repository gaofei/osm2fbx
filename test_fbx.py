from osm2fbx.fbx.module import *


def test_cal_rect_vertex_pos(manager, coords):
    manager.cal_rect_vertex_pos(coords)


if __name__ == '__main__':
    m = FbxManager()
    test_cal_rect_vertex_pos(m, [(-32, 5)])
