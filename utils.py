import json
import requests
from elsapy.elssearch import ElsSearch
from elsapy.elsclient import ElsClient
import pandas as pd
import time


## Load configuration
class Config:
    def __init__(self, config_file):
        con_file = open(config_file)
        config = json.load(con_file)
        con_file.close()
        self.apikey = config["apikey"]
        self.insttoken = config["insttoken"]


def get_search_result_by_year(client: ElsClient, scopus_id: str, year: str):
    search_string = f"AU-ID({scopus_id}) AND PUBYEAR = {year}"
    # print(search_string)
    doc_srch = ElsSearch(search_string, "scopus")
    while True:
        try:
            doc_srch.execute(client, get_all=True)
            break
        except Exception as e:
            print(e)
            print("Retrying...")
            time.sleep(5)
    # doc_srch.execute(client, get_all=True)
    return doc_srch.results


def get_search_result_by_month(
    client: ElsClient, scopus_id: str, year: str, month: str
):
    output = []

    for pub in get_search_result_by_year(client, scopus_id, year):
        cover_date = pub.get("prism:coverDate", None)
        if cover_date is not None and cover_date.split("-")[1] == month:
            output.append(pub)

    return output


def get_doi_from_paper(paper: dict):
    return paper.get("prism:doi", None)


def get_doi_from_papers(papers: list):
    output = []
    for paper in papers:
        output.append(paper.get("prism:doi", None))
    return [x for x in output if x is not None]


# https://api.crossref.org/works/10.2514/6.2021-3245


def get_authors(doi: str):
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url)
    if response.status_code == 200:
        message = response.json()["message"]
        if "author" in message:
            return message["author"]

    return []


def get_author_names_from_doi(doi: str):
    authors = get_authors(doi)
    output = []
    for author in authors:
        output.append(author.get("family", "") + "," + author.get("given", ""))
    return output

# TODO: use get_coauthors_by_year
def get_coauthors_by_month(client, scopus_id: str, year: str, month: str):
    if scopus_id is None:
        return []
    papers = get_search_result_by_month(client, scopus_id, year, month)
    dois = get_doi_from_papers(papers)
    coauthors = []
    for doi in dois:
        coauthors.extend(get_authors(doi))
    return coauthors


def get_coauthors_by_year(client, scopus_id: str, year: str):
    if scopus_id is None:
        return []
    papers = get_search_result_by_year(client, scopus_id, year)
    dois = get_doi_from_papers(papers)
    coauthors = []
    for doi in dois:
        coauthors.extend(get_authors(doi))
    return coauthors


def filter_by_affiliation(coauthors: pd.Series, affiliation: str):
    # coauthors is a pd.Series of lists of coauthors for each author
    for coauthor_list in coauthors:
        for i, coauthor in enumerate(coauthor_list):
            # Iterate over all affiliations of a coauthor
            affiliated = False
            for affil in coauthor["affiliation"]:
                if affiliation.lower() in affil["name"].lower():
                    affiliated = True
                    break
            if not affiliated:
                coauthor_list.pop(i)


def filter_by_student(coauthors: pd.Series, students: pd.DataFrame):
    students = students["Name"].apply(lambda x: x.lower()).values
    # coauthors is a pd.Series of lists of coauthors for each author
    for coauthor_list in coauthors:
        for i, coauthor in enumerate(coauthor_list):
            coauthor_name = coauthor.get("family", "") + "," + coauthor.get("given", "")
            if coauthor_name.lower() not in students:
                coauthor_list.pop(i)


def get_names_from_authors(authors: list):
    output = []
    for author in authors:
        output.append(author.get("family", "") + "," + author.get("given", ""))
    return output
