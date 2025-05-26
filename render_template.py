from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import json


def render_template(filename):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template(filename)

    storage_path = Path("storage/data.json")
    if filename == "read.html" and storage_path.exists():
        with open(storage_path, "r", encoding="utf-8") as f:
            messages = json.load(f)
    else:
        messages = {}

    output = template.render(messages=messages, active_page=filename)

    with open(filename, "w", encoding="utf-8") as fh:
        fh.write(output)
