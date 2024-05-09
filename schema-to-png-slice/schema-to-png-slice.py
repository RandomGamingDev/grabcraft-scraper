import glob
import json
from PIL import Image
import yaml

import blockmodel_avg_mapper as bam

builds_location = input("Enter the location the schemas: ")
build_dirs = glob.glob(f"{ builds_location }/*/*/*")

for build_dir in build_dirs:
    print(build_dir)

    render_object = None
    with open(f"{ build_dir }/data.json", "r") as render_object_file:
        render_object = json.load(render_object_file)

    metadata = None
    with open(f"{ build_dir }/meta.yml", "r") as stream:
        try:
            print(yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            print(exc)