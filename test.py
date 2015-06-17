import os
import unittest
import yaml
import json
import metadata.marc as marc
from metadata.pandata import Pandata
import pymarc

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), 'samples/pandata.yaml')
TESTDATA_MARCFILENAME = os.path.join(os.path.dirname(__file__), 'samples/testoutput.marc.xml')

class Yaml2MarcTest(unittest.TestCase):
    pandata = Pandata(TESTDATA_FILENAME)
    print "loaded"
    print pandata.issued_gutenberg
    record = marc.stub(pandata)
    open(TESTDATA_MARCFILENAME,"w+").write(pymarc.record_to_xml(record))

