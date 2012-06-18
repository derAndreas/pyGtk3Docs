

class BaseFormat(object):
    """ Base Class for output formatter"""
    
    def __init__(self, converter):
        assert converter.getNamespaceTag()
        self.converter = converter
        
        self.walk()
   
    def walk(self):
        """ Walk the ast tree, implement this in the derived formatter"""
        raise NotImplementedError('"%s.walk()" not implemented in formatter' % self.__class__.__name__)
    
    def write(self):
        """ Method to write the data to files, override it if needed"""
        raise NotImplementedError('"%s.write()" not implemented in formatter' % self.__class__.__name__)
