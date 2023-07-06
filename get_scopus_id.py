from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json
import pandas as pd
import swifter
from tqdm.cli import tqdm
from utils import Config


config = Config("config.json")
# Initialize the API client
client = ElsClient(config.apikey)
client.inst_token = config.insttoken


def get_scopus_id_by_name(client, last_name, first_name, verbose=False):
    affiliation_id = "60007801"  # UTEP
    auth_srch = ElsSearch(
        f"AUTHLASTNAME({last_name}) and AUTHFIRST({first_name}) and AF-ID({affiliation_id})",
        "author",
    )
    auth_srch.execute(client)
    if auth_srch.tot_num_res > 0:
        if verbose:
            print("auth_srch has " + str(auth_srch.tot_num_res) + " results.")
            print("First author has ID: " + str(auth_srch.results[0]["dc:identifier"]))
        return auth_srch.results[0]["dc:identifier"].split(":")[1]
    else:
        if verbose:
            print("auth_srch has 0 results.")
        return None


def get_scopus_id_by_info(row):
    # return row['SCOPUS ID'] if row['SCOPUS ID'] is not None
    if pd.notnull(row["SCOPUS ID"]):
        return row["SCOPUS ID"]
    else:
        print(f"Getting SCOPUS ID for {row['Name']}", end=": ")
        last_name, first_name = row["Name"].split(",")
        scopus_id = get_scopus_id_by_name(client, last_name, first_name)
        print(scopus_id)
        return scopus_id if scopus_id is not None else row["SCOPUS ID"]


def get_scopus_ids(excel_file, output_file):
    data = pd.ExcelFile(excel_file)
    with pd.ExcelWriter(output_file, mode="w", engine="openpyxl") as writer:
        for sheet_name in data.sheet_names:
            print(f"Getting SCOPUS IDs for sheet {sheet_name}...")
            df = data.parse(sheet_name)
            df["SCOPUS ID"] = df.apply(get_scopus_id_by_info, axis=1)
            if output_file is not None:
                df.to_excel(writer, sheet_name=sheet_name, index=False)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_file", type=str, required=True, help="Excel file with authors"
    )
    parser.add_argument(
        "--output_file",
        type=str,
        required=True,
        help="Output file (.xlsx) with authors and SCOPUS IDs",
    )
    args = parser.parse_args()

    get_scopus_ids(args.input_file, args.output_file)
