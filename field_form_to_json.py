from arcgis.gis import GIS
import json
import os

def export_field_form(webmap_id, layer_name, output_path):
    """
    Export a layer's field form configuration to JSON.
    
    Parameters:
    webmap_id (str): The item ID of the webmap
    layer_name (str): Name of the layer to export the form from
    output_path (str): Path to save the JSON file (directory or full file path)
    """
    try:
        # Connect to ArcGIS Online using 'home'
        gis = GIS('home')
        print(f"Connected to: {gis.url}")
        print(f"Logged in as: {gis.properties.user.username}")
        
        # Get the webmap item
        print(f"\nRetrieving webmap with ID: {webmap_id}")
        webmap_item = gis.content.get(webmap_id)
        
        if webmap_item is None:
            print(f"Error: Could not find item with ID {webmap_id}")
            return None
        
        # Get the webmap data
        webmap_data = webmap_item.get_data()
        
        # Find the layer
        target_layer = None
        
        print(f"\nSearching for layer '{layer_name}' in webmap...")
        print(f"Available layers:")
        
        for layer in webmap_data.get('operationalLayers', []):
            layer_title = layer.get('title', 'Unnamed')
            print(f"  - {layer_title}")
            
            if layer_title == layer_name:
                target_layer = layer
        
        # Check if layer was found
        if target_layer is None:
            print(f"\nError: Layer '{layer_name}' not found in webmap")
            return None
        
        print(f"\nFound layer: {layer_name}")
        
        # Check if layer has a form
        if 'formInfo' not in target_layer:
            print(f"\nError: Layer '{layer_name}' does not have a form configured")
            return None
        
        # Get the form configuration
        form_config = target_layer['formInfo']
        print(f"Form configuration found!")
        
        # Determine output file path
        if os.path.isdir(output_path):
            # If it's a directory, create filename in that directory
            output_file = os.path.join(output_path, f"{layer_name.replace(' ', '_')}_form.json")
        else:
            # Use as full file path
            output_file = output_path
        
        # Ensure the output path has .json extension
        if not output_file.endswith('.json'):
            output_file += '.json'
        
        # Create directory if it doesn't exist
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Write JSON to file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(form_config, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Field form successfully exported!")
        print(f"Output: {os.path.abspath(output_file)}")
        
        return form_config
        
    except Exception as e:
        print(f"\nError exporting field form: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    # Inputs
    webmap_id = '0ebb035fb72748cfaa601591f9cb2ed0'
    layer_name = 'NHA Structures'
    output_path = r'C:\adb_ble_outputs\nha'
    
    # Export the field form
    export_field_form(webmap_id, layer_name, output_path)
