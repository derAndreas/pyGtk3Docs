
from .. import NS_CORE, NS_C, NS_GLIB

class Base(object):
    """ Base Class all ast.* Nodes should be derived from"""
    NS_CORE = NS_CORE
    NS_C = NS_C
    NS_GLIB = NS_GLIB
    
    def __init__(self, namespace, node):
        """ Init a new Ast element, store the parent global namespace
        instance and etree XML Node and call parse_node(). """
        
        self._namespace = namespace #needed later for type resolvment
        self.node = node
        self.parse_node()
        
    def parse_node(self):
        """ Parse the current Node in the derived AST Object
        Overwrite this method in the concrete implementation """
        raise NotImplementedError('"Ast::%s::parse_node()" not implemented in derived class' % self.__class__.__name__)
        
    def toObjectRepr(self):
        """ Collect all parsed informations and return
        a python object that can be processed later for output 
        Overwrite this method in the concrete implementation """
        raise NotImplementedError('"Ast::%s::toObjectRepr()" not implemented in derived class' % self.__class__.__name__)
    
    def parse_doc(self):
        """ Parse a <doc> node in the ast.* instance if there is any """
        doc = self.node.find(self.ns(self.NS_CORE, 'doc'))
        
        if doc is not None:
            # need to import Doc here, because of nested usage of Base class,
            # which causes infinite import loop
            from Doc import Doc
            self.doc = Doc(self._namespace, doc)
    
    def parse_parameters(self):
        """ Parse <parameters> node and each subnode <parameter> """
        if hasattr(self, 'parameters') is False:
            self.parameters = []
        
        params = self.node.find(self.ns(self.NS_CORE, 'parameters'))
        
        if params is not None:
            from Parameter import Parameter
            for param in self.find_children(self.ns(self.NS_CORE, 'parameter'), params):
                self.parameters.append(Parameter(self._namespace, param))
    
    def parse_attributes_from_map(self, mapping):
        """ Universal method to parse attributed from a node based
        on the given parse map. The mapping is a python Dict that looks like
        
            mapping = {
                'key_to_set_in_ast_instance' : 'name_of_the_xml_attribute'
            }
        
        The key of the mapping Dic will be the property/attribute name of 
        the ast.* instance. If a mapping is {'myCoolVersion' : 'version'} the
        ast instance will have the propertiy self.myCoolVersion
        """
        
        for key, attrib in mapping.iteritems():
            if isinstance(attrib, tuple):
                attrib = self.ns(attrib[0], attrib[1])
            
            self.__dict__[key] = self.node.get(attrib)
            
    def parse_returnvalue(self):
        """ Parse the <return-value> node """
        rValue = self.node.find(self.ns(self.NS_CORE, 'return-value'))
        if rValue is not None:
            # need to import here, because of import loop
            from ReturnValue import ReturnValue
            self.returnValue = ReturnValue(self._namespace, rValue)
            
    def parse_types(self, node):
        """ Method to lookup types used as parameters or return values 
        Lookup the type defined in TypeDef.py and return the Type* instance
        that represents it 
        
        Parameters:
            node -- etree XML node to get and parse the type for
        
        Returns
            Returns an instance of ast.Type* based on the type that the 
            input node describes
        
        """
        if node is None:
            return node
            
        from Type import Type
        from TypeArray import TypeArray
        from TypeVarArg import TypeVarArg
    
        typenode = node.find(self.ns(self.NS_CORE, 'type'))

        if typenode is not None:
            return Type(self._namespace, typenode)
        
        arraynode = node.find(self.ns(self.NS_CORE, 'array'))
        
        if arraynode is not None:
            return TypeArray(self._namespace, arraynode)
        
        varnode = node.find(self.ns(self.NS_CORE, 'varargs'))
        
        if varnode is not None:
            return TypeVarArg(self._namespace, varnode)
        

    def ns(self, ns, tag):
        """ Universal function to generate NS string for XML usage
        
            Arguments:
            ns  -- The namespace string
            tag -- The tag name 
            
            Returns:
            The namespace string as "{%ns}%tag"
        """
        return "{%s}%s" % (ns, tag)
        
    def find_children(self, tag, node=None):
        """ Find direct children of the input etree node or 
        the self.node etree object and return all children that
        match the tag name
        
        Arguments:
            tag  -- Name of the tag to find as direct child (string)
            node -- an etree() node, if not present it will use self.node
        
        Returns:
            An array of etree node objects
        """
        
        if node is None:
            node = self.node
            
        return [c for c in node.getchildren() if c.tag == tag]


    def getNamepspaceTag(self):
        """ Return the global main ast.Namespace.Namespace Object
        
        Returns
            Instance of ast.Namespace.Namespace
        """
        return self._namespace
        
    def getName(self):
        """ Return the value of self.name which should 
        be set in every ast instance
        
        Returns:
            String
        """
        assert self.name
        return self.name
        
    def getVersion(self):
        """ Return the self.version value if present
        If not present, return an empty string
        
        Returns:
            String
        """
        if self.version is None:
            return ''
        return self.version
        
    def getType(self):
        """ Return ast.Type* instance, if there is any type object
        This will only availbe in Parameters, returnValue (etc) instances
        where a <type> node exists
        
        Returns
            None or ast.Type* instance
        """
        return self.type
    
    def getCType(self):
        """ Return the Ctype, which is the attribute "c:type" from the XML node
        
        Returns
            None or String
        """
        if hasattr(self, 'ctype'):
            return self.ctype
        return None
    
    def getDoc(self, asObjectRepr=False):
        """ Get the <doc> ast.Doc instance for this ast instance if there is any
        If called with Argument asObjectRepr=True it will directly call
        toObjectRepr() on the ast.Doc instance. 
        
        Arguments:
            asObjectRepr -- true if directly call toObjectRepr() on ast.Doc instance (default False)
        
        Returns
            String or ast.Doc instance
        """
        if hasattr(self, 'doc'):
            if asObjectRepr is True:
                return self.doc.toObjectRepr()
            else:
                return self.doc
        
        return ''
        
    def getParentTree(self, result=None):
        """Get the Parent Tree for the current node if possible.
        Maybe only available for <class> nodes and derived ast.Klass implementations
        
        Returns:
            None or an sorted array with parents
        """
        if self._parent is None:
            return None
            
        if result is None:
            result = [self.name]
        else:
            result.append(self.name)
        
        if isinstance(self._parent, Base):
            self._parent.getParentTree(result)
        elif isinstance(self._parent, str):
            result.append(self._parent)
        else:
            raise ValueException('Unknown Type found in getParentTree()')
        
        return result

