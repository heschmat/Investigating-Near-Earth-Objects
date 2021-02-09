"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.
"""
import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = ('datetime_utc', 'distance_au', 'velocity_km_s', 'designation', 'name', 'diameter_km', 'potentially_hazardous')

    #@TODO: investigate why this version doesn't work properly? and then delte. 
    # with open(filename, 'w') as outfile:
    #     writer = csv.writer(outfile)
    #     # Create the header row
    #     row_header = ', '.join(fieldnames)
    #     writer.writerow(row_header)
    #     for app in results:
    #         name = '' if app.neo.name is None else app.neo.name
    #         diam = str(app.neo.diameter)
    #         hazard = str(app.neo.hazardous)
    #         row = f'{app.time}, {app.distance}, {app.velocity}, {app._designation}, {name}, {diam}, {hazard}'
    #         writer.writerow(row)

    with open(filename, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames = fieldnames)
        writer.writeheader()
        for app in results:
            app_dict = app.serialize()
            neo_dict = app_dict['neo']
            del app_dict['neo']
            app_dict.update(neo_dict)
            app_dict = {k: str(v) for k, v in app_dict.items()}
            writer.writerow(app_dict)


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    with open(filename, 'w') as f:
        if results is None or len(results) == 0:
            results = []
        # Convert each instance to a matching dictionary:
        results = [app.serialize() for app in results]
        json.dump(results, f, indent=2)
