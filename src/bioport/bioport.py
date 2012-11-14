'''
Created on Nov 14, 2012

@author: hoekstra
'''
from SPARQLWrapper import SPARQLWrapper, JSON
import requests
import re
import json
from pprint import pprint
import csv

BIOPORT_URL = 'http://www.biografischportaal.nl/personen/json'

if __name__ == '__main__':
    sparql = SPARQLWrapper('http://stcn.data2semantics.org/sparql')
    sparql.setReturnFormat(JSON)
    
    q = """PREFIX vocab: <http://stcn.data2semantics.org/vocab/resource/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT DISTINCT ?auteur ?naam WHERE {
        ?auteur a vocab:Auteur .
        ?auteur rdfs:label ?naam .
    }"""
    
    sparql.setQuery(q)
    
    results = sparql.query().convert()
    
    persons = []
    
    print len(results["results"]["bindings"]), "results"
    
    for result in results["results"]["bindings"]:
        naam = result["naam"]["value"]
        uri = result["auteur"]["value"]
        
        m = re.search(r"(.*?)\s\(.*",naam)
        years = re.findall(r"(\d{4})", naam)
        if m :
            name = m.group(1)
#            print naam, "'{}'".format(name), years
        else :
            name = naam
#            print "NOMATCH {}".format(naam)
            
        persons.append((uri,name,years))
        
#    print persons
    
    mapping = []
    
    with open('mappings.csv','w') as csvfile :
        count = 0
        writer = csv.writer(csvfile, delimiter=';',quotechar='\'', quoting=csv.QUOTE_MINIMAL)
        
        writer.writerow(['STCN','Biografisch Portaal','Note'])
        for (uri,n,ys) in persons:
    #        print n
            parameters = {'search_name': n}
            r = requests.get(BIOPORT_URL,params=parameters)
            
            try:
                bioport_result = json.loads(r.text)
            except:
                print "Whoops! Skipping {}".format(n)
                continue
            
    #        pprint(bioport_result)
#            if len(bioport_result) == 1 :
#                print "Match found: ", n, bioport_result[0]['namen']
#                writer.writerow([uri,bioport_result[0]['url_biografie'],'Direct match'])
#                count = count + 1
            if len(bioport_result) > 0:
#                print "Multiple results found, matching years"
                
                for bpr in bioport_result:
                    events = bpr['event']
                    for e in events:
                        if e['when']:
                            m = re.search(r'(\d{4})',e['when'])
                            if m:
                                year = m.group(1)
                                if year in ys:
                                    print "Match found: ", n, bpr['namen'], "for year {}".format(year)
                                    writer.writerow([uri,bpr['url_biografie'],'Match for year {}'.format(year)])
                                    count = count + 1
                                    # Escape from the loop, otherwise we'll add multiple matches if multiple years match.
                                    break

    print "Done ({} matches out of {})".format(count, len(results['results']['bindings']))
    
    

                                


            
            
            
        
            
        
    
    