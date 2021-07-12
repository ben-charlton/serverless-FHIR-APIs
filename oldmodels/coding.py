from . import element

class Coding(element.Element):
    
    resource_type = "Coding"
    
    def __init__(self, jsondict=None, strict=True):
        
        self.code = None
        self.display = None
        self.system = None
        self.userSelected = None
        self.version = None
        
        super(Coding, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Coding, self).elementProperties()
        js.extend([
            ("code", "code", str, False, None, False),
            ("display", "display", str, False, None, False),
            ("system", "system", str, False, None, False),
            ("userSelected", "userSelected", bool, False, None, False),
            ("version", "version", str, False, None, False),
        ])
        return js
