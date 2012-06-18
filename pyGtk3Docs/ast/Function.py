
from Base import Base

class Function(Base):
    """ Function nodes <function>
    This class is also the base class for <method>, <virutal-method> and
    <constructor> nodes, as the have all the same signature """
    
    def parse_node(self):
        """ Parse the node"""
        self.parse_attributes_from_map({
            'name'        : 'name',
            'cidentifier' : (self.NS_C, 'identifier'),
            'version'     : 'version',
            'deprecated'  : 'deprecated', 
            'deprecated_version' : 'deprecated-version', 
            'invoker'     : 'invoker', 
            'throws'      : 'throws', 
            'shadows'     : 'shadows', 
            'shadowed-by' : 'shadowed-by'
        })
        
        self.parse_doc()
        self.parse_parameters()
        self.parse_returnvalue()
        
    def toObjectRepr(self):
        """ Collect all informations about the function or derived ast element """
        params = None
        doc = None
        
        if len(self.parameters) > 0:
            #paramsPlaceholder = []
            params = []
            for param in self.parameters:
                #paramsPlaceholder.append("%s %s" % (param.getType().translate(), param.name))
                params.append(param.toObjectRepr())
                
        
        if hasattr(self.returnValue, 'doc'):
            doc = self.returnValue.doc.toObjectRepr()
        
        
        result = {
            'name' : self.getName(),
            'version' : self.getVersion(),
            'description' : self.getDoc(True),
            'returns' : self.returnValue.toObjectRepr(),
            'parameters' : params
        }
        
        return result

