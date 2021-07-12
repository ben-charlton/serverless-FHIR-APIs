import sys
class Element(object):
    
    resource_type = "Element"
    
    def __init__(self, jsondict=None, strict=True):
        
        self.extension = None
        self.id = None
    
    def elementProperties(self):
       return []
    
    # Instantiation from JSON
    @classmethod
    def with_json(cls, jsonobj):
        """ Initialize an element from a JSON dictionary or array."""
        
        if isinstance(jsonobj, dict):
            return cls._with_json_dict(jsonobj)
        
        if isinstance(jsonobj, list):
            arr = []
            for jsondict in jsonobj:
                try:
                    arr.append(cls._with_json_dict(jsondict))
                except TypeError as e:
                    raise e
            return arr
        
        raise TypeError("`with_json()` on {} only takes dict or list of dict, but you provided {}"
            .format(cls, type(jsonobj)))


    @classmethod
    def _with_json_dict(cls, jsondict):
        """ Internal method to instantiate from JSON dictionary."""

        if not isinstance(jsondict, dict):
            raise TypeError("Can only use `_with_json_dict()` on {} with a dictionary, got {}"
                .format(type(self), type(jsondict)))
        return cls(jsondict)
    
    
    # (De)Serialization
    def elementProperties(self):
        """ Returns a list of tuples, one tuple for each property that should
        be serialized, as: ("name", "json_name", type, is_list, "of_many", not_optional)
        """
        return []
    
    def update_with_json(self, jsondict):
        """ Update the receiver with data in a JSON dictionary. """
        if jsondict is None:
            return
        
        if not isinstance(jsondict, dict):
            raise TypeError("Non-dict type {} fed to `update_with_json` on {}"
                .format(type(jsondict), type(self)))
        
        # loop all registered properties and instantiate
        errs = []
        valid = set(['resourceType'])   # used to also contain `fhir_comments` until STU-3
        found = set()
        nonoptionals = set()
        for name, jsname, typ, is_list, of_many, not_optional in self.elementProperties():
            valid.add(jsname)
            if of_many is not None:
                valid.add(of_many)
            
            # bring the value in shape
            err = None
            value = jsondict.get(jsname)
            if value is not None and hasattr(typ, 'with_json_and_owner'):
                try:
                    value = typ.with_json_and_owner(value, self)
                except Exception as e:
                    value = None
                    err = e
            
            # got a value, test if it is of required type and assign
            if value is not None:
                testval = value
                if is_list:
                    if not isinstance(value, list):
                        err = TypeError("Wrong type {} for list property \"{}\" on {}, expecting a list of {}"
                            .format(type(value), name, type(self), typ))
                        testval = None
                    else:
                        testval = value[0] if value and len(value) > 0 else None
                
                if testval is not None and not self._matches_type(testval, typ):
                    err = TypeError("Wrong type {} for property \"{}\" on {}, expecting {}"
                        .format(type(testval), name, type(self), typ))
                else:
                    setattr(self, name, value)
                
                found.add(jsname)
                if of_many is not None:
                    found.add(of_many)
            
            # not optional and missing, report (we clean `of_many` later on)
            elif not_optional:
                nonoptionals.add(of_many or jsname)
            
            # TODO: look at `_name` only if this is a primitive!
            _jsname = '_'+jsname
            _value = jsondict.get(_jsname)
            if _value is not None:
                valid.add(_jsname)
                found.add(_jsname)
        
    
    def as_json(self):
        """ Serializes to JSON by inspecting `elementProperties()` and creating
        a JSON dictionary of all registered properties. 
        """
        js = {}
        errs = []
        
        # JSONify all registered properties
        found = set()
        nonoptionals = set()
        for name, jsname, typ, is_list, of_many, not_optional in self.elementProperties():
            if not_optional:
                nonoptionals.add(of_many or jsname)
            
            err = None
            value = getattr(self, name)
            if value is None:
                continue
            
            if is_list:
                if not isinstance(value, list):
                   err = TypeError("Expecting property \"{}\" on {} to be list, but is {}"
                       .format(name, type(self), type(value)))
                elif len(value) > 0:
                    if not self._matches_type(value[0], typ):
                        err = TypeError("Expecting property \"{}\" on {} to be {}, but is {}"
                            .format(name, type(self), typ, type(value[0])))
                    else:
                        lst = []
                        for v in value:
                            try:
                                lst.append(v.as_json() if hasattr(v, 'as_json') else v)
                            except:
                                err.append("Unexpected error:", sys.exc_info()[0])
                        found.add(of_many or jsname)
                        js[jsname] = lst
            else:
                if not self._matches_type(value, typ):
                    err = TypeError("Expecting property \"{}\" on {} to be {}, but is {}"
                        .format(name, type(self), typ, type(value)))
                else:
                    try:
                        found.add(of_many or jsname)
                        js[jsname] = value.as_json() if hasattr(value, 'as_json') else value
                    except:
                        err.append("Unexpected error:", sys.exc_info()[0])
            
            if err is not None:
                errs.append(err if isinstance(err, TypeError) else TypeError([err], name))
        
    
    def _matches_type(self, value, typ):
        if value is None:
            return True
        if isinstance(value, typ):
            return True
        if int == typ or float == typ:
            return (isinstance(value, int) or isinstance(value, float))
        return False