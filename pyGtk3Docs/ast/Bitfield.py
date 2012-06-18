

from Base import Base

class Bitfield(Base):
    """ Bitfields contain integer based flags as sub <member> nodes"""
    
    def parse_node(self):
        self.parse_attributes_from_map({
            'name'             : 'name',
            'ctype'            : (self.NS_C, 'type'),
            'version'          : 'version',
            'gTypeName'        : (self.NS_GLIB, 'type-name'),
            'gGetType'         : (self.NS_GLIB, 'get-type')
        })
        
        self.members = []
        self.parse_members()
        
        # propagate the created Bitfield type to the namespace
        self._namespace.registerType(self, self.getName(), self.getCType())
    
    
    def parse_members(self):
        """ Parse the members or the bitfield enumeration """
        from Member import Member
        for member in self.find_children(self.ns(self.NS_CORE, 'member')):
            self.members.append(Member(self._namespace, member))

    def toObjectRepr(self):
        """ Return the Bitfield as an object representation for output usage"""
        return {
            'name' : self.getName(),
            'fullname' : "%s %s.%s" % (self.__class__.__name__, self._namespace.getName(), self.getName()),
            'description' : self.getDoc(True),
            'version' : self.version,
            'members' : {
                'properties' : [mem.toObjectRepr() for mem in self.members]
            }
                
        }

