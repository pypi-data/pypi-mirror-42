'''

Copyright (C) 2017-2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from sregistry.auth import read_client_secrets
from sregistry.main import ApiConnection
import json
import os

from .auth import authorize
from .pull import pull
from .push import push
from .delete import remove
from .query import *

class Client(ApiConnection):

    def __init__(self, secrets=None, base=None, **kwargs):
 
        self.base = base
        self._update_secrets()
        self._update_headers()
        self._update_base() 
        super(ApiConnection, self).__init__(**kwargs)

    def _update_base(self):
        if self.base is not None:
            if not self.base.endswith('api'):
                self.base = '%s/api' %self.base.strip('/')


    def _read_response(self,response, field="detail"):
        '''attempt to read the detail provided by the response. If none, 
        default to using the reason'''

        try:
            message = json.loads(response._content.decode('utf-8'))[field]
        except:
            message = response.reason
        return message


    def _update_secrets(self):
        '''update secrets will take a secrets credential file
        either located at .sregistry or the environment variable
        SREGISTRY_CLIENT_SECRETS and update the current client 
        secrets as well as the associated API base.
        '''
        self.secrets = read_client_secrets()
        if self.secrets is not None:
            if "registry" in self.secrets:
                if "base" in self.secrets['registry']:
                    self.base = self.secrets['registry']['base']
                    self._update_base()

    def __str__(self):
        return type(self)

    

Client.authorize = authorize
Client.remove = remove
Client.pull = pull
Client.push = push
Client.search = search
Client._search_all = search_all
Client._collection_search = collection_search
Client._container_search = container_search
Client._label_search = label_search
