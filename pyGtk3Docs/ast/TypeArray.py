
from Base import Base

#debug
from lxml import etree


class TypeArray(Base):
    """ Array Type used in Parameters or ReturnValue to indicate an array of <X>
    """
    def parse_node(self):
        self.parse_attributes_from_map({
            'ctype'         : (self.NS_C, 'type'),
            'length'        : 'length',
            'zeroTerminated' : 'zero-terminated',
            'fixedSize'     : 'fixed-size'
        })
        
        
        self.type = self.parse_types(self.node)
    
    def translate(self, asRef=False):
        """ Translate the array to a string representation"""
        return '%s[]' % self.type.translate(asRef)
