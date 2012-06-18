

from Base import Base


class Doc(Base):
    """ Documentation Tag Element <doc>"""
    
    def __init__(self, namespace, node):
        self.value = ''
        Base.__init__(self, namespace, node)
    
    def parse_node(self):
        """ Parse the node if there is any node.text value"""
        if self.node.text is not None:
            self.value = self.node.text
    
    def toObjectRepr(self):
        """ Return the value, but not as an object, just the plain text
        
        TODO: this should be changed to have a consistent API
        """
        return self.value
