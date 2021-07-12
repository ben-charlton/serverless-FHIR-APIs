from . import element, coding, fhirdate

class Meta(element.Element):
    
    resource_type = "Meta"
    
    def __init__(self, jsondict=None, strict=True):
        
        self.lastUpdated = None
        self.profile = None
        self.security = None
        self.source = None
        self.tag = None
        self.versionId = None
        
        super(Meta, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Meta, self).elementProperties()
        js.extend([
            ("lastUpdated", "lastUpdated", fhirdate.FHIRDate, False, None, False),
            ("profile", "profile", str, True, None, False),
            ("security", "security", coding.Coding, True, None, False),
            ("source", "source", str, False, None, False),
            ("tag", "tag", coding.Coding, True, None, False),
            ("versionId", "versionId", str, False, None, False),
        ])
        return js
