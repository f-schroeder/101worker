import os
import json

def run(env, res):
    data = env.read_dump('smellsPerContribution')

    if data is None:
        data = {}

    f = res['file']
    if f.endswith(".java"):
        if f.startswith('contributions' + os.sep):
            contribution = f.split(os.sep)[1]

            if data.get(contribution, None) is None:
                data[contribution] = 0

            #count smells for every java contribution
            jsontext = env.get_derived_resource(f, 'smell')
            smellCount = len(jsontext['checkstyle']['file']['error'])

            data[contribution] += smellCount

        env.write_dump('smellsPerContribution', data)
