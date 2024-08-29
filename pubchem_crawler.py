import json, requests,time, csv, os

import rdflib
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD


uriMap={
    "clinicalStudyType" : URIRef('http://purl.obolibrary.org/obo/OPMI_0000418'),
    "hasIdentifier" : URIRef('http://semanticscience.org/resource/SIO_000671'),
    "hasTitle" : URIRef('http://purl.org/dc/elements/1.1/title'),
    "partOf" : URIRef('http://purl.obolibrary.org/obo/BFO_0000050'),
    "investigation" : URIRef('http://purl.obolibrary.org/obo/CTO_0000108'),
    "hasLabel" : URIRef('http://www.w3.org/2000/01/rdf-schema#Label'),
    "hasPhase" : URIRef('http://purl.obolibrary.org/obo/CTO_0000125'),
    "hasStatus" : URIRef('http://purl.obolibrary.org/obo/OPMI_0000622'),
    "investigatesCondition" : URIRef('http://investigatesCondition'),
    "medicalCondition" : URIRef('http://purl.obolibrary.org/obo/OPMI_0000282'),
}



def extract_cid_from_json(basefile, targetfile):
    with open(basefile) as f:
        d = json.load(f)
        d=d["Annotations"]["Annotation"]

    with open(targetfile, 'w') as f:
        for i in d:
            cid=str(i["LinkedRecords"]["CID"][0])
            f.write(cid)
            f.write('\n')
    f.close()

def ask_json_from_cid(cid_filename, targetfolder):
    data=[]
    with open(cid_filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            data.append(row)

    for i in data:
        cid=i
        baseurl="""https://pubchem.ncbi.nlm.nih.gov/sdq/sdqagent.cgi?infmt=json&outfmt=json&query={%22download%22:%22*%22,%22collection%22:%22clinicaltrials%22,%22order%22:[%22updatedate,desc%22],%22start%22:1,%22limit%22:10000000,%22downloadfilename%22:%22pubchem_cid_2244_clinicaltrials%22,%22nullatbottom%22:1,%22where%22:{%22ands%22:[{%22cid%22:%22XXXX%22}]}}"""
        query=baseurl.replace("XXXX", str(cid))
        response = requests.get(query)
        print(response.json())
        with open(targetfolder+'/pubchem_'+str(cid[0])+'.json', 'w') as f:
            json.dump(response.json(), f)

        time.sleep(1)

def turn_to_rdf(g, json_Filename ):
    with open(json_Filename) as f:
        d = json.load(f)

    for i in d:
        id=i['ctid']
        rdf_study=URIRef("http://clinicaltrials.gov/study/" + id)
        g.add((rdf_study, RDF.type, uriMap['clinicalStudyType'] ))
        g.add((rdf_study, uriMap['hasIdentifier'], Literal(id, datatype=XSD.string)))

        title=i['title']
        g.add((rdf_study, uriMap['hasTitle'], Literal(title, datatype=XSD.string)))

        cids=i['cids']
        ##Where do the cids go?

        intervention=i['interventions']
        #for int in intervention:
        rdfint=URIRef('http://'+str(hash(intervention)))
        g.add(( rdfint, uriMap['partOf'], rdf_study ))
        g.add((rdfint, RDF.type, uriMap['investigation']))
        g.add((rdfint, uriMap['hasLabel'], Literal(intervention, datatype=XSD.string)))

        for cid in cids:
             g.add((rdfint, uriMap['hasIdentifier'], URIRef("https://pubchem.ncbi.nlm.nih.gov/compound/"+str(cid))))
#            g.add((rdfint, URIRef(('http://hasPubchemCID')), Literal(str(cid), datatype=XSD.string) ))
#            g.add((rdfint, URIRef('http://seeAlso'), Literal("https://pubchem.ncbi.nlm.nih.gov/compound/"+str(cid), datatype=XSD.string))) ## Link to pubchem


        try:
           phase=i['phase']
           g.add((rdf_study, uriMap['hasPhase'], Literal(phase, datatype=XSD.string)))
        except:
            print("Phase not found in "+id)

        status=i['status']
        g.add((rdf_study, uriMap['hasStatus'], Literal(status, datatype=XSD.string)))

        try:
            conditions=i['conditions']
            if type(conditions) != list:
                conditions=[conditions]
            for con in conditions:
                medical_condition = URIRef('http://medical_condition' + str(hash(con)))
                g.add((medical_condition, RDF.type, uriMap['medicalCondition']))
                g.add((medical_condition, uriMap['hasLabel'], Literal(con, datatype=XSD.string)))
                g.add((rdf_study, uriMap['investigatesCondition'], medical_condition))

        except Exception as e:
            print(e)
            print("No conditions in "+id)


def build_rdf_from_json(inputfolder, ttlfilename):
    g = Graph()
    filelist = os.listdir(inputfolder)
    print(filelist)
    for file in filelist:
        turn_to_rdf(g, inputfolder + file)

    g.serialize(destination=ttlfilename)


#extract_cid_from_json("PubChemAnnotations_EU Clinical Trials Register_heading=EU Clinical Trials Register.json", 'pubchem_EUCTR_cid.csv')
#extract_cid_from_json("PubChemAnnotations_ClinicalTrials.gov_heading=ClinicalTrials.gov.json", 'pubchem_cid.csv')
#extract_cid_from_json("PubChemAnnotations_NIPH Clinical Trials Search of Japan_heading=NIPH Clinical Trials Search of Japan.json", 'pubchem_JP_cid.csv')

#ask_json_from_cid('pubchem_EUCTR_cid.csv','pubchem_EU_CTR_compounds/')
#ask_json_from_cid('pubchem_cid.csv','pubchem_compounds/')
#ask_json_from_cid('pubchem_JP_cid.csv','pubchem_JP_compounds/')

#build_rdf_from_json("pubchem_compounds/", "PubChem_CTgove.ttl")
#build_rdf_from_json("pubchem_EU_CTR_compounds/", "PubChem_EU.ttl")
#build_rdf_from_json("pubchem_JP_compounds/", "PubChem_JP.ttl")


#ask_json_from_cid('pubchem_cid_partial.csv','test/')
build_rdf_from_json("test/", "PubChem_cid_partial.ttl")


## CTO
# Clinical trial rdf:type cto:Human_Subject_Study
# Clinical trial - cto:hasIdentifier - identifier #type: cto:ClinicalTrialRegistryIdentifer   http://purl.obolibrary.org/obo/IAO_0000578
# Clinical trial - cto:hasPhase
# Clinical trial - cto:hasCompletionDate
# Clinical trial - cto:hasStartDate
# Clinical trial - cto:hasLayTitle
# Clinical trial - cto:hasOfficialTitle
# Clinical trial - cto:investigatesCondition - medical condition

# medical condition rdf:type cto:MedicalIntervention
# medical condition skos:closeMAtch doid:Disease?

# Investigational drug administration ro:partOf clinicalTrial
# Investigational drug administration rdf:type cto:InvestigationalMolecularEntityAdministration