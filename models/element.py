from . import fhirabstractbase

class Element(fhirabstractbase.FHIRAbstractBase):
    
    resource_type = "Element"
    
    def __init__(self, jsondict=None, strict=True):
        
        self.extension = None
        """ Additional content defined by implementations.
        List of `Extension` items (represented as `dict` in JSON). """
        
        self.id = None
        """ Unique id for inter-element referencing.
        Type `str`. """
        
        super(Element, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Element, self).elementProperties()
        from . import extension
        js.extend([
            #("extension", "extension", extension.Extension, True, None, False),
            ("id", "id", str, False, None, False),
        ])
        return js