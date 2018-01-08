from flask import Flask
from pathlib import Path
from mistletoe import Document, HTMLRenderer
app = Flask(__name__)


@app.route("/<path:path>")
def which_file_type(path):
    path = normalize_filename(path)
    with open(path, 'r') as fin:
        with HTMLRenderer() as renderer:
            return renderer.render(Document(fin))


def normalize_filename(path):
    path = Path(path).resolve()
    cwd = Path.cwd().resolve()
    if cwd not in path.parents:
        raise Exception("Naughty, trying to look where you aren't supposed to...")
    if path.exists():
        return path
    if path.suffix == "":
        for suffix in [".md", ".markdown"]:
            if path.with_name(path.name + suffix).exists():
                return path.with_name(path.name + suffix)
        else:
            raise Exception("No path with that name found")
