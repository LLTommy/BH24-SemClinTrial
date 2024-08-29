import requests
import os
import csv
import json
import time

def ask_json_from_cid(cid_filename, targetfolder):
    if not os.path.exists(targetfolder):
        os.makedirs(targetfolder)

    data = []
    with open(cid_filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            data.append(row)

    for i in data:
        cid = i[0]  # assuming i is a list with a single element
        baseurl = """https://pubchem.ncbi.nlm.nih.gov/sdq/sdqagent.cgi?infmt=json&outfmt=json&query={%22download%22:%22*%22,%22collection%22:%22clinicaltrials%22,%22order%22:[%22updatedate,desc%22],%22start%22:1,%22limit%22:10000000,%22downloadfilename%22:%22pubchem_cid_2244_clinicaltrials%22,%22nullatbottom%22:1,%22where%22:{%22ands%22:[{%22cid%22:%22XXXX%22}]}}"""
        query = baseurl.replace("XXXX", str(cid))
        response = requests.get(query)
        print(response.json())
        with open(os.path.join(targetfolder, 'pubchem_' + str(cid) + '.json'), 'w') as f:
            json.dump(response.json(), f)

        time.sleep(1)
