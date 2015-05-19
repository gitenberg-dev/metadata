import yaml
import json
import metadata.marc as marc
import pymarc

def subject_constructor(loader, node):
    return node.tag[1:] + ":"+ loader.construct_scalar(node)

yaml.add_constructor(u'!LCSH', subject_constructor)
yaml.add_constructor(u'!LCC', subject_constructor)

PANDATA_STRINGFIELDS = [
    '_repo',
    'description',
    'funding_info',
    'issued_gutenberg',
    'language',
    'publication_date_original',
    'publisher_original',
    'rights',
    'rights_url',
    'title',
    'type',
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
    'identifiers',
    ]
    


# wrapper class for the json object 
class Pandata(object):
    def __init__(self, datafile):
        self.metadata = yaml.load(file(datafile, 'r'))
    
    def __getattr__(self, name):
        if name in PANDATA_STRINGFIELDS:
            return self.metadata.get(name, '')
        if name in PANDATA_LISTFIELDS:
            return self.metadata.get(name, [])
        if name in PANDATA_DICTFIELDS:
            return self.metadata.get(name, {})
    
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

