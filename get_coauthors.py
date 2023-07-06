import pandas as pd
from tqdm.cli import tqdm
from elsapy.elsclient import ElsClient
from utils import (
    Config,
    load_authors,
    get_coauthors_by_month,
    get_coauthors_by_year,
    filter_by_affiliation,
    get_names_from_authors,
    filter_by_student,
)

tqdm.pandas()

def get_coauthors(client, authors, year=None, month=None):
    if month is not None:
        assert year is not None

        return authors["SCOPUS ID"].progress_apply(
            lambda x: get_coauthors_by_month(client, x, year, month)
        )

    return authors["SCOPUS ID"].progress_apply(
        lambda x: get_coauthors_by_year(client, x, year)
    )


if __name__ == "__main__":
    # import argparse
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--month", type=str, help="Month of the year")
    # parser.add_argument("--year", type=str, help="Year")
    # parser.input_file("--input_file", type=str, required=True, help="Excel file with authors")
    # args = parser.parse_args()
    month = "05"
    year = "2021"

    config = Config("config.json")
    # Initialize the API client
    client = ElsClient(config.apikey)
    client.inst_token = config.insttoken

    authors = load_authors()#format="csv", input_file=input_file)
    # get coauthors for each author using Scopus ID
    coauthors = get_coauthors(client, authors, year=year)
    filter_by_affiliation(coauthors, "el paso")
    filter_by_student(coauthors, pd.read_csv("./students.csv", dtype=str))
    authors["coauthors"] = coauthors
    # get names from authors
    authors["coauthors"] = authors["coauthors"].apply(get_names_from_authors)
    # save to csv
    authors.to_csv(f"./coauthors_{year}_{month}.csv", index=False)
