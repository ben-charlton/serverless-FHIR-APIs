from . import element

class Quantity(element.Element):
    
    resource_type = "Quantity"
    
    def __init__(self, jsondict=None, strict=True):
        
        self.code = None
        """ Coded form of the unit.
        Type `str`. """
        
        self.comparator = None
        """ < | <= | >= | > - how to understand the value.
        Type `str`. """
        
        self.system = None
        """ System that defines coded unit form.
        Type `str`. """
        
        self.unit = None
        """ Unit representation.
        Type `str`. """
        
        self.value = None
        """ Numerical value (with implicit precision).
        Type `float`. """
        
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