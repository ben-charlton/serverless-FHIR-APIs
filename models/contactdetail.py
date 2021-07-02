from . import element

class ContactDetail(element.Element):
    
    resource_type = "ContactDetail"
    
    def __init__(self, jsondict=None, strict=True):
        
        self.name = None
        """ Name of an individual to contact.
        Type `str`. """
        
        self.telecom = None
        """ Contact details for individual or organization.
        List of `ContactPoint` items (represented as `dict` in JSON). """
        
        super(ContactDetail, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(ContactDetail, self).elementProperties()
        js.extend([
            ("name", "name", str, False, None, False),
            #("telecom", "telecom", contactpoint.ContactPoint, True, None, False),
        ])
        return js
