import yaml
import json
import metadata.marc as marc
from metadata.pandata import Pandata
import pymarc


pandata = Pandata("github/local/metadata/samples/pandata.yaml")
print "loaded"
print pandata.issued_gutenberg
record = marc.stub(pandata)
open("github/local/metadata/samples/pandata.marc.xml","w+").write(pymarc.record_to_xml(record))
