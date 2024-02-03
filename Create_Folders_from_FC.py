#------------USER INPUTS-----------------------------------------------------
input_feature_class = r''# Input feature class filepath
field_name = r'' # Field name within feature class used to generate folder name
output_folder = r'' # Output base directory for new folders
#------------DO NOT EDIT BELOW THIS LINE---------------------------------------------
print('Importing arcpy, os, time, and subprocess libraries')
import arcpy, os, subprocess, time
print('Import Complete\n')
total_time_start = time.time()

def create_folders(input_feature_class, field_name, output_folder):
    # Check out the ArcGIS Spatial Analyst extension

    # Make sure the output folder exists or create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Use a search cursor to iterate through the features
    with arcpy.da.SearchCursor(input_feature_class, [field_name]) as cursor:
        for row in cursor:
            # Only add a folder if the field is not null
            if row[0] is not None and row[0] != '':
              # Get the value from the specified field
              field_value = row[0]
  
              # Create a folder name based on the field value
              folder_name = str(field_value)

              # Construct the full path for the new folder
              folder_path = os.path.join(output_folder, folder_name)

              # Create the folder if it doesn't exist
              if not os.path.exists(folder_path):
                  os.makedirs(folder_path)

if __name__ == "__main__":
    # Call the function to create folders
    create_folders(input_feature_class, field_name, output_folder)
  
# Open the file explorer to the directory
print(f'opening {output_folder}')
explorer_cmd = f'explorer /select,"{output_folder}"'
subprocess.run(explorer_cmd, shell=True)

total_time_end = time.time()  # Record the end time for the entire process
total_duration = total_time_end - total_time_start

print(f"Done!\nTotal time: {total_duration:.2f} seconds")
