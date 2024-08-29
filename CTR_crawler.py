import requests, time
import json, rdflib, csv
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDFS, XSD

uriMap={
#    "clinicalStudyType" : URIRef('http://purl.obolibrary.org/obo/OPMI_0000418'),
    "hasIdentifier" : URIRef('http://semanticscience.org/resource/SIO_000671'),
    "runBy" : URIRef('http://runBy'),
    "hasTitle" : URIRef('http://purl.org/dc/elements/1.1/title'),
    "hasOfficialTitle" : URIRef('http://purl.org/dc/elements/1.1/title'),
    "hasLeadSponsor" : URIRef('http://hasLeadSponsor'),
    "hasBriefSummary" : URIRef('http://hasBriefSummary'),
    "hasDetailedSummary" : URIRef('http://hasDetailedSummary'),
    "hasCondition" : URIRef('http://hasCondition'),
    "hasConditionKeyword" : URIRef('http://hasConditionKeyword'),
    "isStudyType" : URIRef('http://isOfStudyType'),
    "hasPrimaryOutcome" : URIRef('http://hasPrimaryOutcome'),
    "hasSecondaryOutcome" : URIRef('http://hasSecondaryOutcome'),
    "hasEligibilityCriteria" : URIRef('http://hasEligibilityCriteria'),
    "hasConditionMesh" : URIRef('http://hasConditionMesh'),
    "hasInterventionMesh" : URIRef('http://hasInterventionMesh'),
    "hasLabel" : URIRef('http://www.w3.org/2000/01/rdf-schema#Label'),
}


## Crawling clinical trials gov API given a list of clinical trial identifiers
def parse_API(inputfile, start, end):
    data=[]
    with open(inputfile, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            data.append(row)

    filename="cltgov"+str(start)+"-"+str(end)+".ttl"

    g = Graph()
    for i in data[start:end]:
        response = requests.get('https://clinicaltrials.gov/api/v2/studies/'+i[0])
        time.sleep(1)
        json=response.json()

        studyIdentifier = URIRef("https://clinicaltrials.gov/study/" + json['protocolSection']['identificationModule']['nctId'])
        alternativeIdentifier = json['protocolSection']['identificationModule']['orgStudyIdInfo']['id']
        g.add((studyIdentifier, uriMap['hasIdentifier'], Literal(alternativeIdentifier, datatype=XSD.string)))

        organisationName = json['protocolSection']['identificationModule']['organization']['fullName']
        g.add((studyIdentifier, uriMap['runBy'], Literal(organisationName, datatype=XSD.string)))

        briefTitle=json['protocolSection']['identificationModule']['briefTitle']

        try:
            officialTitle=json['protocolSection']['identificationModule']['officialTitle']
        except:
            print("Offical Title not found in " + studyIdentifier)

        g.add((studyIdentifier, uriMap["hasTitle"], Literal(briefTitle, datatype=XSD.string)))
        g.add((studyIdentifier, uriMap["hasOfficialTitle"], Literal(officialTitle, datatype=XSD.string)))

        leadSponsor = json['protocolSection']['sponsorCollaboratorsModule']['leadSponsor']['name']
        g.add((studyIdentifier, uriMap['hasLeadSponsor'], Literal(leadSponsor, datatype=XSD.string)))

        ## descriptionModule
        briefSummary= json['protocolSection']['descriptionModule']['briefSummary']
        g.add((studyIdentifier, uriMap['hasBriefSummary'], Literal(briefSummary, datatype=XSD.string)))

        try:
            detailedSummary= json['protocolSection']['descriptionModule']['detailedDescription']
            g.add((studyIdentifier, uriMap['hasBriefSummary'], Literal(detailedSummary, datatype=XSD.string)))
        except:
            print("DetailedSummary is missing " + studyIdentifier)



        ## ConditionsModule
        conditions=json['protocolSection']['conditionsModule']['conditions']
        for con in conditions:
            g.add((studyIdentifier, uriMap['hasCondition'], Literal(con, datatype=XSD.string)))

        try:
            keywords=json['protocolSection']['conditionsModule']['keywords']
            for key in keywords:
                g.add((studyIdentifier, uriMap['hasConditionKeyword'], Literal(key, datatype=XSD.string)))
        except:
            print("Keywords are missing " + studyIdentifier)


        ## designModule
        studyType = json['protocolSection']['designModule']['studyType']
        g.add((studyIdentifier, uriMap['isStudyType'], Literal(studyType, datatype=XSD.string)))

        ## outcomesModule
        try:
            primaryOutcomes=json['protocolSection']['outcomesModule']['primaryOutcomes']
            for primaryOutcome in primaryOutcomes:
                g.add((studyIdentifier, uriMap['hasPrimaryOutcome'], Literal(primaryOutcome['measure'], datatype=XSD.string)))
                ## Optional? description and timeframe?
        except Exception as e:
            print("Primary Outcome not found in "+ studyIdentifier)

        try:
            secondaryOutcomes=json['protocolSection']['outcomesModule']['secondaryOutcomes']
            for secondaryOutcome in secondaryOutcomes:
                g.add((studyIdentifier, uriMap['hasSecondaryOutcome'], Literal(secondaryOutcome['measure'], datatype=XSD.string)))
        except:
            print("Secondary Outcome not found in " + studyIdentifier)


        ## eligibilityModule
        eligibilityCriteria = json['protocolSection']['eligibilityModule']['eligibilityCriteria']
        g.add((studyIdentifier, uriMap['hasEligibilityCriteria'], Literal(eligibilityCriteria, datatype=XSD.string)))


        try:
            condition_mesh = json['derivedSection']['conditionBrowseModule']['meshes']
            for con in condition_mesh:
                g.add((studyIdentifier, uriMap['hasConditionMesh'], URIRef("http://purl.bioontology.org/ontology/MESH/" + con["id"])))
                g.add((URIRef("http://purl.bioontology.org/ontology/MESH/"+con["id"]), URIRef('http://haslabel'), Literal(con["term"], datatype=XSD.string)))
        except Exception as e:
            print(e)
            print("DerivedSection/ConditionBrowseModule not found for " + studyIdentifier)

        try:
            intervention_mesh = json['derivedSection']['interventionBrowseModule']['meshes']
            for int in intervention_mesh:
                g.add((studyIdentifier, uriMap['hasInterventionMesh'], URIRef("http://purl.bioontology.org/ontology/MESH/" + int["id"])))
                g.add((URIRef("http://purl.bioontology.org/ontology/MESH/" + int["id"]), uriMap['hasLabel'], Literal(int["term"], datatype=XSD.string)))

        except Exception as e:
            print(e)
            print("DerivedSection/InterventionBrowseModule not found for " + studyIdentifier)

    g.serialize(destination="clt_enrichment/"+filename)



parse_API("study_id_partial.csv", 100, 500)