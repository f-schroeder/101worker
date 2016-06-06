import os
import json
import xmljson
import subprocess
from xml.etree.ElementTree import fromstring, tostring

config = {
    'wantdiff': True,
    'wantsfiles': True,
    'threadsafe': True,
    'behavior': {
        'creates': [['resource', 'smell']]
    }
}

def update_file(context, f):

    #sets the used styleguide for smell-detection (can be 'sun' or 'google')
    styleguide = "sun" #"google"

    #reads the content of the file (primary resource)
    try:
        if f.endswith(".java"):
        
            #----
            #get required paths
            dir = os.path.dirname(__file__)

            subdir = "101worker" + os.sep + "modules" + os.sep + "detectSmells"
            if not dir.endswith(subdir):
                print("Error: Path is false!")
                
            #path concatination
            rootDir=dir[:-len(subdir)]
            #dataPath = rootDir + "101results" + os.sep + "101repo" + os.sep + f
            
            #print(type(f))
            #print(type(context.get_env("repo101dir")))

            dataPath = os.path.join(context.get_env("repo101dir"), f)

            #check smells for source-files
            command = "java -jar " + dir + os.sep + "checkstyle.jar -c " + dir + os.sep + "checkstyle_checks_" + styleguide + ".xml " + dataPath + " -f xml"
            cmdResult = subprocess.check_output(command, shell=True)
            
            #convert xml to json
            xml = fromstring(cmdResult)
            jsonText = xmljson.badgerfish.data(xml)
            jsonText["checkstyle"]["file"]["@name"] = f
            jsonText = json.dumps(jsonText)
            jsonText = json.loads(jsonText)
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
import string
from unittest.mock import Mock

class DetectSmellsTest(unittest.TestCase):
    
    def setUp(self):
        self.env = Mock()
        #pfad zum richtigen file setzen
        self.env.get_env.return_value = os.path.dirname(__file__)
    
    def test_run(self):
        change = {
            'type': 'NEW_FILE',
            'file': 'Cut.java'
        }
        run(self.env, change)
        #assert string mit samplefile
        expectedString = json.loads('{"checkstyle": {"@version": 6.18, "file": {"@name": "Cut.java", "error": [{"@line": 0, "@source": "com.puppycrawl.tools.checkstyle.checks.NewlineAtEndOfFileCheck", "@message": "File does not end with a newline.", "@severity": "warning"}, {"@line": 0, "@source": "com.puppycrawl.tools.checkstyle.checks.javadoc.JavadocPackageCheck", "@message": "Missing package-info.java file.", "@severity": "warning"}, {"@line": 5, "@source": "com.puppycrawl.tools.checkstyle.checks.javadoc.JavadocTypeCheck", "@message": "Missing a Javadoc comment.", "@severity": "warning"}, {"@line": 5, "@source": "com.puppycrawl.tools.checkstyle.checks.design.HideUtilityClassConstructorCheck", "@column": 1, "@message": "Utility classes should not have a public or default constructor.", "@severity": "warning"}, {"@line": 7, "@source": "com.puppycrawl.tools.checkstyle.checks.javadoc.JavadocMethodCheck", "@column": 5, "@message": "Missing a Javadoc comment.", "@severity": "warning"}, {"@line": 7, "@source": "com.puppycrawl.tools.checkstyle.checks.FinalParametersCheck", "@column": 28, "@message": "Parameter c should be final.", "@severity": "warning"}]}}}')
        #smellCount = len(jsontext['checkstyle']['file']['error'])
        self.env.write_derived_resource.assert_called_with('Cut.java', expectedString, "smell")


    def test_run_removed(self):
        change = {
            'type': '',
                'file': 'Cut.java'
            }
        run(self.env, change)
        
        self.env.remove_derived_resource.assert_called_with('Cut.java', 'smell')


def test():
    suite = unittest.TestLoader().loadTestsFromTestCase(DetectSmellsTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

