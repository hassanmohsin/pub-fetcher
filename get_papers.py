import pandas as pd
from tqdm.cli import tqdm
from elsapy.elsclient import ElsClient
from utils import (
    Config,
    get_coauthors_by_month,
    get_coauthors_by_year,
    filter_by_affiliation,
    get_names_from_authors,
    filter_by_student,
    get_search_result_by_year,
)
from utils import get_authors
from typing import List, Dict, Any

tqdm.pandas()


class Paper:
    doi: str
    title: str
    authors: List[Dict[str, Any]]
    year: str
    month: str
    url: str
    citations: int

    def __init__(self, doi, title, authors, year, month, citations):
        self.doi = doi
        self.title = title
        self.authors = authors
        self.year = year
        self.month = month
        self.url = f"https://doi.org/{doi}"
        self.citations = citations

    def __repr__(self):
        return f"{self.title} ({self.url})"

    def __str__(self):
        return f"{self.title} ({self.url})"


def get_paper_from_search(result):
    """
    result: a dict containing the search result for a single publication
    """
    # process the dict object and return a Paper object
    if "error" in result:
        return None
    doi = result.get("prism:doi", "")
    title = result.get("dc:title", "")
    authors = get_authors(doi)
    date = result.get("prism:coverDate", "")
    if date != "":
        year = date.split("-")[0]
        month = date.split("-")[1]
    else:
        year = ""
        month = ""
    citations = result.get("citedby-count", 0)
    return Paper(doi, title, authors, year, month, citations)


def author_list(paper):
    author_list = []
    for author in paper.authors:
        author_list.append(author.get("family", "") + ", " + author.get("given", ""))
    return author_list


def author_to_text(author, author_type="student"):
    if author_type == "student":
        return f"{author.get('Name', '')} | {author.get('Program', '')} | {author.get('Email', '')}"
    elif author_type == "professor":
        return f"{author.get('Name', '')} | {author.get('Title', '')} | {author.get('Department', '')}"
    elif author_type == "post-doc":
        return f"{author.get('Name', '')} | {author.get('Department', '')}"


def load_authors(input_file, author_type="student"):
    """
    Load authors from an excel file
    author_type: student or professor
    """
    if not author_type in ["student", "professor", "post-doc"]:
        raise ValueError("Author type must be student, post-doc or professor")

    data = pd.ExcelFile(input_file)
    dfs = []
    for sheet_name in data.sheet_names:
        if author_type in sheet_name.lower():
            dfs.append(data.parse(sheet_name, converters={"SCOPUS ID": str}))
    return pd.concat(dfs)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", type=str, required=True, help="Excel file with authors"
    )
    parser.add_argument("--output", type=str, required=True, help="Output file (.txt)")
    parser.add_argument(
        "--author_type",
        type=str,
        default="student",
        help="Type of author: student, post-doc or professor",
    )
    parser.add_argument("--month", type=str, help="Month of the year. e.g, 01, 02, ...")
    parser.add_argument("--year", type=str, help="Year. e.g, 2020")
    args = parser.parse_args()

    config = Config("config.json")
    # Initialize the API client
    client = ElsClient(config.apikey)
    client.inst_token = config.insttoken

    # load authors
    authors = load_authors(args.input, author_type=args.author_type)
    with open(args.output, "w", encoding="utf-8") as f:
        for row in tqdm(
            authors.iterrows(),
            total=len(authors),
            desc=f"Retrieving papers of the {args.author_type.lower()}s...",
        ):
            scopus_id = row[1]["SCOPUS ID"]
            if scopus_id is None:
                continue
            author_info = author_to_text(row[1], author_type=args.author_type)
            search_result = get_search_result_by_year(client, scopus_id, year=args.year)
            papers = [get_paper_from_search(x) for x in search_result]
            papers = [x for x in papers if x is not None]
            # sort by citations
            papers = sorted(papers, key=lambda x: x.citations, reverse=True)
            # filter by month
            if args.month is not None:
                papers = [x for x in papers if x.month == args.month]
            if len(papers) == 0:
                continue
            f.write(f"{author_info} ")
            citation_count = 0
            content = ""
            for i, paper in enumerate(papers):
                content += f"\t{i+1}. {paper.title}\n"
                content += f"\t\t- Published: {paper.year}-{paper.month}\n"
                content += f"\t\t- Authors: {'; '.join(author_list(paper))}\n"
                content += f"\t\t- Citations: {paper.citations}\n"
                content += f"\t\t- Link: {paper.url} \n"
                citation_count += int(paper.citations)
            f.write(
                f"| (Total Publications: {len(papers)}, Total Citations: {citation_count}) \n"
            )
            f.write(content)
            f.write("\n")
