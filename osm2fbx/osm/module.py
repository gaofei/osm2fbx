from imposm.parser import OSMParser
from copy import deepcopy


class DataProcessor(object):
    class OSMStructure:
        def __init__(self):
            self.coord_id_list = []
            self.way_id_list = []
            self.ways_dict = {}
            self.coords_dict = {}
            self.normalized_coords_dict = {}
            self.average = 0.0

    def __init__(self):
        self.__structure = self.OSMStructure()

    def callback_ways(self, ways):
        # callback method for ways
        for osmid, tags, refs in ways:
            self.__structure.way_id_list.append(osmid)
            self.__structure.ways_dict[osmid] = refs

    def callback_coords(self, coords):
        for osmid, lon, lat in coords:
            self.__structure.coord_id_list.append(osmid)
            self.__structure.coords_dict[osmid] = (lon, lat)

    def __measure_coords_avg(self):
        lon_avg = 0.0
        lat_avg = 0.0

        for lon, lat in self.__structure.coords_dict.itervalues():
            lon_avg += lon
            lat_avg += lat

        lon_avg = lon_avg / len(self.__structure.coords_dict)
        lat_avg = lat_avg / len(self.__structure.coords_dict)

        avg = (lon_avg, lat_avg)

        return avg

    def __normalized_coords(self, avg, offset):
        norm_coord = {}
        for key in self.__structure.coords_dict:
            val = self.__structure.coords_dict[key]
            norm_coord[key] = tuple(map(lambda x: (x[0]*offset - x[1]*offset), zip(val, avg)))

        print norm_coord
        return norm_coord

    def pre_processing(self, offset):
        avg = self.__measure_coords_avg()
        normalized_coords = self.__normalized_coords(avg, offset)

        self.__structure.average = avg
        self.__structure.normalized_coords_dict = normalized_coords

        return deepcopy(self.__structure)


class OSMImporter:
    def __init__(self, path, offset):
        self.__processor = DataProcessor()
        self.__path = path
        way = OSMParser(concurrency=4, ways_callback=self.__processor.callback_ways)
        coord = OSMParser(concurrency=4, coords_callback=self.__processor.callback_coords)

        way.parse(path)
        coord.parse(path)

        self.__structure = self.__processor.pre_processing(offset)

    def get_osm_structure(self):
        return deepcopy(self.__structure)
