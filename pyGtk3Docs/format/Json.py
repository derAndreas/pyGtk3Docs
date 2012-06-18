

from .Base import BaseFormat
import json

class Json(BaseFormat):
    """ Simple JSON formatter"""
    def __init__(self, converter):
        self.result = {}
        BaseFormat.__init__(self, converter)
        
    
    def walk(self):
        """Walk the AST Tree and update self.result"""
        self.result.update(self.converter.getNamespaceTag().toObjectRepr())
        
    def getResult(self):
        """ Get the result from the formatter (final output result)"""
        return json.dumps(self.result, indent=4)
    
    def write(self, dest):
        fhandle = open(dest, 'w')
        fhandle.write(output.getResult())
        fhandle.close()

