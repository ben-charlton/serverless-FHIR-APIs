from . import fhirabstractresource, meta

class Resource(fhirabstractresource.FHIRAbstractResource):
    
    resource_type = "Resource"
    
    def __init__(self, jsondict=None, strict=True):

        self.id = None
        self.implicitRules = None
        self.language = None
        self.meta = None

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