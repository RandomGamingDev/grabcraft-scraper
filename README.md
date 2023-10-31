# grabcraft-scraper
A little Python script made for scraping data from grabcraft, which can then be used for things like machine learning and data analysis projects and can be transformed to litematica files with https://github.com/RandomGamingDev/grabcraft-to-schema (Sadly, I can't release the dataset since you aren't allowed to share downloaded content)

Download the requirements from `requirements.txt`
This library uses https://github.com/RandomGamingDev/grabcraft-to-schema for downloading the render objects, although converting them to litematica files will have to be done manually on your part, since this library tries to preserve as much of the core of the data as possible, and the conversion from grabcraft's custom javascript format called `RenderObject`s to litematica is currently lossy since it doesn't preserve things like block states.

This project should be called by running `python scraper.py` will put all of the builds in a directory called `grabcraft-builds` next to it. <br/>
The structure is organized from `grabcraft-builds` like this: `<section>/<subsection>/<build name>` with `data.json` and `meta.yml` in the end directory. <br/>
`data.json` contains the actual render object itself
`meta.yml` contains some important meta data that can be used which are the `name`, `dimensions`, and `tags`. (Other data can be easy obtained by editing the underlying library for getting the `RenderObject` and its metadata and the script for scraping the data)

Note: This library is synchronous partially so that we don't cause the website to block us, and partially because I don't really need the speed, so I didn't feel like adding those extra optimizations. However you're welcome to add things like async/await or multithreading and send a pull request if you'd be interested :D
