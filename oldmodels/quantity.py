from . import element

class Quantity(element.Element):
    
    resource_type = "Quantity"
    
    def __init__(self, jsondict=None, strict=True):
        
        self.code = None
        self.comparator = None
        self.system = None
        self.unit = None
        self.value = None
        
        super(Quantity, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Quantity, self).elementProperties()
        js.extend([
            ("code", "code", str, False, None, False),
            ("comparator", "comparator", str, False, None, False),
            ("system", "system", str, False, None, False),
            ("unit", "unit", str, False, None, False),
            ("value", "value", float, False, None, False),
        ])
        return js