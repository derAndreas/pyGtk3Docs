
class TypeDef(object):
    """ Type Definition for mapping C types and Python types """
    def __init__(self, ctype, ptype):
        """ Create a new TypeDefinition
        
        Arguments:
            ctype -- the C Type as a String
            ptype -- the Phython Type as a String
        """
        self.ctype = ctype
        self.ptype = ptype
        
    def __cmp__(self, typ):
        """ Compare the input type to the C any Python type
            and return the result
            
            Arguments:
                typ -- The string value to compare
            
            Returns:
                The compare result as an Integer
        """
        result = cmp(self.ctype, typ)
        if result != 0:
            typ = typ.replace('*', '')
            result = cmp(self.ctype, typ)
        return result
    
    def getPython(self):
        return self.ptype

""" List of instantiated types to be used in the software"""

TYPE_NONE = TypeDef('none', 'None')
TYPE_VOID = TypeDef('void', 'void')
TYPE_ANY = TypeDef('gpointer', 'Mixed')

TYPE_BOOLEAN = TypeDef('gboolean', 'Boolean')
TYPE_FLOAT   = TypeDef('gfloat', 'Float')
TYPE_GDOUBLE = TypeDef('gdouble', 'Float')
TYPE_DOUBLE  = TypeDef('double', 'Float')
TYPE_INT     = TypeDef('gint', 'Integer')
TYPE_INT_2   = TypeDef('int', 'Integer')
TYPE_UINT    = TypeDef('guint', 'Integer')
TYPE_UINT8   = TypeDef('guint8', 'Integer')
TYPE_UINT16  = TypeDef('guint16', 'Integer')
TYPE_UINT32  = TypeDef('guint32', 'Integer')
TYPE_LONG    = TypeDef('glong', 'Integer')
TYPE_GSIZE   = TypeDef('gsize', 'Integer')
TYPE_GSSIZE  = TypeDef('gssize', 'Integer')
TYPE_GTYPE   = TypeDef('GType', 'Integer')# A numerical value which represents the unique identifier of a registered type. 


TYPE_STRING_1= TypeDef('gchar', 'String')
TYPE_STRING_2= TypeDef('char*', 'String')
TYPE_STRING_3= TypeDef('gchar*', 'String')
TYPE_STRING_4= TypeDef('utf8', 'String')
TYPE_STRING_5= TypeDef('gunichar', 'String') # would be better to use Unicode, but Unicode is subclass of str
TYPE_STRING_6= TypeDef('filename', 'String')

TYPE_VALIST  = TypeDef('va_list', 'Mixed')

BASIC_TYPES = [ 
    TYPE_NONE, TYPE_VOID, TYPE_ANY, TYPE_BOOLEAN, 
    TYPE_FLOAT, TYPE_GDOUBLE, TYPE_DOUBLE,
    TYPE_INT, TYPE_INT_2, TYPE_UINT, TYPE_UINT8, TYPE_UINT16, TYPE_UINT32, 
    TYPE_LONG, TYPE_GSIZE, TYPE_GSSIZE, TYPE_GTYPE,
    TYPE_STRING_1, TYPE_STRING_2, TYPE_STRING_3, TYPE_STRING_4, TYPE_STRING_5, TYPE_STRING_6,
    TYPE_VALIST
]
