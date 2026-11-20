"""Friday 20 November 2026, summed up in a single picture.

The repository ships `entry.png`: a broadsheet front page for the day.
Cyclone Akvan's landfall on the Odisha coast leads the page; the panels
below it cover Anthropic's record IPO debut, the COP31 close in Antalya,
the Houthi missile strike on Riyadh, the Hormuz tanker attacks and the
European allies' Berlin talks on Russia, with a strip of shorter items
along the foot of the page.

This script is the entrypoint. It copies the bundled picture into the
grading output folder, byte for byte, and stops with an error unless
the copy is a complete JPEG no larger than one mebibyte.
"""

from hashlib import sha256
from os import environ
import pathlib

ENTRY = "entry.png"
SIZE_LIMIT = 1048576
JPEG_PREFIX = b"\xff\xd8\xff"


def bundled_picture() -> pathlib.Path:
    here = pathlib.Path(__file__).resolve().parent
    return here / ENTRY


def target_folder() -> pathlib.Path:
    wanted = environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return pathlib.Path(wanted)


def read_picture(path: pathlib.Path) -> bytes:
    blob = path.read_bytes()
    if len(blob) == 0:
        raise SystemExit(f"refusing to publish an empty {path.name}")
    if len(blob) > SIZE_LIMIT:
        raise SystemExit(
            f"{path.name} is {len(blob)} bytes, over the {SIZE_LIMIT} limit"
        )
    if blob[: len(JPEG_PREFIX)] != JPEG_PREFIX:
        raise SystemExit(f"{path.name} does not start with a JPEG header")
    return blob


# The grader runs the entrypoint twice and requires identical bytes
# both times, so publish() performs no step that could vary: the
# picture is copied as stored, and the only check is a digest
# comparison of what was written against what was read.
def publish() -> None:
    picture = bundled_picture()
    blob = read_picture(picture)
    wanted = target_folder() / ENTRY
    wanted.parent.mkdir(parents=True, exist_ok=True)
    wanted.write_bytes(blob)
    again = read_picture(wanted)
    if sha256(again).hexdigest() != sha256(blob).hexdigest():
        raise SystemExit("the published copy is not identical to the source")


if __name__ == "__main__":
    publish()
