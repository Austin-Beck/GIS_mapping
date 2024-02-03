# Created by Austin Beck | austin.beck@aecom.com
# Intended to be run in ArcGIS Pro Python Window (could change aprx.activemap if you want to run this in Notebook instead)

#------------USER INPUTS-----------------------------------------------------
group_layer_name = '' # Name of group that all layers will have def query applied to
query = "" #SQL query within double quotes. ex: "DFIRM_PANEL = '38089C0189F'"
#------------DO NOT EDIT BELOW THIS LINE---------------------------------------------

import arcpy

# Create project object
aprx = arcpy.mp.ArcGISProject("CURRENT")

# Create object for current map
map = aprx.activeMap

# reset variable
group_layer = None

# Check to ensure group_layer_name is in active map
for lyr in map.listLayers():
    if lyr.isGroupLayer and lyr.name == group_layer_name:
        group_layer = lyr
        break

# Apply the definition query to each layer within the group
if group_layer:
    for lyr in group_layer.listLayers():
        if lyr.supports("DEFINITIONQUERY"):
            lyr.definitionQuery = query

            # Print the layer name and the applied definition query
            print(f"Applied definition query to layer '{lyr.name}': {query}")

print('Done')
