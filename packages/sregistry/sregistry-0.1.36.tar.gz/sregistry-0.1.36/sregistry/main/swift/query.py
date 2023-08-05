'''

ls: search and query functions for client

Copyright (C) 2018-2019 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

from sregistry.logger import bot
from sregistry.utils import remove_uri
from dateutil import parser

import json
import sys
import os

def search(self, query=None, args=None):
    '''query a Singularity registry for a list of images. 
     If query is None, collections are listed. 

    '''

    if query is not None:

        # Here you might do a function that is a general list
        # Note that this means adding the function Client in __init__
        return self._container_query(query)

    # or default to listing (searching) all things.
    return self._search_all()



def search_all(self):
    '''a "show all" search that doesn't require a query'''

    results = set()

    # Here we get names of collections, and then look up containers
    for container in self.conn.get_account()[1]:

        # The result here is just the name
        for result in self.conn.get_container(container['name'])[1]:
            results.add('%s/%s' %(container['name'], result['name']))

    if len(results) == 0:
        bot.info("No container collections found.")
        sys.exit(1)

    bot.info("Collections")
    bot.table([[x] for x in list(results)])
    return list(results)


def container_query(self, query):
    '''search for a specific container.
    This function would likely be similar to the above, but have different
    filter criteria from the user (based on the query)
    '''

    results = set()

    query = remove_uri(query)

    # Here we get names of collections, and then look up containers
    for container in self.conn.get_account()[1]:

        # The result here is just the name
        for result in self.conn.get_container(container['name'])[1]:
            if query in collection['name']:
                results.add('%s/%s' %(container['name'], result['name']))
   
    if len(results) == 0:
        bot.info("No container collections found.")
        sys.exit(1)

    bot.info("Collections")
    bot.table([list(results)])
    return list(results)
