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
            dataPath = rootDir + "101results" + os.sep + "101repo" + os.sep + f
            
			#check smells for source-files
            command = "java -jar " + dir + os.sep + "checkstyle.jar -c " + dir + os.sep + "checkstyle_checks_" + styleguide + ".xml " + dataPath + " -f xml"
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
        context.write_derived_resource(f, 0, 'smell')

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
