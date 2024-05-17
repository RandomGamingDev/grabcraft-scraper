import glob
import json
from PIL import Image
import yaml

import blockmodel_avg_mapper as bam
import grabcraft_to_schema as gts

builds_location = input("Enter the location the schemas: ")
build_dirs = glob.glob(f"{ builds_location }/*/*/*")

for build_dir in build_dirs:
    render_object_json = None
    with open(f"{ build_dir }/data.json", "r") as render_object_file:
        try:
            render_object_json = render_object_file.read()
            if render_object_json.find("{") == -1:
                continue
        except Exception as exc:
            print(exc)
            continue

    metadata = None
    with open(f"{ build_dir }/meta.yml", "r") as stream:
        try:
            metadata = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            continue

    render_object = gts.RenderObject(render_object_json, metadata["name"], metadata["dims"], metadata["tags"])
    gts.render_object_to_png_slice(render_object).save(f"{ build_dir }/data.png")