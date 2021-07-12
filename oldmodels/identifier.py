from . import element, reference, codeableconcept

class Identifier(element.Element):
    
    resource_type = "Identifier"
    
    def __init__(self, jsondict=None, strict=True):

        self.assigner = None
        self.period = None
        self.system = None
        self.type = None
        self.use = None
        self.value = None
        
        super(Identifier, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Identifier, self).elementProperties()
        js.extend([
            ("assigner", "assigner", reference.Reference, False, None, False),
            ("period", "period", period.Period, False, None, False),
            ("system", "system", str, False, None, False),
            ("type", "type", codeableconcept.CodeableConcept, False, None, False),
            ("use", "use", str, False, None, False),
            ("value", "value", str, False, None, False),
        ])
        return js