import yaml
import json
import copy
import requests
import httplib
import datetime
from .utils import marc_rels, inverse_marc_rels, plural, reverse_name

class TypedSubject(tuple):
    pass
        
def subject_constructor(loader, node):
    return TypedSubject((node.tag[1:] , loader.construct_scalar(node)))
def subject_representer(dumper, subject):
    return dumper.represent_scalar(u'!%s'% subject[0], subject[1])


yaml.SafeLoader.add_constructor(u'!lcsh', subject_constructor)
yaml.SafeLoader.add_constructor(u'!lcc', subject_constructor)
yaml.SafeLoader.add_constructor(u'!bisacsh', subject_constructor)
yaml.SafeDumper.add_representer(TypedSubject, subject_representer)

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
    'subjects', 'covers', 'edition_list',
    ]
PANDATA_DICTFIELDS = [
    'identifiers', 'creator', 'contributor', 'edition_identifiers',
    ]
    
def edition_name_from_repo(repo):
    if '_' in repo:
        return '_'.join(repo.split('_')[0:-1])
    return repo

def get_one(maybe_a_list):
    if  isinstance(maybe_a_list, list):
        return str(maybe_a_list[0])  #use first name if available
    else:
        return str(maybe_a_list)
    
# wrapper class for the json object 
class Pandata(object):
    def __init__(self, datafile=None):
        if datafile:
            if isinstance(datafile, Pandata):
                self.metadata=copy.deepcopy(datafile.metadata) # copy the metadata
            elif datafile.startswith('https://') or datafile.startswith('https://'):
                r = requests.get(datafile)
                if r.status_code == httplib.OK:
                    self.metadata = yaml.safe_load( r.content)
            else:
                self.metadata = yaml.safe_load(file(datafile, 'r').read())
            self.set_edition_id()
        else:
            self.metadata = {}
    
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
        
    def load(self, yaml_string):
        self.metadata = yaml.safe_load(yaml_string)
        self.set_edition_id()
    
    def set_edition_id(self):
        # set a (hopefully globally unique) edition identifier
        if not self.metadata.has_key('edition_identifiers'):
            self.metadata['edition_identifiers'] = {}
        base=self.url
        if not base:
            try:
                base = unicode(self.identifiers.keys[0])+':'+unicode(self.identifiers.values[0])
            except:
                base = u'repo:' + unicode(self._repo)
        self.metadata['edition_identifiers']['edition_id'] =  base + '#' + self._edition
    
    def agents(self, agent_type):        
        if self.creator.get(agent_type,None):
            agents=[self.creator.get(agent_type,None)]
        elif self.creator.get(plural(agent_type),None):
            agents=self.creator.get(plural(agent_type),None)
        elif self.contributor.get(agent_type,None):
            agents=[self.contributor.get(agent_type,None)]
        elif self.contributor.get(plural(agent_type),None):
            agents=self.contributor.get(plural(agent_type),None)
        else:
            agents = []
        return agents
        
    # the edition should be able to report ebook downloads, which should have format and url attributes
    # TODO - fill in URL based on a standard place in repo
    def downloads(self):
        return []

    # the edition should be able to report an "ebook via" url
    def download_via_url(self):
        return []

    # these should be last name first
    def authnames(self):
        return [auth.get('agent_name','') for auth in self.agents("author")]
    
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

            
    def get_one_identifier(self, id_name):
        if self.metadata.get(id_name,''):
            return get_one(self.metadata[id_name])  
        if self.identifiers.get(id_name,''):
            return get_one(self.identifiers[id_name])  
        if self.edition_identifiers.has_key(id_name):
            return get_one(self.edition_identifiers[id_name]) 
        return '' 

    @property
    def isbn(self):
        return self.get_one_identifier('isbn')

    @property
    def _edition(self):
        if self.metadata.get("_edition", ''):
            return unicode(self.metadata["_edition"])
        elif self.get_one_identifier('isbn'):
            return unicode(self.get_one_identifier('isbn'))  #use first isbn if available
        elif self._repo:
            return edition_name_from_repo(self._repo)
        else:
            return 'book'  #this will be the default file name

    def get_edition_list(self):
        yield self
        for edition in self.edition_list:
            new_self = Pandata(self)
            for key in edition.keys():
                new_self.metadata[key] = edition[key]
            new_self.set_edition_id()
            yield new_self
            
    def dump_file(self, file_name):
        with open(file_name,'w+') as f:
            f.write(self.__unicode__())
            
    def __unicode__(self):
        return yaml.safe_dump(self.metadata,default_flow_style=False,allow_unicode=True)
        