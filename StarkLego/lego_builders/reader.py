from StarkLego.lego_builders.model import LdrawSpecification, StarkBlock
from StarkLego.lego_builders.builder import TwoXTwoBlock, LegoWorld

import traceback

class LdrawFileReader():
    def __open(self, file_name):
        file = open(file_name, "r")
        if file.mode == 'r':
            contents_in_list = file.readlines()
            return contents_in_list
        return []

    def readAndBuildLegoWorld(self, file_name):
        self.buildLegoWorld(self.read(file_name))

    def buildLegoWorld(self, list_of_blocks):
        lego_world_max_x = 0
        lego_world_max_y = 0
        lego_world_max_z = 0
        for block in list_of_blocks:
            print(block.__repr__())
            if (block.dimensions.x + block.coordinates.x) > lego_world_max_x:
                lego_world_max_x = block.dimensions.x + block.coordinates.x
            if (block.dimensions.y + block.coordinates.y) > lego_world_max_y:
                lego_world_max_y = block.dimensions.y + block.coordinates.y
            if (block.dimensions.z + block.coordinates.z) > lego_world_max_z:
                lego_world_max_z = block.dimensions.z + block.coordinates.z
        print(lego_world_max_x, lego_world_max_y, lego_world_max_z)
        lego_world = LegoWorld(lego_world_max_x, lego_world_max_y + 1, lego_world_max_z)
        for block in list_of_blocks:
            lego_world.addPartToWorld(TwoXTwoBlock(), block.coordinates.x,  block.coordinates.z)
        print(lego_world.ldrContent)
    def read(self, file_name):
        contents_in_list = self.__open(file_name)
        list_of_blocks = []
        for content in contents_in_list:
            list_of_blocks.append(self.__parseLine(content.strip("\n")))
        return list_of_blocks
    
    def __parseLine(self, content):
        space_seperated_content = content.split(" ")
        if space_seperated_content == "" or space_seperated_content == "\n":
            return None
        try:
            ldraw_content_type = space_seperated_content[0]
            ldraw_color = space_seperated_content[1]
            ldraw_x = space_seperated_content[2]
            ldraw_y = space_seperated_content[3]
            ldraw_z = space_seperated_content[4]
            ldraw_piece_file_name = space_seperated_content[14]

            ldraw_specification = LdrawSpecification(ldraw_content_type, ldraw_color, ldraw_x, ldraw_y, ldraw_z, ldraw_piece_file_name)
            
            return self.__convert(ldraw_specification)

        except Exception as e:
            print(e)
            traceback.format_exc()
            traceback.print_exc()
            return None
    
    def __convert(self, specification):
        if type(specification).__name__ != LdrawSpecification.__name__:
            raise Exception("Wrong specification type, was expecting", LdrawSpecification.__name__, "but got", type(specification).__name__)

        block_size_dimensions = self.__file_to_block_mapper(specification.piece_file_name)
        block_to_return = StarkBlock(block_size_dimensions.x, block_size_dimensions.y, block_size_dimensions.z, specification.x, specification.y, specification.z)
        return block_to_return

    def __file_to_block_mapper(self, file_name):        
        if file_name == '3003.DAT':
            return TwoXTwoBlock().sizeDimensions