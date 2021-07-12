from . import resource, narrative

class DomainResource(resource.Resource):
    
    resource_type = "DomainResource"
    
    def __init__(self, jsondict=None, strict=True):

        self.contained = None
        self.extension = None
        self.modifierExtension = None
        self.text = None
        
        super(DomainResource, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(DomainResource, self).elementProperties()
        js.extend([
            ("contained", "contained", resource.Resource, True, None, False),
            #("extension", "extension", extension.Extension, True, None, False),
            #("modifierExtension", "modifierExtension", extension.Extension, True, None, False),
            ("text", "text", narrative.Narrative, False, None, False),
        ])
        return js