

from Base import Base

class Record(Base):
    """Record nodes <record> are supplying definitions for classes
    Classes have an attribute called "glib:type-struct" that match a <record>
    node for additional informations for the class"""
    
    def parse_node(self):
        """Parse the node"""
        self.parse_attributes_from_map({
            'name'             : 'name',
            'ctype'            : (self.NS_C, 'type'),
            'disguised'        : 'disguised',
            'isGTypeStructFor' : (self.NS_GLIB, 'is-gtype-struct-for'),
            'version'          : 'version',
            'gTypeName'        : (self.NS_GLIB, 'type-name'),
            'gGetType'         : (self.NS_GLIB, 'get-type'),
            'cSymbolPrefix'    : (self.NS_C, 'symbol-prefix')
        })
        
        self.fields = []
        
        self.parse_doc()
        self.parse_fields()
        
    def parse_fields(self):
        """ Parse the fields <field> nodes """
        from Field import Field
        for field in self.find_children(self.ns(self.NS_CORE, 'field')):
            #todo filter '_gtk_reserved' ??
            self.fields.append(Field(self._namespace, field))

    def getField(self, name):
        """ Get a field by name
        
        Arguments:
            name -- String name
        
        Returns:
            ast.Field instance or None if nothing found
        """
        
        for field in self.fields:
            if field.name == name:
                return field

