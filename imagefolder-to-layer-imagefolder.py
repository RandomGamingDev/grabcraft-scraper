import os
import json

from PIL import Image
import pandas as pd

#data_dir = input('Enter the directory to the data: ')
data_dir = "grabcraft-builds-png-slices"

metadata_dir = f"{ data_dir }/metadata.csv"
metadata_df = pd.read_csv(metadata_dir)

out_data = []
for i, row in metadata_df.iterrows():
	# Get fields
	file_name = row["file_name"]
	category = row["category"]
	group = row["group"]
	name = row["name"]
	dimensions = row["dimensions"]
	tags = row["tags"]

	# Parse some of the fields for their data
	img_dir = f"{ data_dir }/{ file_name }"
	if not os.path.isfile(img_dir): # Skip detected duplicates
		continue
	img = Image.open(img_dir)
	os.remove(img_dir)
	build_height = json.loads(dimensions)[1]
	layer_width = img.width / build_height

	# Write the rows for each layer
	for y in range(build_height):
		# Get the differing data between the png slice and layer image
		layer_name = f"{ file_name[:file_name.find('.')] } (Layer { y }).png"
		layer_dir = f"{ data_dir }/{ layer_name }"
		layer_img = img.crop((y * layer_width, 0, (y + 1) * layer_width, img.height))
		layer_img.save(layer_dir)

		# Append the data to be converted to a DataFrame later
		out_data.append([layer_name, category, group, name, dimensions, tags, y])

# Save the DataFrame
out_df = pd.DataFrame(out_data, columns=[*metadata_df.columns, "layer"])
out_df.to_csv(metadata_dir, index=False)