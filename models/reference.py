from . import element, identifier

class Reference(element.Element):

    resource_type = "Reference"
    
    def __init__(self, jsondict=None, strict=True):
        
        self.display = None
        self.identifier = None
        self.reference = None
        self.type = None

