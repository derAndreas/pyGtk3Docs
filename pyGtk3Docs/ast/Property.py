
from Base import Base

class Property(Base):    
    """Class Property nodes <property>"""
    
    def parse_node(self):
        """ Parse the node"""
        self.parse_attributes_from_map({
            'name'       : 'name',
            'version'    : 'version',
            'readable'   : 'readable',
            'writable'   : 'writable',
            'deprecated' : 'deprecated',
            'construct'  : 'construct',
            'construct-only' : 'construct-only',
            'deprecated-version' : 'deprecated-version'
        })
        
        # fix attributes
        if self.writable == 1:
            self.writable = True
        else:
            self.writable = False
        
        if self.readable == 1:
            self.readable = True
        else:
            self.readable = False
        
        self.parse_doc()
        self.type = self.parse_types(self.node)
        
        
    def toObjectRepr(self):
        """ Collect all needed informations and return them as a Dict
        
        Returns:
            Dict
        """
        return {
            'name' : self.name,
            'writable' : self.writable,
            'readable' : self.readable,
            'type' : self.type.translate(),
            'description': self.getDoc(True)
        }

