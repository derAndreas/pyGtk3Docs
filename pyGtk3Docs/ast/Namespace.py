
from Base import Base

class Namespace(Base):
    """ Main global namespace node that contains all informations """
    
    def parse_node(self):
        """ Parse the node"""
        self._refTypesName = {}
        self._refTypesCType = {}
        self.aliases = []
        self.classes = []
        self.records = []
        self.functions = []
        self.constants = []
        self.enums = []
        self.bitfields = []
        self.callbacks = []
        self.ifaces = []
        
        self.parse_attributes_from_map({
            'name'                : 'name',
            'version'             : 'version',
            'identifier_prefixes' : (self.NS_C, 'identifier-prefixes'),
            'symbol_prefixes'     : (self.NS_C, 'symbol-prefixes')
        })
        
        self.parse_doc()
        
        
    
    def append(self, tag, ast_instance):
        """Append subnodes to the namespace node
        
        With the tag name the right bucket to store the ast instance
        is detected and simply append to array
        
        Arguments:
            tag -- String name of the node
            ast_instance -- the ast.* instance to append
        """
        
        if tag == 'alias':
            self.aliases.append(ast_instance)
        elif tag == 'class':
            self.classes.append(ast_instance)
        elif tag == 'record':
            self.records.append(ast_instance)
        elif tag == 'function':
            self.functions.append(ast_instance)
        elif tag == 'constant':
            self.constants.append(ast_instance)
        elif tag == 'enumeration':
            self.enums.append(ast_instance)
        elif tag == 'bitfield':
            self.bitfields.append(ast_instance)
        elif tag == 'callback':
            self.callbacks.append(ast_instance)
        elif tag == 'interface':
            self.ifaces.append(ast_instance)
        else:
            print "missed ", tag
        
    def toObjectRepr(self):
        """ Collect all useful informations and return them as a Dict
        
        Returns:
            Dict
        """
        return {
            'id' : 'root-namespace',
            'name' : self.getName(),
            'version': self.version,
            'identifierPrefix' : self.identifier_prefixes,
            'symbolPrefix' : self.symbol_prefixes,
            'members' : {
                'classes' : [cls.toObjectRepr() for cls in self.classes],
                'bitfields' : [bit.toObjectRepr() for bit in self.bitfields],
                'enumerations' : [enum.toObjectRepr() for enum in self.enums]
            }
        }
    
    def registerType(self, refObj, name, ctype=None):
        """Register Types so that they can be used for 
        mapping internal references. The ast.* (refObj) 
        is remembered with the plain namen and the C Type
        
        Arguments:
            refObj -- ast.* instance
            name   -- String
            ctype  -- String, default None
        
        Returns:
            void
        """
        self._refTypesName.update({name : refObj})
        if ctype is not None:
            self._refTypesCType.update({ctype : refObj})
    
    def findRegisteredType(self, value):
        """Find a type compared with the registered plain names
        and return the object that was registered with this name
        
        Arguments:
            value -- String name to find
        
        Returns:
            ast.* instance if something was found or None if nothing found
        """
        value = value.replace('*', '')
        for rkey, rval in self._refTypesName.iteritems():
            if rkey == value:
                return rval
        
        return None

    def findRegisteredCType(self, value):
        """Find a type compared with the registered C Type name
        and return the object that was registered with this C Type
        
        Arguments:
            value -- String CType name to find
        
        Returns:
            ast.* instance if something was found or None if nothing found
        """
        value = value.replace('*', '')
        for rkey, rval in self._refTypesCType.iteritems():
            if rkey == value:
                return rval
        
        return None
        
    def findRecordInstance(self, value, **kwargs):
        """ Find parsed <record> nodes by a value
        The value is the name or the ctype, which can be set by using
        **kwargs while calling this method with
            findRecordInstance(VALUE, by="name") for looking at 'name' attribute
            findRecordInstance(VALUE, by="ctype") for looking at 'ctype' attribute
        
        Arguments:
            value -- String value to search
            by    -- **kwargs parameter by with possible values "name" or "ctype"
        
        Returns:
            ast.Record instance or None if nothing found
        """
        
        if value is None:
            return None
        
        for record in self.records:
            name = record.name
            ctype = record.ctype
            
            if kwargs.get('by') == 'name' and value == name:
                return record
            elif kwargs.get('by') == 'ctype' and value == ctype:
                return record
            elif value == name or value == ctype:
                return record
                
        return None

    def findInterfaceInstance(self, value):
        """ Find parsed <interface> nodes by their name
        
        Arguments:
            value -- String name of the interface to look for
        
        Returns:
            ast.Iface instance or None if nothing found
        """
        
        if value is None:
            return None
        
        for iface in self.ifaces:
            if value == iface.name:
                return iface
        return iface

