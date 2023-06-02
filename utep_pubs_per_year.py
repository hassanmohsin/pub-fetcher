"""An example program that uses the elsapy module"""

from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json
import sys
import datetime

name = sys.argv[1] 
year = sys.argv[3]
scopus_id = sys.argv[2]
#print(name + " " + year + " " + scopus_id)

## Load configuration
con_file = open("config.json")
config = json.load(con_file)
con_file.close()
search_string =  "AU-ID(" + scopus_id + ") AND PUBYEAR = " + year
#print(search_string)

client = ElsClient(config['apikey'])
client.inst_token = config['insttoken']
doc_srch = ElsSearch(search_string ,'scopus')
#doc_srch = ElsSearch("AU-ID("+scopus_id+") AND PUBYEAR = " + year ,'scopus')
#doc_srch = ElsSearch("AFFIL(University of Texas at El Paso) AND AUTHOR-NAME("+name+") AND PUBYEAR = " + year ,'scopus')
doc_srch.execute(client, get_all = True)

with open('temp.json', 'w') as outputfile:
    json.dump(doc_srch.results, outputfile)

with open('temp.json') as inputfile:
    data = json.load(inputfile)

total_citations = 0
if(data):
    for publication in data:
        #print(data)
        #print(data.keys())
        #print("***********")
        #print(publication["dc:title"])
#       print("Cover date = " + publication["prism:coverDate"])
        #print(publication["prism:publicationName"])
        #print(publication["citedby-count"])
#        if("prism:coverDate" in publication):
#            datem = datetime.datetime.strptime(publication["prism:coverDate"], "%Y-%m-%d")
#        else:
#            print(name + ", no cover date")
#        if("prism:coverDate" in publication and "dc:title" in publication):
#           datem = datetime.datetime.strptime(publication["prism:coverDate"], "%Y-%m-%d")
#            print("month = " + str(datem.month))
#           print("\t" + publication["dc:title"])
#           if("prism:aggregationType" in publication):
#               print("\t" + publication["prism:aggregationType"] + ": " + publication["prism:publicationName"])
#           if("prism:doi" in publication):
#               print("\thttps://doi.org/" + publication["prism:doi"])
 
        if(publication.get('citedby-count') != None):
            total_citations = total_citations + int(publication["citedby-count"])
print (name + ", " + str(len(data)) + ", " + str(total_citations))
