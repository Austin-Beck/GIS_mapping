import arcpy
import os

# Define the input parameters
one_pct_poly = r".shp"
one_pct_zone = 'AE' #AE or A
two_pct_poly = r".shp"
FW_poly = r".shp"
WA_name = "Sand_Creek"  # Example value, replace with the actual name (no spaces/special characters) - this is used for the final fc name

# Create empty list for fcs
fc_list = []


# Set environment settings
arcpy.env.addOutputsToMap = False
arcpy.env.workspace = arcpy.mp.ArcGISProject("CURRENT").defaultGeodatabase
arcpy.env.overwriteOutput = True


print(f'exporting shapefiles to GDB {arcpy.env.workspace} and adding/populating fields..')
if arcpy.Exists(one_pct_poly):
    one_pct_bn = 'one_pct'
    arcpy.conversion.ExportFeatures(one_pct_poly, one_pct_bn)
    arcpy.management.AddFields(one_pct_bn,
                                [['FLD_ZONE', 'TEXT'],
                                ['ZONE_SUBTY', 'TEXT']])
    arcpy.management.CalculateField(one_pct_bn, 'FLD_ZONE', f"'{one_pct_zone}'", "PYTHON3")
    fc_list.append(one_pct_bn)
    
if arcpy.Exists(two_pct_poly):
    two_pct_bn = 'two_pct'
    arcpy.conversion.ExportFeatures(two_pct_poly, two_pct_bn)
    arcpy.management.AddFields(two_pct_bn,
                                [['FLD_ZONE', 'TEXT'],
                                ['ZONE_SUBTY', 'TEXT']])
    arcpy.management.CalculateFields(two_pct_bn, "PYTHON3",
                                    [['FLD_ZONE', "'X'"],
                                    ['ZONE_SUBTY', "'0500'"]])
    fc_list.append(two_pct_bn)
    
if arcpy.Exists(FW_poly):
    FW_bn = 'FW'
    arcpy.conversion.ExportFeatures(FW_poly, FW_bn)
    arcpy.management.AddFields(FW_bn,
                                [['FLD_ZONE', 'TEXT'],
                                ['ZONE_SUBTY', 'TEXT']])
    arcpy.management.CalculateFields(FW_bn, "PYTHON3",
                                [['FLD_ZONE', "'AE'"],
                                ['ZONE_SUBTY', "'1100'"]])
    fc_list.append(FW_bn)
    
def cleanup(fc_list, WA_name):
    to_delete = []
    for fc in fc_list:
        
        to_delete.append(fc)
        print(f'working on {fc}...')
        
        
        # Check spatial reference
        spatial_ref = arcpy.Describe(fc).spatialReference
        if spatial_ref.linearUnitName.lower() not in ['foot', 'international foot', 'survey foot']:
            print(f"{fc} not projected to feet. Quitting.")
            break
        else:
            print(f"{fc} is projected to feet. Continuing...")
        
        
         # Smooth using PAEK with 25 feet tolerance
        smoothed = fc +'_smoothed'
        print('  smothing feature class')
        arcpy.SmoothPolygon_cartography(fc, smoothed, "PAEK", "25 Feet")
        to_delete.append(smoothed)

        # Generalize with 0.5 ft
        print('  generalizing feature class')
        arcpy.Generalize_edit(smoothed, "0.5 Feet")

        # Convert multipart to singlepart
        print('  converting multiparts to single parts')
        single_part = fc + '_singlepart'
        arcpy.MultipartToSinglepart_management(smoothed, single_part)
        to_delete.append(single_part)
        
        # Delete features less than 2,000 sqft
        print('  removing features less than 2000 feet')
        with arcpy.da.UpdateCursor(single_part, ["SHAPE@"]) as cursor:
            for row in cursor:
                if row[0].area < 2000:
                    cursor.deleteRow()
        
        # Eliminate polygon parts less than 2,000 sqft
        elim_poly = fc + '_elim'
        arcpy.management.EliminatePolygonPart(single_part,elim_poly, condition="AREA", part_area="2000 SquareFeet",
                                                  part_area_percent=0, part_option="CONTAINED_ONLY")
        to_delete.append(elim_poly)
    
    
    final_merge = []
    if arcpy.Exists('one_pct_elim') and arcpy.Exists('two_pct_elim'):
        print('erasing 100yr from 500yr..')
        two_pct_erase = 'two_pct_erased'
        arcpy.Erase_analysis('two_pct_elim', 'one_pct_elim', two_pct_erase)
        final_merge = [two_pct_erase]
        to_delete.append(two_pct_erase)
    if arcpy.Exists('FW_elim') and arcpy.Exists('one_pct_elim'):
        print('erasing FW from 100yr..')
        one_pct_erase = 'one_pct_erased'
        arcpy.Erase_analysis('one_pct_elim', 'FW_elim',one_pct_erase)
        final_merge.append(one_pct_erase)
        final_merge.append('FW_elim')
        to_delete.append(one_pct_erase)
    else:
        final_merge.append('one_pct_elim')
        
    print('merging final dataset..')
    arcpy.management.Merge(final_merge, WA_name + '_final')     
        
    arcpy.management.DeleteField(WA_name+'_final',['FLD_ZONE','ZONE_SUBTY'], 'KEEP_FIELDS')
    
    for fc in to_delete:
        arcpy.Delete_management(fc)
        
    print('done')     
        
cleanup(fc_list, WA_name)
