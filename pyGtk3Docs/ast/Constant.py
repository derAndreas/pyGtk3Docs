

from Base import Base


class Constant(Base):
    """ Constant nodes <constant> are global GTK Constants
    The define their values as attributes with <type> subnodes
    """
    def parse_node(self):
        """ Parse the node """
        self.parse_attributes_from_map({
            'name'  : 'name',
            'value' : 'value',
            'ctype' : (self.NS_C, 'type')
        })
        
        #todo check if we can propagate the constant to the namespace
        #     and use it later when formatting the DOC. There is no
        #     parameter or returnvalue usage right now
