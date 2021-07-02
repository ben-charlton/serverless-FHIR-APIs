from . import element, identifier

class Reference(element.Element):

    resource_type = "Reference"
    
    def __init__(self, jsondict=None, strict=True):
        
        self.display = None
        """ Text alternative for the resource.
        Type `str`. """
        
        self.identifier = None
        """ Logical reference, when literal reference is not known.
        Type `Identifier` (represented as `dict` in JSON). """
        
        self.reference = None
        """ Literal reference, Relative, internal or absolute URL.
        Type `str`. """
        
        self.type = None
        """ Type the reference refers to (e.g. "Patient").
        Type `str`. """
        
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