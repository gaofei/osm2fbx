import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from osm2fbx.osm.module import *
from pytest import approx


path = "assets/map.osm"
id = 26658458
offset = 100000
sortedby = "lat"
oi = OSMImporter(path, offset)
structure = oi.get_osm_structure()

