# Created by Austin Beck | austin.beck@aecom.com
# Batch Exporst all Layouts in an APRX

#------------USER INPUTS-----------------------------------------------------

# Where outputs will go
pdf_export = r'L:\DCS\Temporary\austin_beck\BVG\Fillmore\APRX\Exports\testing'
# Resolution of Export, 300 is recommended. FEMA standard is 400
res = 300
# Optional. Only export layouts with this word in it. ex: '2023' (this is case senstive)
keyword = 'Figure'
# Optional. Append something to the end of the layout name. ex: append_name = '_draft' would produce 'layoutname_draft.pdf'
append_name = '_testing'
# Optional. The filepath to the .aprx you want to export from. Leave as '' if you are running this in the APRX you are exproting from
APRX_path = ''

#------------DO NOT EDIT BELOW THIS LINE---------------------------------------------


print('Importing arcpy, os, time, and subprocess libraries')
import arcpy, os, subprocess, time
print('Import Complete\n')
total_time_start = time.time()

# Open the file explorer to the directory
explorer_cmd = f'explorer /select,"{pdf_export}"'
subprocess.run(explorer_cmd, shell=True)

if not APRX_path == '':
    project = arcpy.mp.ArcGISProject(APRX_path)
else:
    project = arcpy.mp.ArcGISProject("CURRENT")

for layout in project.listLayouts(f'{keyword}*'):
    loop_start_time = time.time()
    pdf_name = f"{layout.name}{append_name}.pdf"
    pdf_path = os.path.join(pdf_export, pdf_name)
    layout.exportToPDF(out_pdf=pdf_path,
                       resolution=300, image_compression='JPEG2000'
                      )
    loop_end_time = time.time()  # Record the end time for each loop iteration
    loop_duration = loop_end_time - loop_start_time
    print(f"Exported layout '{layout.name}' in {loop_duration:.2f} seconds\n")

total_time_end = time.time()  # Record the end time for the entire process
total_duration = total_time_end - total_time_start

print(f"Done!\nTotal time: {total_duration:.2f} seconds")
