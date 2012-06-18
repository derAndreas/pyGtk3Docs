
from .Json import Json as JsonFormat
import json
import os.path

class JsonExtTree(JsonFormat):
    """Special JSON Formatter, for EXT2.1 TreePanel """
    
    def write(self, dest):
        if os.path.exists(dest) is True:
            self.getResult() # just call it to have updated self.result variable
            
            if dest[-1] == '/':
                dest = dest[:-1]
            
            treeChildren = []
            treeFile = "%s/tree.json" % dest
            
            for structures in self.result['children']:
                structChildren = []
                for el in structures['children']:
                    structChildren.append({
                        'id' : self.getId(el['text']),
                        'text' : el['text'],
                        'leaf' : True
                    })
                    
                    fhandle = open("%s/Doc-Gtk.%s.json" % (dest, el['name']), 'w')
                    fhandle.write(json.dumps(el, indent=4))
                    fhandle.close()
                    
                treeChildren.append({
                    'id' : self.getId(structures['text']),
                    'text' : structures['text'],
                    'leaf' : False,
                    'children': structChildren
                })

            
            tree = {
                'id' : self.getId(self.result['name']),
                'text' : self.result['name'],
                'leaf' : False,
                'children' : treeChildren
            }
            
            fhandle = open(treeFile, 'w')
            fhandle.write("[%s]" % json.dumps(tree, indent=4))
            fhandle.close()
            
        else:
            raise Exception('Ouput destination "%s" is not a valid, existing folder' % dest)
    
    def getResult(self):
        ns_children = []
        for key, member in self.result['members'].iteritems():
            childs = []
            
            for el in member:
                
                el['text'] = el['name']
                el['id'] = self.getId(el['name'])
                el['leaf'] = True
                
                childs.append(el)
            
            ns_children.append({
                'text' : key.title(),
                'children' : childs,
                'leaf' : False
            })
                
        self.result['leaf'] = False
        self.result['children'] = ns_children
        self.result['id'] = self.getId(self.result['name'])
        self.result['text'] = self.result['name']
        
        del self.result['members']
        
        return "[%s]" % json.dumps(self.result, indent=4)
    
    def getId(self, name):
        return "Docs-%s" % name
