import rdflib
import json
import string
import yaml

from rdflib_jsonld import serializer

def unblank_node(node, bnodes):
    if isinstance(node,dict):
        if "@id" in node and node["@id"].startswith("_"):
            if len(node)==1:
                return bnodes[node["@id"]]
            else:
                return None
        else:
            newdict = {}
            for key in node.keys():
                newdict[key]= unblank_node(node[key], bnodes)
            return newdict
    elif isinstance(node,list):
        newlist=[]
        for item in node:
            newnode= unblank_node(item, bnodes)
            if newnode:
                newlist.append(newnode)
        return newlist
    else:
        return node



def plural(key):
    if key.endswith('s'):
        return key+'es'
    else:
        return key+'s'
        
def get_url(key, val, entities=None):
    try:
        return (key, val['@id'])
    except KeyError:
        return None
    
def get_value(key, val, entities=None):
    try:
        return (key, val['@value'])
    except KeyError:
        try:
            return (key, val["rdf:value"]['@value'])
        except:
            try :
                return (key, val["rdf:value"])
            except KeyError:
                return (key, None)

def set_listable_entity(key, val, entities=None) : 
    list_of_vals = []
    if isinstance(val, list):
        for item in val:
            list_of_vals.append(set_entity(key, item, entities)[1])
        return (plural(key), list_of_vals)            
    else:
        return set_entity(key, val, entities)

def pgimagepath(val):
    return val[val.find("files/")+6:]
    
def get_imagefile(key, val, entities=None) : 
    if isinstance(val,str):
        return (key, {"image_path": pgimagepath(val)})
    elif isinstance(val,list):
        images=[]
        for image in val:
            image = pgimagepath(image)
            if not image in images:
                images.append(image)
        covers=[]
        for image in images:
            covers.append({"image_path": image})
        return (key,covers)
                
            

def set_entity(key, val, entities=None) :  
    uri = val.get('@id',None)
    if entities and entities.has_key(uri):
        if uri.startswith("http://www.gutenberg.org/2009/agents/"):
            entities[uri]["agent_id_gutenberg"] = uri[37:]
        return (key, entities[uri])
    else:
        return uri

def listable(key, val, entities=None) : 
    list_of_vals = []
    if isinstance(val, list):
        for item in val:
            list_of_vals.append(item)
        return (plural(key), list_of_vals)            
    else:
        return (key, val)
    
def get_subjects(key, val, entities=None) :
    subjects = []
    for subject in val:
        try:
            authority = subject["dcam:memberOf"]["@id"]
            authority = authority[8:].lower() if authority.startswith("dcterms:") else authority
            
        except KeyError:
            authority = ''
        try:
            value = subject["rdf:value"]
        except KeyError:
            value = subject
        if authority:
            subjects.append(("!%s:%s" % (authority, value)))
        else:
            subjects.append(( value))
    return (key, subjects)
        
def identifiers(node,entities=None):
    uri = node.get('@id',None)
    pg_id = uri[32:] if uri.startswith('http://www.gutenberg.org/ebooks/') else None
    ids = node.get('identifiers',{})
    if pg_id:
        ids['gutenberg']=pg_id
    node['identifiers']=ids
    
def add_by_path(value,target,path):
    path = str(path)
    if '/' in path:
        keys = path.split('/')
        newpath = string.join(keys[1:],'/')
        newdict = target.get(keys[0],{})
        add_by_path(value,newdict,newpath)
        target[keys[0]]=newdict
    else:
        prev = target.get(path,None)
        if isinstance(prev,dict) and isinstance(value,dict):
            prev.update(value)
        else:
            target[path] = value

        
def mapdata(node, mapping, entities):
    if isinstance(node, dict):
        mapped={}
        for (k,v) in node.iteritems():
            try:
                mapping_v=mapping[k]
                if isinstance(mapping_v,str):
                    add_by_path(v,mapped,mapping_v) 
                elif mapping_v is None:
                    continue
                else:
                    (key,value) = mapping_v[1](mapping_v[0],v,entities)
                    add_by_path(value,mapped,key) 
            except KeyError:
                add_by_path(v,mapped,k)
        return mapped
        
pandata_map ={
"@type":None,
"@id": "url",
"cc:license":None, 
"dcterms:alternative":"", 
"dcterms:creator": ("author", set_listable_entity)  ,
"dcterms:description":"description", 
"dcterms:hasFormat": None,
"dcterms:issued": ("issued_gutenberg",get_value),
"dcterms:language":("language", get_value),
"dcterms:license": None,
"dcterms:publisher": "publisher",
"dcterms:rights":"rights",
"dcterms:subject":("subjects", get_subjects), 
"dcterms:tableOfContents":"", 
"dcterms:title":"title", 
"dcterms:type": ("pg_type", get_value),
"marcrel:adp": ("adapter", set_entity), 
"marcrel:aft": ("author_of_afterword", set_entity), 
"marcrel:ann": ("annotator", set_entity), 
"marcrel:arr": ("arranger", set_entity), 
"marcrel:art": ("artist", set_entity), 
"marcrel:aui": ("author_of_introduction", set_entity), 
"marcrel:clb": ("contributor", set_entity), 
"marcrel:cmm": ("commentator", set_entity), 
"marcrel:cmp": ("composer", set_entity), 
"marcrel:cnd": ("conductor", set_entity), 
"marcrel:com": ("compiler", set_entity), 
"marcrel:ctb": ("contributor", set_entity), 
"marcrel:dub": ("dubious_author", set_entity), 
"marcrel:edt": ("editor", set_entity), 
"marcrel:egr": ("engineer", set_entity), 
"marcrel:ill": ("illustrator", set_entity)  ,
"marcrel:lbt": ("librettist", set_entity), 
"marcrel:oth": ("other_contributor", set_entity), 
"marcrel:pbl": ("publisher_contributor", set_entity), 
"marcrel:pht": ("photographer", set_entity), 
"marcrel:prf": ("performer", set_entity), 
"marcrel:prt": ("printer", set_entity), 
"marcrel:res": ("researcher", set_entity),
"marcrel:trc": ("transcriber", set_entity), 
"marcrel:trl": ("translator", set_entity), 
"marcrel:unk": ("unknown_contributor", set_entity), 
"pgterms:alias": ("alias", listable),
"pgterms:birthdate":"birthdate", 
"pgterms:bookshelf":("gutenberg_bookshelf", get_value), 
"pgterms:deathdate":"deathdate", 
"pgterms:downloads": None,
"pgterms:marc010":"identifiers/lccn", 
"pgterms:marc020":"identifiers/isbn", 
"pgterms:marc250":"edition_note", 
"pgterms:marc260":"publication_note", 
"pgterms:marc300":"physical_description_note", 
"pgterms:marc440":"series_note", 
"pgterms:marc508":"production_note", 
"pgterms:marc520":"summary", 
"pgterms:marc546":"language_note", 
"pgterms:marc653": None, 
"pgterms:marc901": ("cover", get_imagefile), 
"pgterms:marc902": ("titlepage_image", get_imagefile), 
"pgterms:marc903":("back_cover", get_imagefile),
"pgterms:name":"agent_name", 
"pgterms:webpage": ("wikipedia",get_url),
"rdfs:comment":None, 
}
pandata_adders = [identifiers]
    
context =   {
    "cc": "http://web.resource.org/cc/",
    "dcam": "http://purl.org/dc/dcam/",
    "dcterms": "http://purl.org/dc/terms/",
    "marcrel": "http://id.loc.gov/vocabulary/relators/",
    "pgterms": "http://www.gutenberg.org/2009/pgterms/",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    }

def pg_rdf_to_yaml(file_path):
    return yaml.safe_dump(pg_rdf_to_json(file_path),default_flow_style=False)
    
def pg_rdf_to_json(file_path):
    g=rdflib.Graph()
    g.load(file_path)

    #print(g.serialize(format='json-ld', indent=4, context=context))
    ld = serializer.from_rdf(g, context_data=context, base=None,
            use_native_types=False, use_rdf_type=False,
            auto_compact=False, startnode=None, index=False)


    graph = ld['@graph']
    #print(json.dumps(graph,indent=2, separators=(',', ': '), sort_keys=True))

    nodes = {}
    for obj in graph:
        if isinstance(obj,dict):
            obj = obj.copy()
            if "@id" in obj and obj["@id"].startswith("_"):
                nodeid = obj["@id"]
                node = nodes.get(nodeid,{})
                del obj["@id"]
                node.update(obj)
                nodes[nodeid] = node
            
    # now remove the blank nodes and the files
    newnodes = []
    top = None
    for obj in unblank_node(graph,nodes):
        try:
            #
            if obj['@type']== 'pgterms:file':
                continue
            elif obj['@type']== 'pgterms:ebook':
                top = obj
            elif obj.has_key('@id') and (unicode(obj['@id'])=='http://www.gutenberg.org/'):
                continue
            else:
                newnodes.append(obj)
        except KeyError:
            continue

    #print(json.dumps(top,indent=2, separators=(',', ': '), sort_keys=True))
    
    entities={}                   
    for node in newnodes:
        node_id=node.get('@id',None)
        if node_id:
            entities[node_id]=mapdata(node,pandata_map,entities)
    for adder in pandata_adders:
        adder(top,entities)
    top2 = mapdata(top, pandata_map, entities)     
    return top2
    
#print(json.dumps(pg_rdf_to_yaml('/Users/eric/Downloads/cache/epub/19218/pg19218.rdf'),indent=2, separators=(',', ': '), sort_keys=True))

