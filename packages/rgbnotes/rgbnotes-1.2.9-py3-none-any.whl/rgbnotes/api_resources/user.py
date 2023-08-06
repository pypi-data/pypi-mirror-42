from __future__ import absolute_import, division, print_function

from rgbnotes.api_resources.abstract import CreateableAPIResource
from rgbnotes.api_resources.abstract import ListableAPIResource


class User(ListableAPIResource, CreateableAPIResource):

    OBJECT_NAME = 'user'


    
