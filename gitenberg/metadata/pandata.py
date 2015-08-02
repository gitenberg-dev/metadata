import yaml
import json
import requests
import httplib
import datetime

def subject_constructor(loader, node):
    return (node.tag[1:] , loader.construct_scalar(node))

yaml.SafeLoader.add_constructor(u'!lcsh', subject_constructor)
yaml.SafeLoader.add_constructor(u'!lcc', subject_constructor)

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
    'subjects', 'covers',
    ]
PANDATA_DICTFIELDS = [
    'identifiers', 'creator', 'contributor'
    ]
    
def edition_name_from_repo(repo):
    if '_' in repo:
        return '_'.join(repo.split('_')[0:-1])
    return repo
    
# wrapper class for the json object 
class Pandata(object):
    def __init__(self, datafile):
        if datafile.startswith('https://') or datafile.startswith('https://'):
            r = requests.get(datafile)
            if r.status_code == httplib.OK:
                self.metadata = yaml.safe_load( r.content)
        else:
            self.metadata = yaml.safe_load(file(datafile, 'r').read())
    
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
        
    # the edition should be able to report ebook downloads, which should have format and url attributes
    def downloads(self):
        return []

    # the edition should be able to report an "ebook via" url
    def download_via_url(self):
        return []

    # these should be last name first
    def authnames(self):
        return [auth.get('author_sortname','') for auth in self.authors]
    
    # some logic to decide
    @property
    def publication_date(self):
        if self.metadata.get("publication_date",None):
            return  self.metadata["publication_date"]
        elif self.metadata.get("gutenberg_issued",None):
            return self.metadata["gutenberg_issued"]
        else:
            return str(datetime.datetime.now().date())
    
    # gets the right edition. stub method for compatibility with marc converter
    @staticmethod   
    def get_by_isbn(isbn):
        return None

    @property
    def _edition(self):
        if self.metadata.get("_edition", ''):
            return self.metadata["_edition"]
        elif self.identifiers.get("isbn", ''):
            return str(self.metadata.identifiers['isbn'][0])  #use first isbn if available
        elif self._repo:
            return edition_name_from_repo(self._repo)
        else:
            return 'book'  #this will be the default file name
