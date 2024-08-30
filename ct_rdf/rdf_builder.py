import json
import os
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, XSD

# URImap defines which types are being used for when they have not been provided
uriMap = {
    "clinicalStudyType": URIRef('http://purl.obolibrary.org/obo/OPMI_0000418'),
    "hasIdentifier": URIRef('http://semanticscience.org/resource/SIO_000671'),
    "hasTitle": URIRef('http://purl.org/dc/elements/1.1/title'),
    "partOf": URIRef('http://purl.obolibrary.org/obo/BFO_0000050'),
    "investigation": URIRef('http://purl.obolibrary.org/obo/CTO_0000108'),
    "hasLabel": URIRef('http://www.w3.org/2000/01/rdf-schema#Label'),
    "hasPhase": URIRef('http://purl.obolibrary.org/obo/CTO_0000125'),
    "hasStatus": URIRef('http://purl.obolibrary.org/obo/OPMI_0000622'),
    "investigatesCondition": URIRef('http://investigatesCondition'),
    "medicalCondition": URIRef('http://purl.obolibrary.org/obo/OPMI_0000282'),
}

def turn_to_rdf(g, json_filename):
    with open(json_filename) as f:
        d = json.load(f)

    # this list of IDs will be added to a CSV output

    id_list = []

    for i in d:
        id = i['ctid']
        rdf_study = URIRef("https://clinicaltrials.gov/study/" + id)
        g.add((rdf_study, RDF.type, uriMap['clinicalStudyType']))
        g.add((rdf_study, uriMap['hasIdentifier'], Literal(id, datatype=XSD.string)))
        # write the list of IDs to a CSV file that can be used downstream
        id_list.append(id)

        title = i['title']
        g.add((rdf_study, uriMap['hasTitle'], Literal(title, datatype=XSD.string)))

        cids = i['cids']
        intervention = i['interventions']
        rdfint = URIRef('http://' + str(hash(intervention)))
        g.add((rdfint, uriMap['partOf'], rdf_study))
        g.add((rdfint, RDF.type, uriMap['investigation']))
        g.add((rdfint, uriMap['hasLabel'], Literal(intervention, datatype=XSD.string)))

        for cid in cids:
            g.add((rdfint, uriMap['hasIdentifier'], URIRef("https://pubchem.ncbi.nlm.nih.gov/compound/" + str(cid))))

        try:
            phase = i['phase']
            g.add((rdf_study, uriMap['hasPhase'], Literal(phase, datatype=XSD.string)))
        except KeyError:
            print("Phase not found in " + id)

        status = i['status']
        g.add((rdf_study, uriMap['hasStatus'], Literal(status, datatype=XSD.string)))

        try:
            conditions = i['conditions']
            if type(conditions) != list:
                conditions = [conditions]
            for con in conditions:
                medical_condition = URIRef('http://medical_condition' + str(hash(con)))
                g.add((medical_condition, RDF.type, uriMap['medicalCondition']))
                g.add((medical_condition, uriMap['hasLabel'], Literal(con, datatype=XSD.string)))
                g.add((rdf_study, uriMap['investigatesCondition'], medical_condition))

        except Exception as e:
            print(e)
            print("No conditions in " + id)

    # output a CSV that has all the NCT ids that can be used downstream
    with open("pubchem_id_list.csv", "w") as f:
        for i in id_list:
            f.write(f"{i}\n")

def build_rdf_from_json(inputfolder, ttlfilename):
    g = Graph()
    filelist = os.listdir(inputfolder)
    print(filelist)
    for file in filelist:
        turn_to_rdf(g, os.path.join(inputfolder, file))

    g.serialize(destination=ttlfilename)
