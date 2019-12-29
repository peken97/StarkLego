from ldraw.library.parts.others import Brick2X2
from ldraw.pieces import Group, Piece
from ldraw.figure import *
from ldraw.geometry import Identity
from ldraw.library.colours import *



class LdrawSpecification():
    def __init__(self, line_type, color, x, y, z, piece_file_name):
        self.line_type = line_type
        self.color = color
        self.x = x
        self.y = y
        self.z = z
        self.piece_file_name = piece_file_name

class StarkBlock():
    def __init__(self, dim_x, dim_y, dim_z, coor_x, coor_y, coor_z):
        self.dimensions = StarkDimensions(dim_x, dim_y, dim_z)
        self.coordinates = StarkDimensions(float(coor_x), float(coor_y), float(coor_z), flag_convert_from_ldraw=True)
    def __repr__(self):
        return "Dimensions: ({}, {}, {}), Coordinates: ({}, {}, {})".format(self.dimensions.x, self.dimensions.y, self.dimensions.z,self.coordinates.x, self.coordinates.y, self.coordinates.z)

class LdrawBlock():
    def __init__(self, dim_x, dim_y, dim_z, coor_x, coor_y, coor_z):
        self.dimensions = LdrawDimensions(dim_x, dim_y, dim_z)
        self.coordinates = LdrawDimensions(float(coor_x), float(coor_y), float(coor_z), flag_convert_from_stark=True)
    def __repr__(self):
        return "Dimensions: ({}, {}, {}), Coordinates: ({}, {}, {})".format(self.dimensions.x, self.dimensions.y, self.dimensions.z,self.coordinates.x, self.coordinates.y, self.coordinates.z)


class TwoXTwoBlock():        

    def create(self, x, y, z, group=Group()):
        positionDimensions = StarkDimensions(x=x, y=y, z=z)
        convertedX, convertedY, convertedZ = positionDimensions.convertToLdrDimensions()
        return Piece(Dark_Blue, Vector(x=convertedX, y=convertedY, z=convertedZ), Identity(), Brick2X2, group).__repr__()

class Dimensions():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class LdrawDimensions(Dimensions):
    def __init__(self, x, y, z, flag_convert_from_stark=False):
        if not flag_convert_from_stark:
            super().__init__(x, y, z)
        else:
            x, y, z = self.convertFromStarkDimensions(x,y,z)
            super().__init__(x, y, z)

    def convertToStarkDimensions(self, x, y, z):
        return x / 20, y / -8, z / 20
    def convertFromStarkDimensions(self, x, y, z):
        return x * 20, y * -8, z * 20

class StarkDimensions(Dimensions):
    def __init__(self, x, y, z, flag_convert_from_ldraw=False):
        if not flag_convert_from_ldraw:
            super().__init__(x, y, z)
        else:
            x, y, z = self.convertFromLdrDimensions(x,y,z)
            super().__init__(x, y, z)

    def convertToLdrDimensions(self, x, y, z):
        return x * 20, y * -8, z * 20
    def convertFromLdrDimensions(self, x, y, z):
        return int(x / 20), int(y / -8), int(z / 20)
