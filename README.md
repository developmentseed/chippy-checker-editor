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

# How to install the plugin from zip file?

- Download ZIP file  from : https://github.com/developmentseed/chippy-checker-editor/archive/refs/heads/main.zip
- Click on `Plugins` -> `Manage and Install Plugins`, and then select the option  `Install from ZIP` and then select the zip file and  click in install.
![2022-07-11 12 03 43_fixed](https://user-images.githubusercontent.com/1152236/178319413-f6dac886-8bcf-4645-8ecb-c932ebbbfabd.gif)

# How to use the plugin?

![2022-07-11 12 16 50_fixed](https://user-images.githubusercontent.com/1152236/178321372-cc6d3f88-2067-4a1b-a495-285d18b52763.gif)
