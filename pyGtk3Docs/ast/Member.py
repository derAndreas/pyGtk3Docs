
from Base import Base

class Member(Base):
    """ Member nodes <member> are used in ast.Bitfield and ast.Enumartion
    as defining constants"""
    
    def parse_node(self):
        """ Parse the node """
        self.parse_attributes_from_map({
            'name'        : 'name',
            'value'       : 'value',
            'cidentifier' : (self.NS_C, 'identifier'),
            'gNick'       : (self.NS_GLIB, 'nick')
        })


    def toObjectRepr(self):
        """ Collect all usefull informations and return a Dict
        
        Returns
            Dict
        """
        return {
            'name' : self.getName(),
            'value' : self.value
        }

