from pyrosim.commonFunctions import Save_Whitespace

class MATERIAL: 

    def __init__(self, color):

        self.depth  = 3

        self.string1 = f'<material name="{color[4]}">'

        self.string2 = f'    <color rgba="{color[0]} {color[1]} {color[2]} {color[3]}"/>'

        self.string3 = '</material>'

    def Save(self,f):

        Save_Whitespace(self.depth,f)

        f.write( self.string1 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string2 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string3 + '\n' )
