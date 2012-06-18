
from Klass import Klass

class Iface(Klass):
    """ Interfaces <interface> nodes """
    
    def parse_node(self):
        """ parse the node with the ast.Klass base class, as they have
        the same signature . Interface nodes also have subnodes called 'prerequisite'
        """
        
        Klass.parse_node(self)
        
        self.prerequisites = []
        self.parse_prerequisite()
        
        # propagate the interface type to the namespace
        self._namespace.registerType(self, self.getName(), self.getCType())


    def parse_prerequisite(self):
        """ Parse the prerequisite subnodes from interface nodes"""
        from Prerequisite import Prerequisite
        for preq in self.find_children(self.ns(self.NS_CORE, 'prerequisite')):
            self.prerequisites.append(Prerequisite(self._namespace, preq))

