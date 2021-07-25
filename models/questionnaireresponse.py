from . import element, quantity, coding, fhirdate, reference, attachment, domainresource

class QuestionnaireResponse(domainresource.DomainResource):

    resource_type = "QuestionnaireResponse"
    
    def __init__(self, jsondict=None, strict=True):

        self.author = None
        self.authored = None
        self.basedOn = None
        self.encounter = None
        self.identifier = None
        self.item = None
        self.partOf = None
        self.questionnaire = None
        self.source = None
        self.status = None
        self.subject = None

        super(QuestionnaireResponse, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(QuestionnaireResponse, self).elementProperties()
        js.extend([
            ("author", "author", reference.Reference, False, None, False),
            ("authored", "authored", fhirdate.FHIRDate, False, None, False),
            ("basedOn", "basedOn", reference.Reference, True, None, False),
            ("encounter", "encounter", reference.Reference, False, None, False),
            ("identifier", "identifier", identifier.Identifier, False, None, False),
            ("item", "item", QuestionnaireResponseItem, True, None, False),
            ("partOf", "partOf", reference.Reference, True, None, False),
            ("questionnaire", "questionnaire", str, False, None, False),
            ("source", "source", reference.Reference, False, None, False),
            ("status", "status", str, False, None, True),
            ("subject", "subject", reference.Reference, False, None, False),
        ])
        return js

class QuestionnaireResponseItem(element.Element):
    
    resource_type = "QuestionnaireResponseItem"
    
    def __init__(self, jsondict=None, strict=True):
        self.answer = None
        self.definition = None
        self.item = None
        self.linkId = None
        self.text = None

        super(QuestionnaireResponseItem, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(QuestionnaireResponseItem, self).elementProperties()
        js.extend([
            ("answer", "answer", QuestionnaireResponseItemAnswer, True, None, False),
            ("definition", "definition", str, False, None, False),
            ("item", "item", QuestionnaireResponseItem, True, None, False),
            ("linkId", "linkId", str, False, None, True),
            ("text", "text", str, False, None, False),
        ])
        return js

class QuestionnaireResponseItemAnswer(element.Element):

    resource_type = "QuestionnaireResponseItemAnswer"
    
    def __init__(self, jsondict=None, strict=True):
        
        self.item = None
        self.valueAttachment = None
        self.valueBoolean = None
        self.valueCoding = None
        self.valueDate = None
        self.valueDateTime = None
        self.valueDecimal = None
        self.valueInteger = None
        self.valueQuantity = None
        self.valueReference = None
        self.valueString = None
        self.valueTime = None
        self.valueUri = None
        