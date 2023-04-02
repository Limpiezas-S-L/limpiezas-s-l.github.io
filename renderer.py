import jinja2
import json
from datetime import datetime, date
from os import listdir, getenv, makedirs, path
from random import choice

# Configuration

template_folder = getenv("TEMPLATE_FOLDER", "templates")
template_default = getenv("TEMPLATE_DAFAULT", "default.html")
template_output = getenv("TEMPLATE_OUTPUT", "public/index.html")
data_file = getenv("DATA_FILE", "data.json")

# Find if there is any birthday today

with open(data_file) as f:
  data = json.loads(f.read())

def is_bday(bday_str, format):
    today = date.today()
    birthday = datetime.strptime(bday_str, format).date().replace(year=today.year)
    return (birthday - today).days == 0

# At the moment it is design without considering multiple people sharing birthday
member = [m for m in data["members"] if is_bday(m["birthday"], "%d/%m") ][0]

# Render the template

template_loader = jinja2.FileSystemLoader(searchpath=template_folder)
environment = jinja2.Environment(loader=template_loader)

template = template_default

if member:
    # This may broke with nested directories inside the template folder
    template_list = listdir(template_folder)
    template_list.remove(template_default)

    template = choice(template_list)

# Make sure the output folder exists
makedirs(path.dirname(template_output), exist_ok=True)

with open(template_output, "w") as f:
    f.write(environment.get_template(template).render(member))
