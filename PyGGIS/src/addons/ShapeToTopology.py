from OCC.TopoDS import *
from OCC.TopAbs import *


class ShapeToTopology(object):

    def __init__(self):
        self.tds = topods
        self.topology_types = {TopAbs_COMPOUND: self.tds.Compound,
                               TopAbs_COMPSOLID: self.tds.CompSolid,
                               TopAbs_SOLID: self.tds.Solid,
                               TopAbs_SHELL: self.tds.Shell,
                               TopAbs_FACE: self.tds.Face,
                               TopAbs_WIRE: self.tds.Wire,
                               TopAbs_EDGE: self.tds.Edge,
                               TopAbs_VERTEX: self.tds.Vertex}

    def __call__(self, shape):
        if isinstance(shape, TopoDS_Shape):
            return self.topology_types[shape.ShapeType()](shape)
        else:
            raise AttributeError('shape has not method `ShapeType`')