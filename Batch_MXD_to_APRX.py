# Created by Austin Beck | austin.beck@aecom.com

# This script takes an input of a folder "Directory Path" and converts all mxds within that folder into an ArcGIS Pro Project (.aprx)

# Intended to be run in an arcgis pro notebook (but not in the project/arpx that you are copying the files into(the aprx_file_path variable))
# use just a blank aprx with no exists maps/layouts instead


#------------USER INPUTS-----------------------------------------------------

# Base directory where MXDs are located
directory_path = r"L:\DCS\Projects\Western Zirconium\GIS\Plant Area Monitoring\2023\Spring_2023"

#Output Path for APRX - will create an APRX is this file doesn't already exist
aprx_file_path = r"L:\DCS\Projects\Western Zirconium\GIS\Plant Area Monitoring\2023\Spring_2023\Pro\WZ_Spring_2023.aprx"

#------------DO NOT EDIT BELOW THIS LINE---------------------------------------------


print('Importing arcpy, os, and time libraries')
import arcpy, os, time
print('Import Complete\n')
total_time_start = time.time()

def create_aprx(aprx_file_path):
    # Create a new ArcGIS Pro project
    aprx = arcpy.mp.ArcGISProject("CURRENT")
    
    # Save the new project to the specified path
    aprx.saveACopy(aprx_file_path)
    del aprx

def import_mxd_to_aprx(aprx_path, directory_path):
    # Open the ArcGIS Pro project
    aprx = arcpy.mp.ArcGISProject(aprx_path)
    

    print("Importing MXDs into Pro..")
    for filename in os.listdir(directory_path): # Iterate through files in the directory
        if filename.endswith(".mxd"):
            mxd_path = os.path.join(directory_path, filename)
            
            print(f"  Importing document: {filename}")
            
            # Create a new layout in the ArcGIS Pro project
            layout = aprx.importDocument(mxd_path)

            # Set layout name to match MXD file name
            layout.name = filename[:-4]  # Remove the ".mxd" extension from the filename
            
            # Save the changes to the ArcGIS Pro project
            aprx.save()
            print(f"  Document imported: {filename}")
            
            
    print("\nChanging map names to match layout name")
    lyts = aprx.listLayouts() # Create list of layouts
    for lyt in lyts: # Iterate through layouts
        
        lyt_name = lyt.name # used to create new map names
        largest_map_frame = 0 # set to 0 at each iteration to find largest map in each layout
        i = 2 #used to name maps other than the layout
        
        maps = lyt.listElements("mapframe_element") # get list of maps used in the layout
        
        for map_object in maps: # find the largest map in the current layout      
            map_object_area = map_object.elementHeight * map_object.elementWidth                
            if map_object_area > largest_map_frame: #compare to previous layout size
                largest_map_frame = map_object_area 
                largest_map_name = map_object # reassign varaible if map is larger

        for map_object in maps: # reiterate through the maps to change names

            if map_object == largest_map_name:
                map_object.name = f"{lyt_name}_main"
                map_object.map.name = f"{lyt_name}_main"
            else:
                map_object.name = f"{lyt_name}_{i}"
                map_object.map.name = f"{lyt_name}_{i}"
                i += 1

            # Save the changes to the ArcGIS Pro project
            aprx.save()

        print(f"  Changed map names in {lyt_name}")
            
            

    # Save changes and close the ArcGIS Pro project
    aprx.save()
    del aprx

# Check if the .aprx file exists, if not, create a new project
if not os.path.exists(aprx_file_path):
    print("Creating new .aprx file...")
    create_aprx(aprx_file_path)


# Call the function to import the MXD files as layouts in the .aprx project
import_mxd_to_aprx(aprx_file_path, directory_path)

total_time_end = time.time()  # Record the end time for the entire process
total_duration = total_time_end - total_time_start

print(f"Done!\nTotal time: {total_duration:.2f} seconds")
