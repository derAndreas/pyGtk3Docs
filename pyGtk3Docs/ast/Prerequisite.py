

from Base import Base


class Prerequisite(Base):
    """ Prerequisite nodes <prerequisite> are used in interfaces
    are requirements to use an interface.
    """
    
    def parse_node(self):
        """ Parse the node"""
        self.parse_attributes_from_map({
            'name'          : 'name'
        })
