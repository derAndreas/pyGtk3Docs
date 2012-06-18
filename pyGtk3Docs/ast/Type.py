
from Base import Base
from Record import Record
from ..TypeDef import TypeDef
from ..TypeDef import BASIC_TYPES


class Type(Base):
    """Type node <type> define a type of a parameter or return value and so on
    To match a ctype to a python type the ast.Type* are used
    """
    
    def __init__(self, namespace, node):
        Base.__init__(self, namespace, node)
    
    def parse_node(self):
        """Parse the node"""
        self.parse_attributes_from_map({
            'name'          : 'name',
            'ctype'         : (self.NS_C, 'type')
        })
        
        
    def translate(self, asRef=False):
        """ Translate the type value to a TypeDef instance or if a 
        external Type is used, return a string or try to match Record Instances
        
        Arguments:
            asRef -- True to return the result string as a ref: indicating string
                     to create links in the output
        
        Returns:
            Returns a String
        """
        
        result = None
    
        if self.ctype is not None:
            compareType = self.ctype
        elif self.name is not None:
            compareType = self.name
        else:
            raise ValueError('No Type attribute in type tag')
        
        if self.name.find('.') > 0:
            # type is an external libraray like Gio, Gdk
            result = self.name
        else:
            for t in BASIC_TYPES:
                if t == compareType:
                    result = t
            
            if self._hasGTKCTypeAttrib():
                # lookup GTK Object
                result = self._namespace.findRegisteredCType(self.ctype)
            elif self._namespace.findRegisteredType(self.name) is not None:
                # check with name attribute
                result = self._namespace.findRegisteredType(self.name)
            
        # check for types that are defined through <record> tags
        if self._hasGTKCTypeAttrib():
            record = self._namespace.findRecordInstance(self.name)
            if record is not None:
                result = record
        elif result is None:
            # check with name attrib, could be working
            record = self._namespace.findRecordInstance(self.name)
            if record is not None:
                result = record
                
            
        
        if result is not None:
            if isinstance(result, str):
                return self._translate(result, False)
            elif isinstance(result, Record):
                return self._translate("Gtk.%s" % result.name, asRef)
            elif isinstance(result, Base):
                return self._translate("Gtk.%s" % result.name, asRef)
            elif isinstance(result, TypeDef):
                return self._translate(result.getPython(), False)
            else:
                raise ValueError('Unknown instancetype')
                
        raise ValueError('Type not resolved: ', self.name, self.ctype)


    def _translate(self, value, asRef):
        """ Helper function for self::translate() to return a string
        representation.
        
        Arguments:
            value -- the value to format
            asRef -- True to return as referencable string by prefixing with ref:
        
        Returns:
            String
        """
        
        if asRef is False:
            return value
        else:
            return "ref:%s" % value
    
    def _hasGTKCTypeAttrib(self):
        return hasattr(self, 'ctype') and self.ctype is not None and self.ctype[0:3] == 'Gtk'
