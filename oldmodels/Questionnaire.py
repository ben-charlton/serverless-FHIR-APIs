from . import backboneelement, element, coding, contactdetail, fhirdate, reference
class Questionnairee(domainresource.DomainResource):
    
    resource_type = "Questionnaire"
    
    def __init__(self, jsondict=None, strict=True):
        
        self.approvalDate = None
        self.code = None
        self.contact = None
        self.copyright = None
        self.date = None
        self.description = None
        self.identifier = None
        self.item = None
        self.lastReviewDate = None
        self.name = None
        self.publisher = None
        self.purpose = None
        self.status = None
        self.subjectType = None 
        self.title = None
        self.url = None
        self.version = None
        
        super(Questionnaire, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(Questionnaire, self).elementProperties()
        js.extend([
            ("approvalDate", "approvalDate", fhirdate.FHIRDate, False, None, False),
            ("code", "code", coding.Coding, True, None, False),
            ("contact", "contact", contactdetail.ContactDetail, True, None, False),
            ("copyright", "copyright", str, False, None, False),
            ("date", "date", fhirdate.FHIRDate, False, None, False),
            ("description", "description", str, False, None, False),
            ("identifier", "identifier", identifier.Identifier, True, None, False),
            ("item", "item", QuestionnaireItem, True, None, False),
            ("lastReviewDate", "lastReviewDate", fhirdate.FHIRDate, False, None, False),
            ("name", "name", str, False, None, False),
            ("publisher", "publisher", str, False, None, False),
            ("purpose", "purpose", str, False, None, False),
            ("status", "status", str, False, None, True),
            ("subjectType", "subjectType", str, True, None, False),
            ("title", "title", str, False, None, False),
            ("url", "url", str, False, None, False),
            ("version", "version", str, False, None, False),
        ])
        return js

class QuestionnaireItem(element.Element):
    
    resource_type = "QuestionnaireItem"
    
    def __init__(self, jsondict=None, strict=True):
        
        self.answerOption = None
        self.answerValueSet = None
        self.code = None
        self.definition = None
        self.enableBehavior = None
        self.item = None
        self.linkId = None
        self.maxLength = None
        self.prefix = None
        self.readOnly = None
        self.repeats = None
        self.required = None 
        self.text = None
        self.type = None
        
        super(QuestionnaireItem, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(QuestionnaireItem, self).elementProperties()
        js.extend([
            ("answerOption", "answerOption", QuestionnaireItemAnswerOption, True, None, False),
            ("answerValueSet", "answerValueSet", str, False, None, False),
            ("code", "code", coding.Coding, True, None, False),
            ("definition", "definition", str, False, None, False),
            ("enableBehavior", "enableBehavior", str, False, None, False),
            ("item", "item", QuestionnaireItem, True, None, False),
            ("linkId", "linkId", str, False, None, True),
            ("maxLength", "maxLength", int, False, None, False),
            ("prefix", "prefix", str, False, None, False),
            ("readOnly", "readOnly", bool, False, None, False),
            ("repeats", "repeats", bool, False, None, False),
            ("required", "required", bool, False, None, False),
            ("text", "text", str, False, None, False),
            ("type", "type", str, False, None, True),
        ])
        return js

class QuestionnaireItemAnswerOption(element.Element):
    
    resource_type = "QuestionnaireItemAnswerOption"
    
    def __init__(self, jsondict=None, strict=True):

        self.initialSelected = None
        self.valueCoding = None
        self.valueDate = None
        self.valueInteger = None
        self.valueReference = None
        self.valueString = None
        self.valueTime = None
        super(QuestionnaireItemAnswerOption, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(QuestionnaireItemAnswerOption, self).elementProperties()
        js.extend([
            ("initialSelected", "initialSelected", bool, False, None, False),
            ("valueCoding", "valueCoding", coding.Coding, False, "value", True),
            ("valueDate", "valueDate", fhirdate.FHIRDate, False, "value", True),
            ("valueInteger", "valueInteger", int, False, "value", True),
            ("valueReference", "valueReference", reference.Reference, False, "value", True),
            ("valueString", "valueString", str, False, "value", True),
            ("valueTime", "valueTime", fhirdate.FHIRDate, False, "value", True),
        ])
        return js
