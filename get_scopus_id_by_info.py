from elsapy.elsclient import ElsClient
from elsapy.elssearch import ElsSearch
from utils import Config


config = Config("config.json")
# Initialize the API client
client = ElsClient(config.apikey)
client.inst_token = config.insttoken


def get_scopus_id_by_name(client, last_name, first_name, affiliation, verbose=False):
    """
    client: ElsClient
    last_name: str
    first_name: str
    affiliation: str
    verbose: bool

    return: str

    Example:
    - get_scopus_id_by_name(client, "MacDonald", "Eric", "University of Texas at El Paso")

    """
    auth_srch = ElsSearch(
        f"AUTHLASTNAME({last_name}) and AUTHFIRST({first_name}) and AFFIL({affiliation})",
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
        return ""


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--last_name", type=str, required=True, help="Last name")
    parser.add_argument("-f", "--first_name", type=str, required=True, help="First name")
    parser.add_argument("-a", "--affiliation", type=str, required=True, help="Affiliation name")
    args = parser.parse_args()

    scopus_id = get_scopus_id_by_name(
        client, args.last_name, args.first_name, args.affiliation
    )
    print("SCOPUS ID:", scopus_id if scopus_id != "" else "Not found")

    """
    Example: 
    - python get_scopus_id_by_info.py --l MacDonald --f Eric --a "University of Texas at El Paso"
    - python get_scopus_id_by_info.py --last_name MacDonald --first_name Eric --affiliation "University of Texas at El Paso"
    """
