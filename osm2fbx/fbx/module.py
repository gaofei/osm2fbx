# -*- coding: utf-8 -*-
import fbx
import FbxCommon


"""
    Structure
        self.coord_id_list = []
            self.way_id_list = []
            self.ways_dict = {}
            self.coords_dict = {}
            self.normalized_coords_dict = {}
            self.average = 0.0
"""

class FBXStructure:
    """
    지금은 그냥 길만 만들지만
    나중엔 이거 상속해서 건물 스트럭쳐도 만들것이므로
    확장성에 신경쓰자
    """
    def __init__(self, color, structure):
        self.color = color
        self.__structure = structure


class WayStructure:
    def __init__(self, structure, pos_Z, color, ):
        self.__color = color
        self.__pos_Z = pos_Z
        self.__structure = structure
        self.__processor()

    def __processor(self):
        way_id_list = self.__structure.way_id_list
        self.__way_vertex = {}

        for way_id in way_id_list:
            node_refs = self.__structure.ways_dict[way_id]
            coords = self.__node_refs_to_coord(node_refs)
            vertex4_list = self.__coords_to_vertex4(coords)

            self.__way_vertex[way_id] = vertex4_list

    def __node_refs_to_coord(self, refs):
        coords_dict = self.__structure.normalized_coords_dict
        coords = [coords_dict[ref] for ref in refs]
        return coords

    def __coords_to_vertex4(self, coords):
        fbx_list = [
            fbx.FbxVector4(coord[0], coord[1], self.__pos_Z, 1) for coord in coords
        ]
        return fbx_list

    def get_way_vertex(self):
        return self.__way_vertex.copy()


class StreetBuilder:
    def __init__(self, fbx_manager, scene, structure):
        self.fbx_manager = fbx_manager
        self.scene = scene
        self.structure = structure
        self.root_node = fbx.FbxNode.Create(self.fbx_manager, "ROOT_NODE")

    def draw_scene(self, pos_Z, thickness, color):
        ws = WayStructure(self.structure, pos_Z, color)
        way_ids = self.structure.way_id_list

        self.__draw_way(way_ids, ws.get_way_vertex(), thickness, color)
        scene_root_node = self.scene.GetRootNode()
        scene_root_node.AddChild(self.root_node)

    def __draw_way(self, way_ids, way_vertex_list, thickness, color):
        for id in way_ids:
            vertexes = way_vertex_list[id]
            for idx in range(len(vertexes) - 1):
                self.__add_2d_line_mesh(vertexes[idx], vertexes[idx+1], thickness, color)

    def __add_2d_line_mesh(self, start, end, thickness, color):
        direction = (end - start)
        direction.Normalize()
        right_vector = fbx.FbxVector4(-direction[1], direction[0], direction[3])

        bottom_left_vertex = (start - right_vector * thickness)
        bottom_right_vertex = (start + right_vector * thickness)

        top_left_vertex = (end - right_vector * thickness)
        top_right_vertex = (end + right_vector * thickness)

        self.__create_mesh(bottom_left_vertex, bottom_right_vertex, top_left_vertex)
        self.__create_mesh(top_left_vertex, top_right_vertex, bottom_right_vertex)

    def __create_mesh(self, vertex1, vertex2, vertex3):
        mesh = fbx.FbxMesh.Create(self.fbx_manager, "")
        node = self.__create_node()

        mesh.InitControlPoints(3)

        mesh.SetControlPointAt(vertex1, 0)
        mesh.SetControlPointAt(vertex2, 1)
        mesh.SetControlPointAt(vertex3, 2)

        mesh.BeginPolygon()
        mesh.AddPolygon(0)
        mesh.AddPolygon(1)
        mesh.AddPolygon(2)
        mesh.EndPolygon()

        node.AddNodeAttribute(mesh)
        self.root_node.AddChild(node)

    def __create_node(self):
        return fbx.FbxNode.Create(self.fbx_manager, "")


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
            print idx
            print cp
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
