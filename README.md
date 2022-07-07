# Chippy Checker Editor

Qgis plugin that allowed to review chips with their label-geojson matching file.


The plugin need to access to 4 directories, in order to work.

#### Records directory

At the beginning this folder is empty,  once you start reviewing  the tasks, the plugin will create 2 files.

- `missing_labels.csv` - This file contains  the location of the missing label-geojson files.
- `chip_review.csv` - This file contains the status of the reviewed chips, in case to resume the work later on.

#### Chips directory

This folder should contain the chips, that need to be reviewed. E.g: [dataset/chips](dataset/chips)

#### Input label directory

This folder should contain the label-geojson files. E.g: [dataset/labels](dataset/labels)

#### Output label directory

This folder will be used to store the output label-geojson files.

# How to install the plugin?

# How to use the plugin?