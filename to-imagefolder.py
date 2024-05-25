import os
import csv

dataDir = input("Enter the directory to the data: ")

with open(f"{ dataDir }/metadata.csv", 'w', newline='') as csv_file:
    # Create the CSV writer
    csv_writer = csv.writer(csv_file)

    # Write all of the CSV fields
    csv_fields = ["file_name", "category", "group", "name", "dimensions", "tags"]
    csv_writer.writerow(csv_fields)
    
    for category in os.listdir(path=dataDir):
        categoryDir = f"{ dataDir }/{ category }"
        # Skip if it isn't a directory
        if not os.path.isdir(categoryDir):
            continue

        for group in os.listdir(path=categoryDir):
            groupDir = f"{ categoryDir }/{ group }"
            # Skip if it isn't a directory
            if not os.path.isdir(groupDir):
                continue

            for build in os.listdir(path=groupDir):
                buildDir = f"{ groupDir }/{ build }"

                metaYmlDir = f"{ buildDir }/meta.yml"
                dataJsonDir = f"{ buildDir }/data.json"
                os.remove(dataJsonDir)

                # Where the build's image is
                imgDir = f"{ buildDir }/data.png"
                if not os.path.isfile(imgDir):
                    os.remove(metaYmlDir)
                    os.rmdir(buildDir)
                    continue

                # Where we're moving it to
                newImgName = f"{ build }.png"
                newImgDir = f"{ dataDir }/{ newImgName }"

                # Moving the build
                os.rename(imgDir, newImgDir)

                # Extract all of the data from the original meta.yml file
                fields = ["name", "dimensions", "tags"]
                metadata = None
                with open(metaYmlDir, 'r') as f:
                    toFind = ": "
                    metadata = [line[line.find(toFind) + len(toFind):].replace('\n', '') for line in f.readlines()]
                    
                csv_writer.writerow([newImgName, category, group, metadata[0], metadata[1], metadata[2]])
                    
                # The original skin directory is no longer needed
                os.remove(metaYmlDir)
                os.rmdir(buildDir)
            os.rmdir(groupDir)
        os.rmdir(categoryDir)