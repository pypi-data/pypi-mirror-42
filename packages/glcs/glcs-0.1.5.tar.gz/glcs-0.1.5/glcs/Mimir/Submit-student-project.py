"""Submit-project-project class"""
import subprocess
from pathlib import Path
import json

def get_professor_config():
    if course_config_exists():
        config_path = Path.home() / 'GitUtils' / 'gitutils' / 'gitutils' / 'Mimir' / ('Config-file.cfg')
        options = {}
        with open(config_path) as config_file:
            options = json.load(config_file)
        return options

    return None

def course_config_exists():
    config_path = Path.home() / 'GitUtils' / 'gitutils' / 'gitutils' / 'Mimir' / ('Config-file.cfg')
    if Path(config_path).exists():
        return True
    else:
        return False

config_file = get_professor_config()
email = config_file["professor_email"]
psswd = config_file["professor_psswd"]
input_string = bytearray(email + "\n" + psswd, 'utf-8')
print(input_string)
process = subprocess.Popen(["mimir", "login"], stdin=subprocess.PIPE)
process.stdin.write(input_string)
