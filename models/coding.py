from . import element

class Coding(element.Element):
    
    resource_type = "Coding"
    
    def __init__(self, jsondict=None, strict=True):
        
        self.code = None
        """ Symbol in syntax defined by the system.
        Type `str`. """
        
        self.display = None
        """ Representation defined by the system.
        Type `str`. """
        
        self.system = None
        """ Identity of the terminology system.
        Type `str`. """
        
        self.userSelected = None
        """ If this coding was chosen directly by the user.
        Type `bool`. """
        
        self.version = None
        """ Version of the system - if relevant.
        Type `str`. """
        
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
