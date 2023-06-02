"""An example program that uses the elsapy module"""

from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json
import sys
import re
import datetime

name = sys.argv[1] 
month = int(sys.argv[3])
year = sys.argv[4]
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
doc_srch.execute(client, get_all = True)

with open('temp.json', 'w') as outputfile:
    json.dump(doc_srch.results, outputfile)

with open('temp.json') as inputfile:
    data = json.load(inputfile)

print(name)
total_citations = 0
#print(name + "length of data " + str(len(data)))

#if(len(data)!=1):
if(data):
    for publication in data:
#       print(publication)
        if("prism:coverDate" in publication):
#           if(publication["prism:coverDate"].find(month)!="-1" and "citedby-count" in publication and "dc:title" in publication):
            if("citedby-count" in publication and "dc:title" in publication):
            #print(publication["prism:coverDate"])
#            if("prism:coverDate" in publication and "dc:title" in publication):
#                if publication["prism:aggregationType"].find("Proceedings"): 
#                    print("\t" + publication["dc:title"])
#                    if("prism:aggregationType" in publication):
#                        print("\t" + publication["prism:aggregationType"] + ": " + publication["prism:publicationName"])
#                    if("prism:doi" in publication):
#                        print("\thttps://doi.org/" + publication["prism:doi"])
#                    if("prism:coverDate" in publication):
#                        datem = datetime.datetime.strptime(publication["prism:coverDate"], "%Y-%m-%d")
#                        print("Cover Date = " + str(datem))
                    datem = datetime.datetime.strptime(publication["prism:coverDate"], "%Y-%m-%d")
                    if((datem.month) == month):
                        print("\t" + publication["dc:title"])
                        if("prism:aggregationType" in publication):
                            print("\t" + publication["prism:aggregationType"] + ": " + publication["prism:publicationName"])
                        if("prism:doi" in publication):
                            print("\thttps://doi.org/" + publication["prism:doi"])
                        if("prism:coverDate" in publication):
                            print("\tCover Date = " + datem.strftime("%Y-%m-%d"))
                    else:
                        print("\tNo published work in this month ")
        else:
            print("\tNo published work in " + year)
#else:
#    print(name + " has not published this year")
#            print(datem.month)
#            print(type(datem.month))
#            print(month)
#            print(type(month))
#               print(year + ", " + name + ", " + publication["citedby-count"] + ", " + publication["dc:title"])
#                print(publication["prism:coverDate"])
#                print(publication["prism:coverDisplayDate"])
#           if("prism:eIssn" in publication):
#               print(publication["prism:eIssn"])
#           else:
#               print("No eIssn")
#            print(publication["affiliation"])
#            print(publication["affiliation-city"])
#            print(publication["affiliation-country"])
#            print(publication["prism:aggregationType"])
#            print(publication["source-id"])
#            print(publication["open-access"])
#            print(publication["openaccessFlag"])
#            print(publication["citedby-count"])
#####        if(publication.get('citedby-count') != None):
#####            total_citations = total_citations + int(publication["citedby-count"])
#####print (name + " has " + str(len(data)) + " Scopus indexed publications in " + str(year) + " and was cited " + str(total_citations) + " times.")
