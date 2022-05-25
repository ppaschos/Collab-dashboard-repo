import pandas as pd
import json
import csv
from collections import defaultdict

# Points to csv snapshot of google sheets
AP_FILE_PATH = "./files/IGWN_sites-APs.csv"
CE_FILE_PATH = "./files/IGWN_sites-CE.csv"
INSTITUTES_PATH = "./files/IGWN_sites-Institutions.csv"


def parse_ces() -> pd.DataFrame:
    """Parses cs csv into json objects by institution"""

    df = pd.read_csv(CE_FILE_PATH)

    def f(x):
        d = {
            "ce": list(x["COMPUTE ENTRY POINT (CE)"].unique()),
            "latitude": x["Latitude"].unique()[0],
            "longitude": x["Longtitude"].unique()[0],
            "hosted_ce": x["Hosted CE"].unique()[0],
            "ce_location": x["CE location"].unique()[0]
        }

        return pd.Series(d)

    df = df.groupby("Institute Site").apply(f)

    return df


def parse_aps() -> pd.DataFrame:

    df = pd.read_csv(AP_FILE_PATH, index_col="Institute Site")

    def f(x):
        d = {
            "ap": list(x["Access Point"].unique())
        }

        return pd.Series(d)

    df = df.groupby("Institute Site").apply(f)

    return df


def export_institutes():
    """Exports institutions JSON File"""  # TODO - This should be merged with the one above ( Update data )

    df = pd.read_csv(INSTITUTES_PATH, index_col="Member Institution")

    d = df.to_dict(orient="index")

    with open("data/institutions.json", "w") as fp:
        json.dump(d, fp)


def export_sites():
    """Join AP and CE tables on Site Name and export to json file under data"""

    df_aps = parse_aps()
    df_ces = parse_ces()

    df = pd.merge(df_ces, df_aps, how="left", left_index=True, right_index=True)

    d = df.to_dict(orient="index")

    with open("data/sites.json", "w") as fp:
        json.dump(d, fp)


def main():
    export_sites()
    export_institutes()


if "__main__" == __name__:
    main()
