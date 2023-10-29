import requests
import shutil
import os
from litemapy import Schematic, Region, BlockState
import json
import csv

block_map = {}

# Load the block map of predefined blocks
def load_block_map(file_name):
    global block_map

    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            i += 1
            if i == 0:
                continue
            block_map[row[1]] = row[2:]

# Automatically map grabcraft blocks to schema blocks
def auto_block_map(grabcraft_block):
    # Set the schema_block to grabcraft_block so that it's ready for later transformations
    schema_block = grabcraft_block
    # Remove the parenthesis
    parenthesis_loc = schema_block.find(" (")
    if parenthesis_loc != -1:
        schema_block = schema_block[:parenthesis_loc]
    # Make all of the characters lowercase like in vanilla Minecraft block codes
    schema_block = schema_block.lower()
    # Replace all spaces with _ like in vanilla Minecraft block codes
    schema_block = schema_block.replace(' ', '_')
    # Replace some weird formatting regarding wood items
    schema_block = schema_block.replace("_wood_", '_')

    return f"minecraft:{ schema_block }"

class RenderObject:
    def __init__(self, obj, name, dims, tags):
        self.obj = obj 
        self.name = name
        self.dims = dims
        self.tags = tags

def render_object_to_schema(render_object):
    global block_map

    # Get the part of the javascript containing the JSON
    ro_text = render_object.obj[render_object.obj.find('{'):]
    # Convert it to a json
    ro_json = json.loads(ro_text)

    # Store the dimensions
    dims = render_object.dims
    # Create the schema
    reg = Region(0, 0, 0, dims[0], dims[1], dims[2])
    schem = reg.as_schematic(name="idk", author="rgd", description="test")
    # Move the blocks from the render object to the region
    for x, yz in ro_json.items():
        for y, z in yz.items():
            for _, data in z.items():
                block_loc = (int(data['x']) - 1, int(data['y']) - 1, int(data['z']) - 1)
                grabcraft_block = data["name"]
                schema_block = None
                if grabcraft_block in block_map:
                    schema_block = block_map[grabcraft_block][0]
                else:
                    schema_block = auto_block_map(grabcraft_block)
                block = BlockState(schema_block)  # get the attributes
                reg.setblock(block_loc[0], block_loc[1], block_loc[2], block)
    return schem

# Get the url to the render object from the webpage for the build
def url_to_render_object_data(url):
    # Getting the webpage itself
    res = requests.get(url).text

    # The index for the renderObject's info
    render_object_i = res.find("myRenderObject")
    # The end index for getting the renderObject's string
    render_object_e = res.find('"', render_object_i)
    # Store the url to the render object
    render_object_url = "https://www.grabcraft.com/js/RenderObject/" + res[render_object_i:render_object_e]

    # Get the index for the name
    name_i = res.find("content-title")
    name_i = res.find(">", name_i) + 1
    # Get the end index for the name
    name_e = res.find("<", name_i)
    # Get the name
    name = res[name_i:name_e]

    # Get the index for the table containing the dimensions and tags
    table_i = res.find("object_properties")
    # Get the metadata
    rows = ("Width", "Height", "Depth", "Tags")
    meta = []
    for row in rows:
        # Get the row
        row_i = res.find(row, table_i)
        # Get the index for the value
        value_i = res.find('>', res.find("value", row_i)) + 1
        # Get the end index for the value
        value_e = res.find('<', value_i)
        # Get the value
        val = res[value_i:value_e]
        # If the value is a list split it to represent it as such
        if val.isdigit():
            val = int(val)
        elif val.find(", ") != -1:
            val = val.split(", ")
        # Add the values to the values list
        meta.append(val)
    tags = tuple(meta.pop())
    dims = tuple(meta)

    return RenderObject(requests.get(render_object_url).text, name, dims, tags)

# Convert the url to a schema file
def url_to_schema(url):
    # Make sure that the url is for the general section
    url = url[:url.find('#')] + "#general"

    # Get the render object, its dimensions, the tags, the name, and the data itself from the url
    render_object = url_to_render_object_data(url)

    # Get the dimensions and tags
    return render_object_to_schema(render_object) # do this with all of the data that we've gotten

#load_block_map("blockmap.csv")
#schem = url_to_schema("https://www.grabcraft.com/minecraft/gothic-medieval-church/churches#model3d")
# Save the schema
#schem.save("test.litematic")
