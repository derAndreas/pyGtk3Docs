
from Base import Base

class Callback(Base):
    """ Callbacks nodes, used for signals """
    
    def parse_node(self):
        """ Parse the node """
        self.parse_attributes_from_map({
            'name'        : 'name',
            'ctype'       : (self.NS_C, 'type')
        })
        
        self.parse_parameters()
        self.parse_returnvalue()
        
        # propagate the Callback definition to the namespace
        self._namespace.registerType(self, self.getName(), self.getCType())

