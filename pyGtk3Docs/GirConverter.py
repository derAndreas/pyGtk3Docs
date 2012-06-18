#!/usr/bin/env python

import warnings

from lxml import etree
from . import NS_CORE, NS_C, NS_GLIB

from ast.Namespace import Namespace
from ast.Alias import Alias
from ast.Klass import Klass
from ast.Record import Record
from ast.Bitfield import Bitfield
from ast.Enumeration import Enumeration
from ast.Function import Function
from ast.Callback import Callback
from ast.Iface import Iface
from ast.Constant import Constant

class GirConverter(object):
    """ The converter to convert the GIR XML File """
    
    astMap = {
        'alias' : Alias,
        'bitfield' : Bitfield,
        'callback' : Callback,
        'class' : Klass,
        'constant' : Constant,
        'enumeration' : Enumeration,
        'interface' : Iface,
        'function' : Function,
        'record' : Record
    }
    
    def __init__(self, source, dest):
        self.root = etree.parse(source).getroot()
        self.dst_file = dest
        
        assert self.root.tag == self.create_ns(NS_CORE, 'repository')
        

    def parse(self):
        """ Parse the GIR XML File"""
        namespace = self.root.find(self.create_ns(NS_CORE, 'namespace'))
        assert namespace is not None
        self._namespace = Namespace(None, namespace)
        
        # parse through the XML hierachy and collect all data from subnodes
        for cnode in namespace.getchildren():
            tag = self.strip_ns(NS_CORE, cnode.tag)
            inst = self.astMap.get(tag)
            
            if inst is not None:
                self._namespace.append(tag, inst(self._namespace, cnode))
            else:
                warnings.warn('Missed node type "%s" in namespace tag' % tag, UserWarning)
        
        
        # resolve any inner cross references between the objects
        # perform this after all subnodes have been parsed
        self.create_references()
    
    def create_ns(self, ns, tag):
        """ Universal function to generate NS string for XML usage
        
            Arguments:
            ns  -- The namespace string
            tag -- The tag name 
            
            Returns:
            The namespace string as "{%ns}%tag"
        """
        return "{%s}%s" % (ns, tag)
    
    def strip_ns(self, ns, tag):
        """ Universal method to remove the Namespace from
            a XML Tag and return the plain XML Tag 
            
            Arguments
                ns  -- the Namespace string to remove
                tag -- the tag string name
            
            Returns:
                String
        """
        ns = "{%s}" % ns
        return tag.replace(ns, '')
    
    def getNamespaceTag(self):
        """ Return the Main Namespace Instance
        
            Returns:
                Namespace Instance of ast.Namespace.Namespace
        """
        return self._namespace
    
    
    def create_references(self):
        """ Create References between Gtk Objects or parameter dependencies
            
            Rules:
                1. Namespace does not have any dependencies on sub objects
                2. Alias do not have any dependencies
                3. Bitfield none
                4. Callback none
                5. Class need to be checked to references
                5.1 Check "parent" attribute
                5.1.1 Lookup value in namespace types or use the plain value if nothing found
                #TODO? 5.2 Check Record Tag for this Class and search for field "parent_class"
                #TODO? 5.2.1 Lookup value in namespace types or use the plain value if nothing found
                6. Constant None
                7. Enumeration None
                8. Interface need to be checked
                8.1 Check interfaces for prerequisutes
                8.1.1 check the value of prerequisite tag in namespace types
                8.2 Check Record Tag for this Interface and search for field "g_iface"
                8.2.1 Use the value of g_iface field
                9. Function none
                10. Record should only be used by class and iface tags and not used directly
        """
        
        for cls in self._namespace.classes:
            if cls.parent.find(".") > -1:
                cls._parent = cls.parent
                continue
            
            parentObj = self._namespace.findRegisteredType(cls.parent)
            
            if parentObj is not None:
                cls._parent = parentObj
            
            
