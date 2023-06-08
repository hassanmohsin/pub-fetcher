from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json
import pandas as pd
import swifter
from tqdm.cli import tqdm

## Load configuration
class Config:
    def __init__(self, config_file):
        con_file = open(config_file)
        config = json.load(con_file)
        con_file.close()
        self.apikey = config['apikey']
        self.insttoken = config['insttoken']


config = Config("config.json")
# Initialize the API client
client = ElsClient(config.apikey)
client.inst_token = config.insttoken


def get_scopus_id_by_name(client, last_name, first_name, verbose=False):
    affiliation_id = '60007801' # UTEP
    auth_srch = ElsSearch(f'AUTHLASTNAME({last_name}) and AUTHFIRST({first_name}) and AF-ID({affiliation_id})','author')
    auth_srch.execute(client)
    if auth_srch.tot_num_res > 0:
        if verbose:
            print("auth_srch has " + str(auth_srch.tot_num_res) + " results.")
            print("First author has ID: " + str(auth_srch.results[0]['dc:identifier']))
        return auth_srch.results[0]['dc:identifier'].split(':')[1]
    else:
        if verbose: 
            print("auth_srch has 0 results.")
        return None


def get_scopus_id_by_info(row):
    # return row['SCOPUS ID'] if row['SCOPUS ID'] is not None
    if pd.notnull(row['SCOPUS ID']):
        return row['SCOPUS ID']
    else:
        last_name, first_name = row['Name'].split(',')
        scopus_id = get_scopus_id_by_name(client, last_name, first_name)
        return scopus_id if scopus_id is not None else row['SCOPUS ID']


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str, required=True, help='Excel file with authors')
    parser.add_argument('--output_file', type=str, required=True, help='Output file (.csv) with authors and SCOPUS IDs')
    parser.add_argument('--parallel', action='store_true', help='Use parallel processing')
    args = parser.parse_args()

    # read all the sheets in the excel file
    df = pd.read_excel(args.input_file, sheet_name=None, dtype={'Scopus ID': str})
    # concatenate all the sheets into one dataframe
    df = pd.concat(df.values(), ignore_index=True)
    df.head()

    print("Getting SCOPUS IDs for all authors...")
    if args.parallel:
        df['SCOPUS ID'] = df.swifter.progress_bar(True).apply(get_scopus_id_by_info, axis=1)
    else:
        tqdm.pandas()
        df['SCOPUS ID'] = df.progress_apply(get_scopus_id_by_info, axis=1)
    
    print("Saving to file...")
    df.to_csv(args.output_file, index=False)
