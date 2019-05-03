from imposm.parser import OSMParser


class DataPreprocessor(object):
    def __init__(self):
        self.__ways = {}
        self.__coords = {}

    def callback_ways(self, ways):
        # callback method for ways
        for osmid, tags, refs in ways:
            self.__ways[osmid] = refs

    def callback_coords(self, coords):
        for osmid, lon, lat in coords:
            self.__coords[osmid] = (lon, lat)

    def __measure_coords_avg(self):
        if not self.__coords:
            raise AttributeError

        l = []
        for lon, lat in self.__coords.itervalues():
            l.append((lon, lat))

        out = list(map(sum, zip(*l)))
        avg = map(lambda x: x/len(self.__coords), out)
        return avg

    def __normalized_coords(self, offset):
        norm_coord = {}
        for key in self.__coords:
            val = self.__coords[key]
            norm_coord[key] = tuple(map(lambda x: (x[0] - x[1]) * 10000, zip(val, offset)))

        return norm_coord

    def preprocessing(self, path):
        avg = self.__measure_coords_avg()
        normalized_coords = self.__normalized_coords(avg)
        return self.__ways, normalized_coords


class OSManager:
    def __init__(self, path, data_preprocessor):
        self.__preprocessor = data_preprocessor
        self.__path = path
        way = OSMParser(concurrency=4, ways_callback=self.__preprocessor.callback_ways)
        coord = OSMParser(concurrency=4, coords_callback=self.__preprocessor.callback_coords)

        way.parse(path)
        coord.parse(path)

        self.ways, self.coords =self.__preprocessor.preprocessing(path)

    def get_pos_from_coords_by_wayid(self, id, offset, sortedby="None"):
        coords = self.get_coords_from_wayid(id, sortedby)

        if sortedby == "lon":
            left = [(x + offset, y) for x, y in coords]
            right = [(x - offset, y) for x, y in coords]
        else:
            left = [(x, y + offset) for x, y in coords]
            right = [(x, y - offset) for x, y in coords]

        return left, right

    def get_coord_from_nodeid(self, id):
        return self.coords[id]

    def get_coords_from_wayid(self, id, sortedby="None"):
        ref = self.ways[id]
        coords = [self.get_coord_from_nodeid(co) for co in ref]

        if sortedby == "lon":
            coords.sort(key=lambda tup: tup[0])
        elif sortedby == "lat":
            coords.sort(key=lambda tup: tup[1])

        return coords

