# Edit CHIP_DIR, INPUT_LABEL_DIR, OUTPUT_LABEL_DIR settings.
# Then run from the python console in QGIS.


import sys, os, re, argparse
from matplotlib.patches import Polygon
from pathlib import Path
import simplejson as json
import csv
from qgis.core import *
from qgis.gui import *
from qgis.utils import *  # iface should be in here
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# Working settings for the editing session.
from .chippy_checker_utils import get_record_status_file, replace_line


# RECORD_DIR = r"/Users/ruben/Downloads/ramp_sierraleone_2022_05_31/PREP/tq_muscat"
# CHIP_DIR = r"/Users/ruben/Downloads/ramp_sierraleone_2022_05_31/PREP/tq_muscat/chips"
# INPUT_LABEL_DIR = r"/Users/ruben/Downloads/ramp_sierraleone_2022_05_31/PREP/tq_muscat/labels"
# OUTPUT_LABEL_DIR = r"/Users/ruben/Downloads/ramp_sierraleone_2022_05_31/PREP/tq_muscat/edited"

# # disable creation of aux.xml files when raster files are closed after labeling
# os.environ["GDAL_PAM_ENABLED"] = "NO"


# Used to check whether directory paths are given in the arguments
def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def get_file_basename(filename):
    mypath, myname = os.path.split(filename)
    basename, myext = os.path.splitext(myname)
    return basename


######################################################################################################


class EditSession:
    def __init__(
        self,
        iface,
        records_directory,
        chips_directory,
        input_label_directory,
        output_label_directory,
    ):
        self.iface = iface
        # self.accept_action = QAction("ACCEPT CHIP", self.iface.mainWindow())
        # self.reject_action = QAction("REJECT CHIP", self.iface.mainWindow())

        # # Note, calling 'connect(self.edit_next_label)' does nothing,
        # # even though it should be equivalent to this lambda call.
        # self.accept_action.triggered.connect(lambda: self.accept_label())
        # self.reject_action.triggered.connect(lambda: self.reject_label())
        # self.iface.addToolBarIcon(self.accept_action)
        # self.iface.addToolBarIcon(self.reject_action)
        # self.commentBox = QLineEdit(self.iface.mainWindow())
        # self.commentBox.setPlaceholderText("Your Comments Here")
        # self.iface.addToolBarWidget(self.commentBox)
        # self.iface.advancedDigitizeToolBar().setVisible(True)

        self.setupSession(
            records_directory,
            chips_directory,
            input_label_directory,
            output_label_directory,
        )

    # Modified CJ 2022.04.13 to check only basenames, in case you are on different paths or different machines
    def chip_already_reviewed(self, raster_file, vector_file):
        r_stem = Path(raster_file).stem 
        v_stem = Path(vector_file).stem
        for chip_record in self.json_records:
            cr_stem = Path(chip_record["chip"]).stem
            vr_stem = Path(chip_record["label"]).stem
            if vr_stem == v_stem and cr_stem == r_stem:
                return True
        return False

    # def chip_already_reviewed(self, vector_file):
    #     #check for presence of label file in output label directory
    #     edited_label_files = os.listdir(self.out_label_base)
    #     for filename in edited_label_files:
    #         if vector_file.endswith(filename):
    #             return True
    #     return False

    def setupSession(
        self,
        records_directory,
        chips_directory,
        input_label_directory,
        output_label_directory,
    ):
        self.raster_file = None
        self.vector_file = None

        # Directories
        self.chip_base = chips_directory
        self.in_label_base = input_label_directory
        self.out_label_base = output_label_directory
        # Records file

        # self.set_record_dir(record_dir)

        record_review_file = get_record_status_file(
            records_directory, chips_directory, input_label_directory
        )

        print(record_review_file)



        # with open(record_review_file, "r") as temp_file:
        #     with open(f"{record_review_file}.csv", "w") as status_file:
        #         for line in temp_file:
        #             chipId, exist_geojson_label, review_status = line.split(",")
        #             while True:
        #                 try:
        #                     # the_pair = next(self.chip_iterator)
        #                     geojson = f"{input_label_directory}/{chipId}.geojson"
        #                     raster  = f"{chips_directory}/{chipId}.tif"



        #                 except StopIteration:
        #                     # print("hit end of chips")
        #                     # self.show_end_of_chips_mbox()
        #                     return
                    
                    # chipId, exist_geojson_label, review_status = line.split(",")
                    # row =  f"{chipId}, {exist_geojson_label}, {review_status}"
                    # status_file.writelines(row)

                # chipId, exist_geojson_label, review_status = line.split(",")
                # replace_line(
                #     record_review_file,
                #     index,
                #     f"{chipId},{exist_geojson_label},{index}",
                # )

        # with open(record_review_file, "r", encoding="utf8") as file_source:
        #     # file_source.seek(499)
        #     file_content = file_source.readlines()

        #     for line in file_content:
        #     #     # if line.strip():
        #         chipId, exist_geojson_label, review_status = line.split(",")
        #         print(chipId)

        #             value = int(value)
        #             bunch.append((key, value))
        #             # Check the number of lines to read and once it achieve that number,
        #             # get the maximum x large numbers and set again the var “bunch” with the largest number.
        #             # so  in that way it will reduce to overloaded on memory.
        #             if len(bunch) == CHUNK_SIZE:
        #                 bunch = sort_tuples(bunch, large_numbers)
        # # with open(record_review_file, 'r') as read_obj:
        #     csv_reader = csv.reader(read_obj)
        #     header = next(csv_reader)
        # # Check file as empty
        # if header != None:
        #     # Iterate over each row after the header in the csv
        #     for row in csv_reader:
        #         print("=========")
        #         print(row)

        # # Set up json to contain results
        # # create record directory if not found
        # Path(record_dir).mkdir(parents=True, exist_ok=True)
        #

        # self.set_file_pairs()

        # self.reset_chip()

    def get_chip_file(self, snum, chips_list):
        for chip in chips_list:
            if chip.endswith(f"img{snum}.tif"):
                return chip
        raise FileNotFoundError(f"Image {snum} not found")

    def get_gjson_file(self, snum, json_list):
        for fvec in json_list:
            if fvec.endswith(f"img{snum}.geojson"):
                return fvec
        raise FileNotFoundError(f"Json {snum} not found")

    def set_file_pairs(self):
        """
        set image and label file pairs of the form (anyname).tif and (samename).geojson
        """
        chip_files = os.listdir(self.chip_base)

        print(chip_files)
        # extract image names and construct the paths of the label files
        basenames = [
            os.path.splitext(cfile)[0] for cfile in chip_files if cfile.endswith(".tif")
        ]

        file_pairs = []
        for basename in basenames:
            the_image = os.path.join(self.chip_base, f"{basename}.tif")
            the_geojson = os.path.join(self.in_label_base, f"{basename}.geojson")
            if not os.path.exists(the_geojson):
                raise FileNotFoundError(f"Missing geojson file: {the_geojson}")
            file_pairs.append((the_image, the_geojson))
        self.chip_iterator = iter(file_pairs)

    def save_labels_to_output_dir(self):
        label_file = self.vector_file
        the_directory, label_file = os.path.split(label_file)
        outpath = os.path.join(self.out_label_base, label_file)
        # vlayer = iface.activeLayer()
        QgsVectorFileWriter.writeAsVectorFormat(
            self.vlayer, outpath, "utf-8", self.vlayer.crs(), "GeoJSON"
        )
        return

    def reset_chip(self):
        """
        operations common to accepting and rejecting the previous chip
        """
        # clear the previous project
        # prevent it asking you to save changes
        #         the_project = QgsProject.instance()
        #         the_project.setDirty(False)
        #         the_project.removeAllMapLayers()
        # #        the_project.clear()

        while True:
            try:
                the_pair = next(self.chip_iterator)
            except StopIteration:
                print("hit end of chips")
                self.show_end_of_chips_mbox()
                return

            raster_file = the_pair[0]
            vector_file = the_pair[1]
            if not self.chip_already_reviewed(raster_file, vector_file):
                break

        self.raster_file = raster_file
        self.vector_file = vector_file

        # load chip, label into QGIS
        rlayer = iface.addRasterLayer(self.raster_file)
        display_name = get_file_basename(self.vector_file)
        vlayer = QgsVectorLayer(self.vector_file, display_name, "ogr")

        # check feature count and whether geometry type is polygon
        if vlayer.geometryType() != 2:
            # create new vector layer in ram and load it
            vlayer = QgsVectorLayer("Polygon", display_name, "memory")

        # for use later, in writing out files
        self.vlayer = vlayer
        self.rlayer = rlayer

        QgsProject.instance().addMapLayer(vlayer)
        iface.setActiveLayer(vlayer)
        iface.mapCanvas().setExtent(rlayer.extent())
        iface.mapCanvas().zoomToFullExtent()
        activelayer = iface.activeLayer()
        # change style of vector layer
        myRenderer = activelayer.renderer()
        mySymbol1 = QgsFillSymbol.createSimple(
            {"color": "255,0,0,0", "color_border": "#FF0000", "width_border": "0.4"}
        )
        myRenderer.setSymbol(mySymbol1)
        activelayer.triggerRepaint()

        # toggle label editing
        iface.actionToggleEditing().trigger()

        # reset json record and comment box
        self.current_json_record = {}
        self.current_json_record["chip"] = raster_file
        self.current_json_record["label"] = vector_file
        self.commentBox.setText("")
        self.commentBox.setPlaceholderText("Your Comment Here")
        return

    def getComment(self):
        return self.commentBox.text()

    def write_to_output_json_file(self):
        if self.output_json_file == None:
            print("json output file not defined")
            return
        with open(self.output_json_file, "w") as outfile:
            outfile.write(json.dumps(self.json_records))
        self.writeCsvFile()

    def set_output_json_file(self, output_json_file):
        self.output_json_file = output_json_file
        self.json_records = None
        if os.path.exists(output_json_file):
            with open(output_json_file, "r") as fh:
                records = fh.read()
                if records:
                    self.json_records = json.loads(records)
                else:
                    self.json_records = []
        else:
            self.json_records = []
        self.current_json_record = {}

    def set_record_dir(self, record_dir):
        output_json_file = os.path.join(record_dir, "chip_review.json")
        self.set_output_json_file(output_json_file)

    def writeCsvFile(self):

        # get name of csv file
        filebase, jsonext = os.path.splitext(self.output_json_file)
        csvfile = filebase + ".csv"
        if os.path.exists(csvfile):
            os.remove(csvfile)
        # write the csv file
        if len(self.json_records) == 0:
            return
        keys = self.json_records[0].keys()
        csv_file = open(csvfile, "w")

        dict_writer = csv.DictWriter(csv_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(self.json_records)
        csv_file.close()
        return

    def record_rejected(self):
        comment = self.getComment()
        if comment is None:
            comment = ""
        print(f"REJECTED: {self.current_json_record['chip']}")

        self.current_json_record["accept"] = False
        self.current_json_record["comment"] = comment
        self.json_records.append(self.current_json_record)
        self.write_to_output_json_file()
        self.current_json_record = {}

    def reject_label(self):
        QgsProject.instance().clear()
        self.record_rejected()
        self.reset_chip()

    def record_accepted(self):
        comment = self.getComment()
        if comment is None:
            comment = ""
        print(f"ACCEPTED: {self.current_json_record['chip']}")
        self.current_json_record["accept"] = True
        self.current_json_record["comment"] = comment
        self.json_records.append(self.current_json_record)
        self.current_json_record = {}
        self.write_to_output_json_file()

    def accept_label(self):

        # export current layer to the output directory
        if self.iface.activeLayer() is not None:
            self.save_labels_to_output_dir()
        QgsProject.instance().clear()
        self.record_accepted()
        self.reset_chip()

    def show_end_of_chips_mbox(self):
        iface.messageBar().pushMessage(
            "Heads up", "You have no more labels to edit!", level=Qgis.Info, duration=5
        )


# def main():
# EditSession(iface, RECORD_DIR, CHIP_DIR, INPUT_LABEL_DIR, OUTPUT_LABEL_DIR)

# main()
