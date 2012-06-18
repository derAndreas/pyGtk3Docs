
from Base import Base

class Signal(Base):    
    """Signals are events that can be listen on and invoke callbacks"""
    
    def parse_node(self):
        """Parse the node"""
        self.parse_attributes_from_map({
            'name'    : 'name',
            'version' : 'version',
            'when'    : 'when',
            'deprecated' : 'deprecated',
            'deprecated-version' : 'deprecated-version',
            'action' : 'action',
            'no-recurse' : 'no-recurse',
            'no-hooks' : 'no-hooks',
            'detailed' : 'detailed'
        })
        
        self.parse_doc()
        self.parse_returnvalue()
        self.parse_parameters()
        

    def toObjectRepr(self):
        """Collect all informations and return them as a Dict
        
        Returns:
            Dict
        """
        return {
            'name': self.getName(),
            'version': self.getVersion(),
            'when' : self.when,
            'description' : self.getDoc(True)
        }

