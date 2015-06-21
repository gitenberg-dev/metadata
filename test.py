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
    def setUp(self):
        self.pandata = Pandata(TESTDATA_FILENAME)
        
    def test_pandata(self):
        self.assertTrue( self.pandata.issued_gutenberg == "2007-03-03")
        self.assertTrue( isinstance( self.pandata.authors , list))
        self.assertTrue( isinstance( self.pandata.subjects[0] , tuple ))
        self.assertEqual( self.pandata.subjects[0][0] , u'lcsh' )

    def test_marc(self):
        record = marc.stub(self.pandata)
        for field in record.get_fields('650'):
            
            self.assertEqual(field.get_subfields('a')[0],  'Science fiction')
            break
        open(TESTDATA_MARCFILENAME,"w+").write(pymarc.record_to_xml(record))

