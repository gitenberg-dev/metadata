import os
import unittest
import yaml
import json
import gitenberg.metadata.marc as marc
import pymarc

from gitenberg.metadata.pandata import Pandata
from gitenberg.metadata.pg_rdf import pg_rdf_to_yaml


TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), '../samples/pandata.yaml')
TESTDATA_MARCFILENAME = os.path.join(os.path.dirname(__file__), '../samples/testoutput.marc.xml')
TESTDATA_PGRDFFILENAME = os.path.join(os.path.dirname(__file__), '../samples/pg20728.rdf')
TESTDATA_YAMLFILENAME = os.path.join(os.path.dirname(__file__), '../samples/testoutput.yaml')

class Yaml2MarcTest(unittest.TestCase):
    def setUp(self):
        self.pandata = Pandata(TESTDATA_FILENAME)
        
    def test_pandata(self):
        print self.pandata
        self.assertEqual( self.pandata.gutenberg_issued , "2007-03-03")
        self.assertTrue( isinstance( self.pandata.creator , dict))
        self.assertTrue( isinstance( self.pandata.subjects[0] , tuple ))
        self.assertEqual( self.pandata.subjects[0][0] , u'lcsh' )

    def test_marc(self):
        record = marc.stub(self.pandata)
        open(TESTDATA_MARCFILENAME,"w+").write(pymarc.record_to_xml(record))
        for field in record.get_fields('650'):
            
            self.assertEqual(field.get_subfields('a')[0],  'Science fiction')
            break
        for field in record.get_fields('100'):
            self.assertEqual(field.get_subfields('a')[0],  'Piper, H. Beam')
            break
        for field in record.get_fields('700'):
            self.assertEqual(field.get_subfields('4')[0],  'ill')
            break

class Rdf2YamlTest(unittest.TestCase):
        
    def test_conversion(self):
        yaml = pg_rdf_to_yaml(TESTDATA_PGRDFFILENAME)
        open(TESTDATA_YAMLFILENAME, "w+").write(json.dumps(yaml,indent=2, separators=(',', ': '), sort_keys=True))
        pandata = Pandata(TESTDATA_YAMLFILENAME)


if __name__ == '__main__':
    unittest.main()