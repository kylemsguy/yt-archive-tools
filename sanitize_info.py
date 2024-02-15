import os
import glob
import json

fields_to_purge = [
    "formats",
    "thumbnails",
    "automatic_captions",
]

files = glob.glob("*.info.json")

for f in files:
    with open(f) as infile:
        meta = json.load(infile)

    sanitized_meta = {
        k: v for k, v in meta.items() if k not in fields_to_purge
    }

    if not os.path.isdir("sanitized"):
        os.mkdir("sanitized")

    with open(os.path.join("sanitized", f), 'w') as outfile:
        json.dump(sanitized_meta, outfile, indent=4)
