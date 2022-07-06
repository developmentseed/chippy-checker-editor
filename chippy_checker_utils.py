import sys, os, re, argparse
from matplotlib.patches import Polygon
from pathlib import Path
import simplejson as json
import csv
from qgis.core import *
from qgis.gui import *
from qgis.utils import *

def set_file_pairs(chips_directory, input_label_directory):
    """
    set image and label file pairs tif and geojson
    """
    list_files = os.listdir(chips_directory)
    # extract image names and construct the paths of the label files
    chip_basename_files = [os.path.splitext(cfile)[0] for cfile in list_files if cfile.endswith(".tif")]

    file_pairs = []
    for chip_basename in chip_basename_files:
        the_image = os.path.join(chips_directory, f"{chip_basename}.tif")
        the_geojson = os.path.join(input_label_directory, f"{chip_basename}.geojson")
        if not os.path.exists(the_geojson):
            raise FileNotFoundError(f"Missing geojson file: {the_geojson}")
        file_pairs.append((the_image, the_geojson))
    return iter(file_pairs), len(file_pairs)


def get_file_basename(filename):
    file_path, file_name = os.path.split(filename)
    file_basename, file_ext = os.path.splitext(file_name)
    return file_path, file_basename, file_ext


def display_info_pamel(title, body, time):
    iface.messageBar().pushMessage(title, body, level=Qgis.Info, duration=time)


def save_labels_to_output_dir(label_geojson_file, output_label_directory, vlayer):
    """Save puput geojson files."""
    _, file_basename, file_ext = get_file_basename(label_geojson_file)
    output_geojson_file = os.path.join(output_label_directory, f"{file_basename}.{file_ext}")
    QgsVectorFileWriter.writeAsVectorFormat(vlayer, output_geojson_file, "utf-8", vlayer.crs(), "GeoJSON")
    return


def write_status_records(status_json_file, json_records):
    if status_json_file == None:
        print("json output file not defined")
    with open(status_json_file, "w") as outfile:
        outfile.write(json.dumps(json_records))
    return


def write_status_records_csv(status_json_file, json_records):
    file_path, file_basename, file_ext = get_file_basename(status_json_file)
    csvfile = os.path.join(file_path, f"{file_basename}.csv")
    # remove files in case exist
    if os.path.exists(csvfile):
        os.remove(csvfile)
    # write the csv file
    if len(json_records) == 0:
        return
    keys = json_records[0].keys()
    csv_file = open(csvfile, "w")
    dict_writer = csv.DictWriter(csv_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(json_records)
    csv_file.close()
    return


def read_status_records(status_json_file):
    json_records = None
    if os.path.exists(status_json_file):
        with open(status_json_file, "r") as fh:
            records = fh.read()
            if records:
                json_records = json.loads(records)
            else:
                json_records = []
    else:
        json_records = []
    return json_records
