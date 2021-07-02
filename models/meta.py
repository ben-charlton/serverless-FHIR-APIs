from . import element, coding, fhirdate

class Meta(element.Element):
    
    resource_type = "Meta"
    
    def __init__(self, jsondict=None, strict=True):
        
        self.lastUpdated = None
        """ When the resource version last changed.
        Type `FHIRDate` (represented as `str` in JSON). """
        
        self.profile = None
        """ Profiles this resource claims to conform to.
        List of `str` items. """
        
        self.security = None
        """ Security Labels applied to this resource.
        List of `Coding` items (represented as `dict` in JSON). """
        
        self.source = None
        """ Identifies where the resource comes from.
        Type `str`. """
        
        self.tag = None
        """ Tags applied to this resource.
        List of `Coding` items (represented as `dict` in JSON). """
        
        self.versionId = None
        """ Version specific identifier.
        Type `str`. """
        
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
