from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import json


def render_messages():
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("messages.html")

    storage_path = Path("storage/data.json")
    if storage_path.exists():
        with open(storage_path, "r", encoding="utf-8") as f:
            messages = json.load(f)
    else:
        messages = {}

    output = template.render(messages=messages)

    with open("messages.html", "w", encoding="utf-8") as fh:
        fh.write(output)
