from . import element

class CodeableConcept(element.Element):

    resource_type = "CodeableConcept"
    
    def __init__(self, jsondict=None, strict=True):
        
        self.coding = None
        self.text = None
        
        super(CodeableConcept, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(CodeableConcept, self).elementProperties()
        js.extend([
            ("coding", "coding", coding.Coding, True, None, False),
            ("text", "text", str, False, None, False),
        ])
        return js