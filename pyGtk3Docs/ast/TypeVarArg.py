
from Base import Base

class TypeVarArg(Base):
    """ TypeVarArg node "<vararg>" """
    def __init__(self, namespace, node):
        Base.__init__(self, namespace, node)
        self.type = 'VarArg'
        
    def parse_node(self):
        """Parse not possible, just use the instance with ::translate() method"""
        pass
        
    def translate(self, asRef=False):
        return self._translate(self.type, asRef)
    
    def _translate(self, value, asRef):
        if asRef is False:
            return value
        else:
            return "ref:%s" % value
