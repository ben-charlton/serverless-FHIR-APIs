from . import resource, narrative

class DomainResource(resource.Resource):
    
    resource_type = "DomainResource"
    
    def __init__(self, jsondict=None, strict=True):

        self.contained = None
        """ Contained, inline Resources.
        List of `Resource` items (represented as `dict` in JSON). """
        
        self.extension = None
        """ Additional content defined by implementations.
        List of `Extension` items (represented as `dict` in JSON). """
        
        self.modifierExtension = None
        """ Extensions that cannot be ignored.
        List of `Extension` items (represented as `dict` in JSON). """
        
        self.text = None
        """ Text summary of the resource, for human interpretation.
        Type `Narrative` (represented as `dict` in JSON). """
        
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