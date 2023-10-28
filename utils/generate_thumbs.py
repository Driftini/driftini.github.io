#!/usr/bin/python3

from os import listdir, path
from textwrap import indent
from PIL import Image

COLLECTIONS = ["artwork", "walls"]
THUMB_SETTINGS = {
    "extension": "jpg",
    "maxsize": (512, 512),
    "quality": 70
}

counters = {
    "saved": 0,
    "failed": 0,
    "skipped": 0
}

for collection in COLLECTIONS:
    pictures_dir = f"src/assets/img/posts/{collection}"
    thumbs_dir = f"{pictures_dir}/thumbs"

    if path.isdir(pictures_dir) and path.isdir(thumbs_dir):
        pictures = listdir(pictures_dir)
        pictures.remove("thumbs")

        for filename in pictures:
            name = filename.split('.')[0]
            source_path = f"{pictures_dir}/{filename}"
            target_path = f"{thumbs_dir}/{name}.{THUMB_SETTINGS['extension']}"

            if not path.isfile(target_path):
                try:
                    with Image.open(source_path) as i:
                        i.thumbnail(THUMB_SETTINGS["maxsize"])
                        i.save(
                            target_path,
                            quality=THUMB_SETTINGS["quality"],
                            optimize=True,  # for JPEG
                            method=6       # for WebP
                        )
                        
                        print(f"{name} saved.")
                        counters["saved"] += 1
                except Exception as e:
                    print(f"{name} failed:")
                    print(indent(str(e), "  "))
                    counters["failed"] += 1
            else:
                print(f"{name} skipped, thumbnail already exists.")
                counters["skipped"] += 1

    else:
        print("This script must be run from the repo's root.")
        exit(1)

print("Done!")
print(f"Successful: {counters['saved']}")
print(f"Skipped: {counters['skipped']}")
print(f"Failed: {counters['failed']}")