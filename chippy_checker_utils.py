# Edit CHIP_DIR, INPUT_LABEL_DIR, OUTPUT_LABEL_DIR settings.
# Then run from the python console in QGIS.


import sys, os, re, argparse
from matplotlib.patches import Polygon
from pathlib import Path
import simplejson as json
import csv
from qgis.core import *
from qgis.gui import *
from qgis.utils import *


def set_file_pairs(chips_directory, input_label_directory):
    """set image and label file pairs of the form (anyname).tif and (samename).geojson

    Args:
        chips_directory (str): Location of chips
        input_label_directory (str): Location of geojson labels

    Raises:
        FileNotFoundError: _description_

    Returns:
        _type_: _description_
    """
    chip_files = os.listdir(chips_directory)

    # extract image names and construct the paths of the label files
    basenames = [os.path.splitext(cfile)[0] for cfile in chip_files if cfile.endswith(".tif")]
    file_pairs = []
    for basename in basenames:
        chip_file = os.path.join(chips_directory, f"{basename}.tif")
        geojson_file = os.path.join(input_label_directory, f"{basename}.geojson")
        # if not os.path.exists(geojson_file):
        #     raise FileNotFoundError(f"Missing geojson file: {geojson_file}")
        geojson_file_exist = False
        if os.path.exists(geojson_file):
            geojson_file_exist = True
        file_pairs.append((basename, geojson_file_exist, False))
    return file_pairs


def get_record_status_file(records_directory, chips_directory, input_label_directory):

    records_json_file = os.path.join(records_directory, "chip_review_temporal.csv")
    if not os.path.exists(records_json_file):
        chip_files = set_file_pairs(chips_directory, input_label_directory)
        with open(records_json_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(chip_files)
    return records_json_file


def replace_line(file_name, line_num, text):
    lines = open(file_name, "r").readlines()
    lines[line_num] = text
    out = open(file_name, "w")
    out.writelines(lines)
    out.close()


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


# def set_output_json_file(self, output_json_file):
#     self.output_json_file = output_json_file
#     self.json_records = None
#     if os.path.exists(output_json_file):
#         with open(output_json_file, "r") as fh:
#             records = fh.read()
#             if records:
#                 self.json_records = json.loads(records)
#             else:
#                 self.json_records = []
#     else:
#         self.json_records = []
#     self.current_json_record = {}


# def set_record_dir(self, record_dir):
#     output_json_file = os.path.join(record_dir, "chip_review.json")
#     self.set_output_json_file(output_json_file)
