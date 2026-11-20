"""Publish the Friday 20 November 2026 front page.

The repository holds one picture, entry.png: a JPEG broadsheet front
page summing up the day's world news. Cyclone Akvan's landfall on the
Odisha coast is the lead story; five panels below it cover Anthropic's
record IPO debut, the COP31 close in Antalya, the Houthi missile
strike on Riyadh, the Hormuz tanker attacks and the Berlin talks on
Russia, with a strip of shorter items along the foot of the page.

Running this module copies that picture, byte for byte, into the
grading output directory. It refuses to publish anything that is not
a complete JPEG inside the one-mebibyte cap, and it checks the copy
against the source by comparing digests, so two runs always write
the same bytes.
"""

import hashlib
import os
import sys
from pathlib import Path

PICTURE_NAME = "entry.png"
MAX_BYTES = 1024 * 1024
JPEG_MAGIC = bytes((0xFF, 0xD8, 0xFF))


def source_picture():
    return Path(__file__).resolve().with_name(PICTURE_NAME)


def output_dir():
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def load_jpeg(path):
    data = path.read_bytes()
    if not data:
        sys.exit(f"{path.name} is empty, refusing to publish it")
    if len(data) > MAX_BYTES:
        sys.exit(f"{path.name} is {len(data)} bytes, over the {MAX_BYTES} cap")
    if data[:3] != JPEG_MAGIC:
        sys.exit(f"{path.name} is not a JPEG")
    return data


def main():
    data = load_jpeg(source_picture())
    dest = output_dir()
    dest.mkdir(parents=True, exist_ok=True)
    target = dest / PICTURE_NAME
    target.write_bytes(data)
    published = load_jpeg(target)
    if len(published) != len(data):
        sys.exit("published copy is not the same size as the source picture")
    if hashlib.sha256(published).digest() != hashlib.sha256(data).digest():
        sys.exit("published copy differs from the source picture")


if __name__ == "__main__":
    main()
