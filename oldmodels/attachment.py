from . import element, fhirdate

class Attachment(element.Element):

    resource_type = "Attachment"
    
    def __init__(self, jsondict=None, strict=True):
        self.contentType = None
        self.creation = None
        self.data = None
        self.hash = None
        self.language = None
        self.size = None  
        self.title = None
        self.url = None
        
        super(Attachment, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Attachment, self).elementProperties()
        js.extend([
            ("contentType", "contentType", str, False, None, False),
            ("creation", "creation", fhirdate.FHIRDate, False, None, False),
            ("data", "data", str, False, None, False),
            ("hash", "hash", str, False, None, False),
            ("language", "language", str, False, None, False),
            ("size", "size", int, False, None, False),
            ("title", "title", str, False, None, False),
            ("url", "url", str, False, None, False),
        ])
        return js