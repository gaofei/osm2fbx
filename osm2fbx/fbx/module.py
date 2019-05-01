import fbx
import FbxCommon


class FbxManager:
    def __init__(self, x=10, y=10):
        self.sdkmanager, self.scene = FbxCommon.InitializeSdkObjects()
        self.padding_x = x;
        self.padding_y = y;

    def set_polygon_padding(self, x, y):
        self.padding_x = x;
        self.padding_y = y;

    def __create_polygon(self, key, coords):
        print('placeholder')

    def __cal_rect_vertex_pos(self, coords):
        pos_offset = [
            (-self.padding_x, -self.padding_y),
            (-self.padding_x, self.padding_y),
            (self.padding_x, -self.padding_y),
            (self.padding_x, self.padding_y)
        ]
        rect_pos = []
        for coord in coords:
            print map(sum, map(lambda x: zip(x, coord), pos_offset))

        print rect_pos

    def cal_rect_vertex_pos(self, coords):
        self.__cal_rect_vertex_pos(coords)

    def create_scene(self, node_coords, way_nodes):
        for key in way_nodes:
            node_coords[key]
