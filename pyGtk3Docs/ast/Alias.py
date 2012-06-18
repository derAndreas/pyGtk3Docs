

from Base import Base

class Alias(Base):
    """ Alias <alias> nodes"""
    
    def parse_node(self):
    
        self.parse_attributes_from_map({
            'name'     : 'name',
            'ctype' : (self.NS_C, 'type')
        })
        
        self.parse_doc()
        self.type = self.parse_types(self.node)
        
        # propagate the created alias type to the namespace
        self._namespace.registerType(self, self.name, self.ctype)

