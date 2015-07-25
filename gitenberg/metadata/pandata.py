import yaml
import json
from . import marc
import pymarc

def subject_constructor(loader, node):
    return (node.tag[1:] , loader.construct_scalar(node))

yaml.add_constructor(u'!lcsh', subject_constructor)
yaml.add_constructor(u'!lcc', subject_constructor)

PANDATA_STRINGFIELDS = [
    '_repo',
    'description',
    'funding_info',
    'gutenberg_issued',
    'language',
    'publication_date_original',
    'publisher_original',
    'rights',
    'rights_url',
    'title',
    ]
    
PANDATA_AGENTFIELDS = [
    'authors',
    'editors_of_a_compilation',
    'translators',
    'illustrators',
    ]
PANDATA_LISTFIELDS = PANDATA_AGENTFIELDS + [
    'subjects',
    ]
PANDATA_DICTFIELDS = [
    'identifiers', 'creator', 'contributor'
    ]
    


# wrapper class for the json object 
class Pandata(object):
    def __init__(self, datafile):
        self.metadata = yaml.load(file(datafile, 'r'))
    
    def __getattr__(self, name):
        if name in PANDATA_STRINGFIELDS:
            value = self.metadata.get(name, '')
            if isinstance(value, str):
                return value
        if name in PANDATA_LISTFIELDS:
            return self.metadata.get(name, [])
        if name in PANDATA_DICTFIELDS:
            return self.metadata.get(name, {})
        return self.metadata.get(name, None)
    
    def agents(self, agent_type):
        agents = self.metadata.get(agent_type, [])
        return agents if agents else []
        
    # the edition should be able to report ebook downloads, with should have format and url attributes
    def downloads(self):
        return []

    # the edition should be able to report an "ebook via" url
    def download_via_url(self):
        return []

    # these should be last name first
    def authnames(self):
        return [auth.get('author_sortname','') for auth in self.authors]
    
    # gets the right edition
    @staticmethod   
    def get_by_isbn(isbn):
        return None

