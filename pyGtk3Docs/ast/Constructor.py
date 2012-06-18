
from Function import Function
from lxml import etree

class Constructor(Function):
    """ The <constructor> node(s) describe ways to initiaite a new object
    There are multiple ways to create a new object, with none or some parameters.
    Currently the self.name contains the differences, but this could merged
    later to one constructor with an extended/modified ast.Doc object to
    describe the differences.
    """
    
    def toObjectRepr(self, clsName):
        """ Collect all parsed informations and return
        a python object that can be processed later for output.
        The 'name' attribute will describe the differences of creating an
        instance of the object to create 
        
        Arguments
            clsName -- the class name that this constructor is used for
                       this name is needed to create a valid representation
                       of the name of the class to instantiate
        
        Returns
            Dict
        """
        params = None
        
        if len(self.parameters) > 0:
            paramsPlaceholder = []
            params = []
            for param in self.parameters:
                paramsPlaceholder.append("%s %s" % (param.getType().translate(), param.name))
                params.append({
                    'name' : param.name,
                    'type' : param.getType().translate(True)
                })
                
            name = "Gtk.%s(%s)" % (clsName, ', '.join(paramsPlaceholder))
        else:
            name = "Gtk.%s()" % clsName

        result =  {
            'isConstructor' : True,
            'name' : name,
            'version' : self.version,
            'description' : self.getDoc(True),
            'returns' : {
                'name' : self.returnValue.getType().translate(True),
                'doc' : self.returnValue.doc.toObjectRepr()
            },
            'parameters' : params
        }
        
        if self.deprecated is not None:
            result.update({
                'deprecated'  : self.deprecated, 
                'deprecated_version' : self.deprecated_version
            })
        
        
        return result

