import os
import json
import xmljson
import subprocess
from xml.etree.ElementTree import fromstring, tostring

config = {
    'wantdiff': True,
    'wantsfiles': True,
    'threadsafe': True
}

def update_file(context, f):
    # reads the content of the file (primary resource)
    try:
        #source = context.get_primary_resource(f)
        if f.endswith(".java"):
        
            #----
            #get required paths
            dir = os.path.dirname(__file__)
            #subdir = "101worker" + os.sep + "modules" + os.sep + "detectSmells"
            #if not dir.endswith(subdir):
            #    print("Error: Path is false!")
                
            #path concatination
            #rootDir=dir[:-len(subdir)]
            #dataPath = rootDir + "101results" + os.sep + "101repo" + os.sep + f
            dataPath = os.path.join(context.get_env("repo101dir"), f)
			#check smells for source-files
            command = "java -jar " + dir + os.sep + "checkstyle.jar -c " + dir + os.sep + "checkstyle_checks_sun.xml " + dataPath + " -f xml"
            cmdResult = subprocess.check_output(command, shell=True)
            
            #convert xml to json
            xml = fromstring(cmdResult)
            jsonText = xmljson.badgerfish.data(xml)
            '{"p": {"@id": 1, "$": "text"}}'
            #xmljson.parker.etree({'ul': {'li': [1, 2]}})
            print("Finished detection of " + f)
            #----
        
            context.write_derived_resource(f, jsonText, 'smell')
    except UnicodeDecodeError:
        context.write_derived_resource(f, "", 'smell')

def remove_file(context, f):
    context.remove_derived_resource(f, 'smell')

def run(context, change):
    # dispatch the modified file
    if change['type'] == 'NEW_FILE':
        update_file(context, change['file'])

    elif change['type'] == 'FILE_CHANGED':
        update_file(context, change['file'])

    else:
        remove_file(context, change['file'])


import unittest
from unittest.mock import Mock

class DetectSmellsTest(unittest.TestCase):
    
    def setUp(self):
        self.env = Mock()
        #pfad zum richtigen file setzen
        self.env.get_primary_resource.return_value = 'x = 5\ny=6\nprint(x)\n'
    
    def test_run(self):
        change = {
            'type': 'NEW_FILE',
            'file': 'some-file.java'
        }
        run(self.env, change)
        #assert string mit samplefile
    self.env.write_derived_resource.assert_called_with(dir + 'some-file.py', 4, 'loc')


def test_run_removed(self):
    change = {
        'type': '',
            'file': 'some-file.java'
        }
        run(self.env, change)
        
    self.env.remove_derived_resource.assert_called_with('some-file.java', 'smell')


def test():
    suite = unittest.TestLoader().loadTestsFromTestCase(DetectSmellsTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

