# -*- coding: utf-8 -*-
import fbx
import FbxCommon


class SceneCreator:
    """
    [EN]
    SceneCreator is creating scene and generation 3D node on it.
    Method List:
        private:
            __create_mesh(control_point):
                Get attribute to preprocessed control point and create mesh
                (by get_rect_vertex_pos)
                return type: fbx.FbxMesh

        public:
            generate_scene():
                Register polygon in created scene

    [KO]
    SceneCreator 에서는 씬을 생성하고 해당 씬에 3D 노드를 생성합니다

    Method List:
        private:
            __create_polygon_mesh(control_point):
                전처리된 폴리곤 꼭짓점들을 받아 메쉬를 생성합니다. (get_rect_vertex_pos에 의해)
                return type: fbx.FbxMesh

        public:
            generate_scene():
                생성된 씬 안에 만들어진 폴리곤들을 등록합니다.
    """
    def __init__(self, manager, scene):
        self.__manager = manager
        self.__scene = scene
        self.__root_node = fbx.FbxNode.Create(self.__manager, "OSM2FBX ROOT")

    def __register_node(self, node):
        self.__root_node.AddChild(node)

    def create_mesh(self, control_point, name=""):
        mesh = fbx.FbxMesh.Create(self.__manager, name)
        mesh.InitControlPoints(4)
        for idx, cp in enumerate(control_point):
            mesh.SetControlPointAt(cp, idx)

        vtxId = [
            0, 1, 2, 3
        ]

        mesh.BeginPolygon()
        for id in vtxId:
            mesh.AddPolygon(id)
        mesh.EndPolygon()

        return mesh

    def create_node(self, name=""):
        node = fbx.FbxNode.Create(self.__manager, name)

        return node

    def create_way_polygon(self, control_points,  z=1, name=""):
        for cp in control_points:
            node = self.create_node(name)
            node.SetNodeAttribute(self.create_mesh(cp))
            node.SetShadingMode(fbx.FbxNode.eTextureShading)
            self.__root_node.AddChild(node)

    def generate_scene(self, control_points):
        root_node = self.__scene.GetRootNode()
        self.create_way_polygon(control_points)
        root_node.AddChild(self.__root_node)


class Osm2FbxProcessor:
    def __init__(self, x=10, y=10):
        self.__padding_x = x;
        self.__padding_y = y

    def __cal_rect_vertex_pos(self, coords):
        pos_offset = [
            (-self.__padding_x, -self.__padding_y),
            (-self.__padding_x, self.__padding_y),
            (self.__padding_x, -self.__padding_y),
            (self.__padding_x, self.__padding_y)
        ]

        rect_list = []
        for coord in coords:
            rect = []
            for offset in pos_offset:
                rect.append(
                    list(map(sum, zip(coord, offset)))
                )

            rect_list.append(rect[:])

        return rect_list[:]

    def get_rect_vertex_pos(self, coords):
        return self.__cal_rect_vertex_pos(coords)

    def set_polygon_padding(self, x, y):
        self.__padding_x = x;
        self.__padding_y = y;

