# -*- coding: utf-8 -*-
import fbx
import FbxCommon


class WayStructure:
    """

    """
    def __init__(self, structure, pos_Z, color, ):
        self.__color = color
        self.__pos_Z = pos_Z
        self.__structure = structure
        self.__processor()

    def __processor(self):
        """

        :return: None
        """
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
            fbx.FbxVector4(coord[1], coord[0], self.__pos_Z, 1) for coord in coords
        ]
        return fbx_list

    def get_way_vertex(self):
        return self.__way_vertex.copy()


class StreetBuilder:
    """
    Build a street
    """
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

        self.__create_mesh(bottom_left_vertex, bottom_right_vertex, top_left_vertex, top_right_vertex)

    def __create_mesh(self, vertex1, vertex2, vertex3, vertex4):
        mesh = fbx.FbxMesh.Create(self.fbx_manager, "")
        node = self.__create_node()

        mesh.InitControlPoints(3)

        mesh.SetControlPointAt(vertex1, 0)
        mesh.SetControlPointAt(vertex2, 1)
        mesh.SetControlPointAt(vertex3, 2)
        mesh.SetControlPointAt(vertex4, 3)

        mesh.BeginPolygon()
        mesh.AddPolygon(0)
        mesh.AddPolygon(1)
        mesh.AddPolygon(2)
        mesh.EndPolygon()

        mesh.BeginPolygon()
        mesh.AddPolygon(1)
        mesh.AddPolygon(2)
        mesh.AddPolygon(3)
        mesh.EndPolygon()

        node.AddNodeAttribute(mesh)
        self.root_node.AddChild(node)

    def __create_node(self):
        return fbx.FbxNode.Create(self.fbx_manager, "")


class SceneCreator:
    """
    [EN]
    SceneCreator is creating scene and generation 3D node on it.
    """
    def __init__(self, structure=None):
        manager, scene = FbxCommon.InitializeSdkObjects()
        self.__manager = manager
        self.__scene = scene
        self.__root_node = fbx.FbxNode.Create(self.__manager, "OSM2FBX ROOT")
        self.__structure = structure

    def register_structure(self, structure):
        """
        [EN]
        Register structure from OSMImporter at SceneCreator Instance

        :param structure:
        :return none:
        """
        self.__structure = structure

    def draw_scene(self, pos_z, thickness, color):
        """
        [EN]
        drawing scene, need z pos(thickness way z), thickness(way width), color(way color)

        :param pos_z:
        :param thickness:
        :param color:
        :return boolean:
        """
        sb = StreetBuilder(self.__manager, self.__scene, self.__structure)
        sb.draw_scene(pos_z, thickness, color)
        return True

    def save_scene(self, path="out.fbx"):
        FbxCommon.SaveScene(self.__manager, self.__scene, path)
        return True

