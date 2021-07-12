from . import element, identifier

class Reference(element.Element):

    resource_type = "Reference"
    
    def __init__(self, jsondict=None, strict=True):
        
        self.display = None
        self.identifier = None
        self.reference = None
        self.type = None

        super(Reference, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Reference, self).elementProperties()
        js.extend([
            ("display", "display", str, False, None, False),
            ("identifier", "identifier", identifier.Identifier, False, None, False),
            ("reference", "reference", str, False, None, False),
            ("type", "type", str, False, None, False),
        ])
        return js