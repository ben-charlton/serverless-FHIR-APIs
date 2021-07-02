from . import fhirabstractresource

class Resource(fhirabstractresource.FHIRAbstractResource):
    
    resource_type = "Resource"
    
    def __init__(self, jsondict=None, strict=True):

        self.id = None
        """ Logical id of this artifact.
        Type `str`. """
        
        self.implicitRules = None
        """ A set of rules under which this content was created.
        Type `str`. """
        
        self.language = None
        """ Language of the resource content.
        Type `str`. """
        
        self.meta = None
        """ Metadata about the resource.
        Type `Meta` (represented as `dict` in JSON). """
        
        super(Resource, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Resource, self).elementProperties()
        js.extend([
            ("id", "id", str, False, None, False),
            ("implicitRules", "implicitRules", str, False, None, False),
            ("language", "language", str, False, None, False),
            ("meta", "meta", meta.Meta, False, None, False),
        ])
        return js