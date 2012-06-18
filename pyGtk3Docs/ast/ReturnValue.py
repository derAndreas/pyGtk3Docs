
from Base import Base

class ReturnValue(Base):
    """ Return value node <return-value>"""
    
    def parse_node(self):
        """ Parse the node"""
        self.parse_doc()
        self.type = self.parse_types(self.node)
    
    def toObjectRepr(self):
        """ Collect all needed informations and return them as a Dict
        
        Returns:
            Dict
        """
        return {
            'type' : self.getType().translate(True),
            'description' : self.getDoc(True)
        }

