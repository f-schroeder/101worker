import os
import json
import xmljson
import subprocess
from xml.etree.ElementTree import fromstring, tostring

#check smells for source-files
dir = os.path.dirname(__file__)
command = "java -jar " + dir + "\checkstyle.jar" + " -c " + dir + "\checkstyle_checks.xml" + " " + dir + "\Cut.java" + " -f xml"
cmdResult = subprocess.check_output(command, shell=True)

#convert xml to json
xml = fromstring(cmdResult)
jsonText = json.dumps(xmljson.badgerfish.data(xml))
'{"p": {"@id": 1, "$": "text"}}'
#xmljson.parker.etree({'ul': {'li': [1, 2]}})

#write json-text to file
file = open(dir + "\smells.json", 'w')
file.write(jsonText)
file.close()

print("smell detection done")

#os.system("java -jar " + dir + "\checkstyle.jar" + " -c " + dir + "\checkstyle_checks.xml" + " " + dir + "\Cut.java" + " -f xml > " + dir + "\smells.json")
