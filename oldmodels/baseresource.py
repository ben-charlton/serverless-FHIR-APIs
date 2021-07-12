from . import element

class baseResource(element.Element):

    resource_type = 'baseResource'
    
    def __init__(self, jsondict=None, strict=True):
        
        self._server = None
        
        # raise if "resourceType" does not match
        if jsondict is not None and 'resourceType' in jsondict \
            and jsondict['resourceType'] != self.resource_type:
            raise Exception("Attempting to instantiate {} with resource data that defines a resourceType of \"{}\""
                .format(self.__class__, jsondict['resourceType']))
        
        super(baseResource, self).__init__(jsondict=jsondict, strict=strict)
    
    def as_json(self):
        js = super(baseResource, self).as_json()
        js['resourceType'] = self.resource_type
        return js
    
    
    # MARK: Handling Paths
    
    def relativeBase(self):
        return self.__class__.resource_type
    
    def relativePath(self):
        if self.id is None:
            return self.relativeBase()
        return "{}/{}".format(self.relativeBase(), self.id)
    
    @classmethod
    def read(cls, rem_id, server):
        """ Read the resource with the given id from the given server. The
        passed-in server instance must support a `request_json()` method call,
        taking a relative path as first (and only mandatory) argument.
        
        :param str rem_id: The id of the resource on the remote server
        :param FHIRServer server: An instance of a FHIR server or compatible class
        :returns: An instance of the receiving class
        """
        if not rem_id:
            raise Exception("Cannot read resource without remote id")
        
        path = '{}/{}'.format(cls.resource_type, rem_id)
        instance = cls.read_from(path, server)
        instance._local_id = rem_id
        
        return instance
    
    @classmethod
    def read_from(cls, path, server):
        """ Requests data from the given REST path on the server and creates
        an instance of the receiving class.
        
        :param str path: The REST path to read from
        :param FHIRServer server: An instance of a FHIR server or compatible class
        :returns: An instance of the receiving class
        """
        if not path:
            raise Exception("Cannot read resource without REST path")
        if server is None:
            raise Exception("Cannot read resource without server instance")
        
        ret = server.request_json(path)
        instance = cls(jsondict=ret)
        instance.origin_server = server
        return instance
    
    def create(self, server):
        """ Attempt to create the receiver on the given server, using a POST
        command.
        
        :param FHIRServer server: The server to create the receiver on
        :returns: None or the response JSON on success
        """
        srv = server or self.origin_server
        if srv is None:
            raise Exception("Cannot create a resource without a server")
        if self.id:
            raise Exception("This resource already has an id, cannot create")
        
        ret = srv.post_json(self.relativeBase(), self.as_json())
        if len(ret.text) > 0:
            return ret.json()
        return None
    
    def update(self, server=None):
        """ Update the receiver's representation on the given server, issuing
        a PUT command.
        
        :param FHIRServer server: The server to update the receiver on;
            optional, will use the instance's `server` if needed.
        :returns: None or the response JSON on success
        """
        srv = server or self.origin_server
        if srv is None:
            raise Exception("Cannot update a resource that does not have a server")
        if not self.id:
            raise Exception("Cannot update a resource that does not have an id")
        
        ret = srv.put_json(self.relativePath(), self.as_json())
        if len(ret.text) > 0:
            return ret.json()
        return None
    
    def delete(self, server=None):
        """ Delete the receiver from the given server with a DELETE command.
        
        :param FHIRServer server: The server to update the receiver on;
            optional, will use the instance's `server` if needed.
        :returns: None or the response JSON on success
        """
        srv = server or self.origin_server
        if srv is None:
            raise Exception("Cannot delete a resource that does not have a server")
        if not self.id:
            raise Exception("Cannot delete a resource that does not have an id")
        
        ret = srv.delete_json(self.relativePath())
        if len(ret.text) > 0:
            return ret.json()
        return None
    
    
    # MARK: - Search
    
    def search(self, struct=None):
        """ Search can be started via a dictionary containing a search
        construct.
        
        Calling this method with a search struct will return a `FHIRSearch`
        object representing the search struct, with "$type" and "id" added.
        
        :param dict struct: An optional search structure
        :returns: A FHIRSearch instance
        """
        if struct is None:
            struct = {'$type': self.__class__.resource_type}
        if self._local_id is not None or self.id is not None:
            struct['id'] = self._local_id or self.id
        return self.__class__.where(struct)
    