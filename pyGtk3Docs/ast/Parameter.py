
from Base import Base

class Parameter(Base):
    """ Parameter nodes <parameter> are subnodes of <parameters> node.
    <parameters> do not have its own ast.* representation and the
    <parameter> nodes are directly parsed in the funtions, methods and so on
    and generate for each parameter node one of this ast.Parameter instance """
    
    def parse_node(self):
        """Parse the node """
        self.parse_attributes_from_map({
            'name'       : 'name',
            'direction'  : 'direction',
            'allow-none' : 'allowNone',
            'scope'      : 'scope',
            'destroy'    : 'destroy',
            'closure'    : 'closure',
            'caller-allocates' : 'callerAllocates'
        })
        
        self.parse_doc()
        self.type = self.parse_types(self.node)
    
    def toObjectRepr(self):
        """ Collect all needed informations and return a Dict
        
        Returns:
            Dict
        """
        return {
            'name' : self.name, # not all parameters in GIR File do have a 'name' attribute, dont use self.getName() here
            'type' : self.getType().translate(True),
            'description' : self.getDoc(True)
        }

