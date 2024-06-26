import requests
import os
import grabcraft_to_schema as gts

def safe_mkdir(directory):
    if not os.path.isdir(directory):
        os.mkdir(directory)

# Load the blockmap csv (This contains manually made block mappings)
gts.load_block_map("blockmap.csv")

# The URL to the site we're scraping
site_link = "https://www.grabcraft.com"
# Get the site's content
site_res = requests.get(site_link).text

# Where the scraped data will go
builds_dir = "grabcraft-builds"
safe_mkdir(builds_dir)

# Get the menu containing all of the different sections
menu_header = "<div class=\"secondary-menu-wrap menu-wrap\"  id=\"secondary-menu-wrap\""
menu_tail = "</div>"
menu_start = site_res.find(menu_header)
menu_end = site_res.find(menu_tail, menu_start)
menu = site_res[menu_start:menu_end]

# The sections of the menu
section_header = "<li class=\"cats-"
# All sections (sections and subsections are on the same layer of the list)
all_sections = menu.split(section_header)
# Remove the first element which is useless
all_sections.pop(0)
# The current section (not subsection)
section_dir = None
# Organize the sections into subsections and sections
for section in all_sections:
    # Getting the level of a section in the table
    level_header = "level_"
    level_start = section.find(level_header) + len(level_header)
    level_end = level_start + 1
    level = int(section[level_start:level_end])

    # Variables for getting suburls
    suburl_header = "href=\"/minecraft/"
    suburl_tail = '\"'

    # Getting the subdirectory name of the section for the website
    subsuburl_start = section.find(suburl_header) + len(suburl_header)
    subsuburl_end = section.find(suburl_tail, subsuburl_start)
    subsuburl = section[subsuburl_start:subsuburl_end]
    
    # Switch the section if it's a section and not a subsection
    if level == 1:
        # Get & make the directory for the section
        section_dir = f"{ builds_dir }/{ subsuburl }"
        safe_mkdir(section_dir)
        print(f"Scraping section { subsuburl } into { section_dir }!")
        continue
    
    # Get & make the directory for the subsection
    subsection_dir = f"{ section_dir }/{ subsuburl }"
    safe_mkdir(subsection_dir)

    # Get the subdirectory's page
    suburl = f"{ site_link }/minecraft/{ subsuburl }"
    subsection_res = requests.get(suburl).text

    # Print progress
    print(f"\tScraping subsection { subsuburl } from { suburl } into { subsection_dir }!")

    # Get the number of pages of the subdirectory from the to last button
    # Get the button
    to_last_button_header = "<li class=\"last\">"
    to_last_button_start = subsection_res.find(to_last_button_header)

    # Get the number of pages
    num_pages_header = "/pg/"
    num_pages_start = subsection_res.find(num_pages_header, to_last_button_start) + len(num_pages_header)
    num_pages = None # The value will be determined in the following statements
    if num_pages_start == -1 + len(num_pages_header):
        num_pages = 1
    else:
        num_pages_end = subsection_res.find(suburl_tail, num_pages_start)
        num_pages = int(subsection_res[num_pages_start:num_pages_end])

    for i in range(1, num_pages + 1):
        # Get the page (We refetch the first page just in case grabcraft changes how they display things by default)
        subpage_url = f"{ suburl }/pg/{ i }"
        subpage_res = requests.get(subpage_url).text

        # Get the build's image and then get the link from that
        # Get the image
        image_header = "<img src=\""
        subpage_split_image = subpage_res.split(image_header)
        subpage_split_image.pop(len(subpage_split_image) - 1)
        # Extract the link from the image
        for subpage_split in subpage_split_image:
            # Get the build's link
            a_href_header = "<a href=\""
            build_link_start = subpage_split.rfind(a_href_header) + len(a_href_header)
            build_link_end = subpage_split.find(suburl_tail, build_link_start)
            build_sub_link = subpage_split[build_link_start:build_link_end]
            build_link = f"{ site_link }{ build_sub_link }"
            # Get the build's link name
            build_link_name_header = '/minecraft/'
            build_link_name_tail = '/'
            build_link_name_start = build_sub_link.find(build_link_name_header) + len(build_link_name_header)
            build_link_name_end = build_sub_link.find(build_link_name_tail, build_link_name_start)
            build_link_name = build_sub_link[build_link_name_start:build_link_name_end]
            
            # Create the directory for containing the build
            build_dir = f"{ subsection_dir }/{ build_link_name }"
            safe_mkdir(build_dir)
            print(f"\t\tScraping build { build_link_name } from { build_link } into { build_dir }!")

            # Get the schema
            render_object = gts.url_to_render_object_data(build_link)
            # The RenderObject.obj converted from a javascript variable to a json string
            ro_json = render_object.obj[render_object.obj.find('{'):]
            # Write the RenderObject json
            with open(f"{ build_dir }/data.json", 'w') as f:
                f.write(ro_json)
            # Write the RenderObject's attributes/metadata as a txt formatted as a yml
            with open(f"{ build_dir }/meta.yml", 'w') as f:
                f.write(f"name: { render_object.name }\n")
                f.write(f"dims: { list(render_object.dims) }\n")
                f.write(f"tags: { list(render_object.tags) }\n")