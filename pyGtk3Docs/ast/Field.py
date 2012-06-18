
from Base import Base

class Field(Base):    
    """ Fields nodes <field> contain informations about classes
    like parent_instances that can be used to create the parent tree and
    the inheritance
    """
    
    def parse_node(self):
        """ Parse the node"""
        self.parse_attributes_from_map({
            'name'     : 'name',
            'readable' : 'readable',
            'private'  : 'private',
            'bits'     : 'bits'
        })
        
        self.callbacks = []
        
        self.parse_callbacks()
        self.type = self.parse_types(self.node)
        
        #todo <field> tags does not seem to populate own types, rather
        #     then map from parameter keys to types
        #     check if we iterate over the fields everytime or collect them
        #     in the record tag, because fields are bound to records and not
        #     globally uniqe

    def parse_callbacks(self):
        """ Field nodes can have callback subnodes, parse them here """
        from Callback import Callback
        for cb in self.find_children(self.ns(self.NS_CORE, 'callback')):
            self.callbacks.append(Callback(self._namespace, cb))

