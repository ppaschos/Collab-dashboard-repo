import glob

import pandas as pd
import json


def parse_ces(path: str) -> pd.DataFrame:
    """Parses cs csv into json objects by institution"""

    df = pd.read_csv(path)

    def f(x):
        d = {
            "ce": list(x["COMPUTE ENTRY POINT (CE)"].unique()),
            "latitude": x["Latitude"].unique()[0],
            "longitude": x["Longitude"].unique()[0],
            "hosted_ce": x["Hosted CE"].unique()[0],
            "ce_location": x["CE location"].unique()[0]
        }

        return pd.Series(d)

    df = df.groupby("Institute Site").apply(f)

    return df


def parse_aps(path: str) -> pd.DataFrame:

    df = pd.read_csv(path, index_col="Institute Site")

    def f(x):
        d = {
            "ap": list(x["Access Point"].unique())
        }

        return pd.Series(d)

    df = df.groupby("Institute Site").apply(f)

    return df


def parse_institutes(path: str) -> pd.DataFrame:

    df = pd.read_csv(path)

    def f(x):
        d = {
            "labs": list(x["Lab"].unique()),
            "latitude": x["Latitude"].unique()[0],
            "longitude": x["Longtitude"].unique()[0],
            "country": x["Country"].unique()[0]
        }

        return pd.Series(d)

    df = df.groupby("Institute").apply(f)

    return df


def get_collaborations():
    """Grabs the prepended collaboration names from the csv file"""

    return list(set(x.split("/")[-1].split("-")[0] for x in glob.glob("indata/*")))


def get_collaboration_dictionary(collaboration: str):

    df_aps = pd.DataFrame()
    df_ces = pd.DataFrame()
    df_institutes = pd.DataFrame()

    ap_files_path = glob.glob(f"indata/{collaboration}-ap-sites.csv")
    ce_files_path = glob.glob(f"indata/{collaboration}-ce-sites.csv")
    institutes_path = glob.glob(f"indata/{collaboration}-institutes.csv")

    if ap_files_path:
        df_aps = parse_aps(ap_files_path[0])

    if ce_files_path:
        df_ces = parse_ces(ce_files_path[0])

    if institutes_path:
        df_institutes = parse_institutes(institutes_path[0])

    df_compute_sites = pd.merge(df_ces, df_aps, how="left", left_index=True, right_index=True)
    d_compute_sites = df_compute_sites.where(pd.notnull(df_compute_sites), None).to_dict(orient="index")

    d_institutes = df_institutes.to_dict(orient="index")

    return {collaboration.upper(): {"computeSites": d_compute_sites, "institutions": d_institutes}}

def export_collaboration_data():
    """Exports the collaboration csvs in a json file"""

    d = {}
    for collaboration in get_collaborations():
        d.update(get_collaboration_dictionary(collaboration))

    with open("data/collaborations.json", "w") as fp:
        json.dump(d, fp)


def main():
    export_collaboration_data()


if "__main__" == __name__:
    main()


#######################################################################################################################
# Deprecated Functions
#######################################################################################################################

AP_FILE_PATH = "./indata/igwn-ap-sites.csv"
CE_FILE_PATH = "indata/igwn-ce-sites.csv"
INSTITUTES_PATH = "indata/igwn-institutions.csv"

def export_institutes():
    """Deprecated - Exports institutions JSON File"""  # TODO - This should be merged with the one above ( Update data )

    df_institutes = parse_institutes(INSTITUTES_PATH)

    d = df_institutes.to_dict(orient="index")

    d = {"igwn": d}  # TODO this should be parsable from the csv file

    with open("data/institutions.json", "w") as fp:
        json.dump(d, fp)


def export_sites():
    """ DeprecatedJoin AP and CE tables on Site Name and export to json file under data"""

    df_aps = parse_aps(AP_FILE_PATH)
    df_ces = parse_ces(CE_FILE_PATH)

    df = pd.merge(df_ces, df_aps, how="left", left_index=True, right_index=True)

    d = df.where(pd.notnull(df), None).to_dict(orient="index")

    d = {"igwn": d}  # TODO this should be parsable from the csv file

    with open("data/sites.json", "w") as fp:
        json.dump(d, fp)