# Batch Exporst all Layouts in an APRX
# This script was designed to be run within the notebook of the APRX you want to export out of

import arcpy, os

# Where outputs will go
pdf_export = r'Z:\Denver-USDEN06\DCS\Projects\WTR\60680844_BAG_2022_EoR_Support\400_Technical\450_Photos\GIS\PDFs\2023'
# Resolution of Export, 300 is recommended. FEMA standard is 400
res = 300
# Optional. Only export layouts with this word in it. ex: '2023'
keyword = '2023_Q4'
# Optional. Append word to the end of the export. ex: '_draft'
append_name = ''


project = arcpy.mp.ArcGISProject("CURRENT")

for layout in project.listLayouts(f'{keyword}*'):
    pdf_name = f"{layout.name}{append_name}.pdf"
    pdf_path = os.path.join(pdf_export, pdf_name)
    layout.exportToPDF(out_pdf=pdf_path,
                       resolution=300, image_compression='JPEG2000'
                      )
    print(f"Exported layout '{layout.name}' to '{pdf_path }'\n")
