"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    # cols_wanted = ['full_name', 'pdes', 'name', 'neo', 'diameter', 'pha']
    # with open(neo_csv_path, 'r') as f:
    #     reader = csv.reader(f)
    #     header = next(reader)
    #     idx = [header.index(col) for col in cols_wanted]
    #     res = [header]
    #     for row in reader:
    #         res.append([row[i] for i in idx])
    # return res

    #res = {}
    res = []
    with open(neo_csv_path, 'r') as f:
        content_dict = csv.DictReader(f)
        for elm in content_dict:
            obj = NearEarthObject(**elm)
            #res[elm['pdes']] = obj
            res.append(obj)
    return res


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    fields_wanted = ['des', 'cd', 'dist', 'v_rel']
    with open(cad_json_path, 'r') as f:
        content = json.load(f)

    #res = {}
    res = []
    idx = [content['fields'].index(field) for field in fields_wanted]
    for itm in content['data']:
        info = [itm[i] for i in idx]
        info_dict = {k:v for k, v in zip(fields_wanted, info)}
        obj = CloseApproach(**info_dict)
        #res[info_dict['des']] = obj
        res.append(obj)
    return res
