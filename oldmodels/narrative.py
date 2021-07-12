from . import element

class Narrative(element.Element):
    
    resource_type = "Narrative"
    
    def __init__(self, jsondict=None, strict=True):
        
        self.div = None
        self.status = None

        super(Narrative, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Narrative, self).elementProperties()
        js.extend([
            ("div", "div", str, False, None, True),
            ("status", "status", str, False, None, True),
        ])
        return js