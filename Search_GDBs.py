# Created by Austin Beck | austin.beck@aecom.com
# Intended to be run in ArcGIS Pro Notebook or Python Window

# This script uses a keyword to search for a GDB featureclass within a directory and its subdirectories 

#------------USER INPUTS---------------------------------------------------------------------
root_directory = r"c:" # starting directory to search (all subdirectories will also be searched)
keyword = "example" # feature class needs to contain these characters in sequence (not case sensitive, so can be all lower case)
#------------DO NOT EDIT BELOW THIS LINE-----------------------------------------------------

import os
import arcpy

def search_gdb_feature_class(root_directory, keyword):
    # Initialize a list to store the paths of found feature classes
    feature_class_paths = []

    # Walk through the directory and its subdirectories
    for dirpath, dirnames, filenames in os.walk(root_directory):
        # Check if the current directory is a file geodatabase
        if dirpath.endswith(".gdb"):
            gdb_path = dirpath

            # Print the geodatabase being searched
            print(f"Searching in geodatabase: {gdb_path}")

            # List all feature classes in the geodatabase
            arcpy.env.workspace = gdb_path
            feature_classes = arcpy.ListFeatureClasses()

            # Check if the keyword is in the feature class names
            matching_feature_classes = [fc for fc in feature_classes if keyword.lower() in fc.lower()]

            # Add matching feature class paths to the result list
            feature_class_paths.extend([os.path.join(gdb_path, fc) for fc in matching_feature_classes])

    return feature_class_paths

if __name__ == "__main__":

    found_feature_classes = search_gdb_feature_class(root_directory, keyword)

    if found_feature_classes:
        print("\n\nFound feature classes:")
        for feature_class in found_feature_classes:
            print(feature_class)
    else:
        print("No matching feature classes found.")
