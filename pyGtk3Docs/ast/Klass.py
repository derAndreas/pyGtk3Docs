
from Base import Base

class Klass(Base):
    """ Class represents a <class> Node from the GIR XML File """
    
    def parse_node(self):
        """ Parse the node and fetch any information that can be useful.
            That means, that Nodes like <field> are also parsed, even though
            they are not directly used in the output, but can be important for
            internal references or lookups """
        
        self.parse_attributes_from_map({
            'name'          : 'name',
            'parent'        : 'parent',
            'abstract'      : 'abstract',
            'symbol_prefix' : (self.NS_C, 'symbol-prefix'),
            'ctype'         : (self.NS_C, 'type'),
            'gtype_name'    : (self.NS_GLIB, 'type-name'),
            'gtype_struct'  : (self.NS_GLIB, 'type-struct'),
            'gGetType'      : (self.NS_GLIB, 'get-type')
        })
        
        
        self.interfaces = []
        self.constructors = []
        self.virtualmethods = []
        self.methods = []
        self.properties = []
        self.signals = []
        self.fields = []
        self.functions = []
        
        self.parse_doc()
        self.parse_implements()
        self.parse_constructors()
        self.parse_virtualmethods()
        self.parse_methods()
        self.parse_properties()
        self.parse_signals()
        self.parse_fields()
        self.parse_functions()
        
        
        # propagate the created klass type to the namespace
        self._namespace.registerType(self, self.getName(), self.getCType())


    def parse_implements(self):
        """ Parse the <implements> nodes in the <class> node
        Does not create ast.* objects, as the <implements> nodes are
        just strings with no additional informations that need to be
        stored as it's own object"""
        for iface in self.find_children(self.ns(self.NS_CORE, 'implements')):
            self.interfaces.append(iface.get('name').split(","))

    def parse_constructors(self):
        """ Parse Class constructors
        There can be many Constructors in <class> nodes to document all
        variations in C to instantiate a new object. For each of this
        variant create a new ast.Constructor instance """
        
        from Constructor import Constructor
        for ctor in self.find_children(self.ns(self.NS_CORE, 'constructor')):
            self.constructors.append(Constructor(self._namespace, ctor))

    def parse_virtualmethods(self):
        """ Parse <virtual-method> nodes
        Inherited virtual method from C, but should be later documented
        as a normal method in python. Merge virtual- and normal methods later
        """
        
        from VirtualMethod import VirtualMethod
        for vmeth in self.find_children(self.ns(self.NS_CORE, 'virtual-method')):
            self.virtualmethods.append(VirtualMethod(self._namespace, vmeth))

    def parse_methods(self):
        """ Parse <method> Nodes """
        from Method import Method
        for meth in self.find_children(self.ns(self.NS_CORE, 'method')):
            self.methods.append(Method(self._namespace, meth))
            
    def parse_properties(self):
        """ Parse Class properties """
        from Property import Property
        for prop in self.find_children(self.ns(self.NS_CORE, 'property')):
            self.properties.append(Property(self._namespace, prop))

    def parse_fields(self):
        """ Parse <field> nodes which can contain usefull informations 
        like parent_instance"""
        
        from Field import Field
        for field in self.find_children(self.ns(self.NS_CORE, 'field')):
            self.fields.append(Field(self._namespace, field))

    def parse_signals(self):
        """ Parse <signal> nodes that can be emitted and listen on """
        from Signal import Signal
        for sig in self.find_children(self.ns(self.NS_GLIB, 'signal')):
            self.signals.append(Signal(self._namespace, sig))

    def parse_functions(self):
        """ Parse <function> node """
        from Function import Function
        for func in self.find_children(self.ns(self.NS_GLIB, 'function')):
            self.functions.append(Function(self._namespace, func))


    def toObjectRepr(self):
        """ Collect all parsed informations and return
        a python object that can be processed later for output 
        
        Returns    
            Dict of all informations that is needed in output
        """
        # collect the interfaces from the "<implements>" tag
        ifaceObjs = []
        for iface in self.interfaces:
            if type(iface) == list:
                for ifacelist in iface:
                    ifaceObjs.append([ifacelist])
            elif iface.find('.') > -1:
                ifaceObjs.append([iface])
            else:
                #TODO ifaces seem not to inherit from parent, only from 
                #     "GObject.TypeInterface", validate this
                ifaceObj = self._namespace.findInterfaceInstance(iface)
                ifaceRecord = self._namespace.findRecordInstance(ifaceObj.gtype_struct)
                if ifaceRecord is not None:
                    if ifaceRecord.getField('g_iface') is not None:
                        field = ifaceRecord.getField('g_iface')
                    elif ifaceRecord.getField('base_iface') is not None:
                        field = ifaceRecord.getField('base_iface')
                    elif ifaceRecord.getField('base_interface') is not None:
                        field = ifaceRecord.getField('base_interface')
                    else:
                        print "Iface unknown", ifaceRecord.name
                    ifaceObjs.append([iface, field.getType().getName()])


        # reformat abstract attribute and use it as isAbstract
        if self.abstract is not None:
            self.abstract = True
        else:
            self.abstract = False

        # collect all methods: constructor, method
        methods = []
        # constructors format, change it a bit and later add it to "methods"
        for ctor in self.constructors:
            ctorObj = ctor.toObjectRepr(self.name)
            methods.append(ctorObj)

        for meth in self.methods:
            methObj = meth.toObjectRepr()
            methods.append(methObj)

        # for now, virtual-methods are just methods
        for vmeth in self.virtualmethods:
            methObj = vmeth.toObjectRepr()
            methods.append(methObj)
            
        #TODO functions are not within classes and interfaces??


        # handle properties
        properties = []

        for prop in self.properties:
            properties.append(prop.toObjectRepr())

        # signals...
        signals = []
        for signal in self.signals:
            signals.append(signal.toObjectRepr())

        return {
            'name' : self.getName(),
            'fullname' : "Class %s.%s" % (self._namespace.getName(), self.getName()),
            'description' : self.getDoc(True),
            'parents' : self.getParentTree(),
            'isAbstract' : self.abstract,
            'interfaces' : ifaceObjs,
            'members' : {
                'methods' : methods,
                'properties' : properties,
                'signals' : signals
            }
        }

