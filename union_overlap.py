# working script. finds overlap from a list of input polygons.
# basically works like the intersect tool, but ouptuts any features that intersect rather than an output of intersections among all outputs.

#INPTUS
output_folder = r'C:\adb_ble_outputs\delete'
union_output = os.path.join(output_folder, "mesh_union.shp")
feature_list = ["Dissolve_selected_cell_polygons4",
                "Dissolve_selected_cell_polygons3",
                "Dissolve_selected_cell_polygons2",
                "Dissolve_selected_cell_polygons1"]


print("  Finding all overlap areas between meshes...")
# Union keeps all features and shows where any overlap
arcpy.analysis.Union(
    in_features=feature_list,  # Your list of dissolved work areas
    out_feature_class=union_output,
    join_attributes="ONLY_FID",
    gaps="NO_GAPS"
)

# Get all FID fields from union
fid_fields = [f.name for f in arcpy.ListFields(union_output) if f.name.startswith("FID_")]

# Add overlap count field
arcpy.management.AddField(union_output, "OL_COUNT", "SHORT")

# Use UpdateCursor to count non -1 values in each row
with arcpy.da.UpdateCursor(union_output, fid_fields + ["OL_COUNT"]) as cursor:
    for row in cursor:
        # Count how many FID fields are >= 0 (not -1)
        overlap_count = sum(1 for fid in row[:-1] if fid >= 0)
        row[-1] = overlap_count  # Set OVERLAP_COUNT field
        cursor.updateRow(row)

print("  Overlap count calculated")


# Filter to only areas where 2+ meshes overlap
overlap_final = os.path.join(output_folder, "mesh_overlaps_only")
arcpy.analysis.Select(
    union_output,
    overlap_final,
    "OL_COUNT >= 2"   
)

print(f"  Overlap areas found: {overlap_final}")
