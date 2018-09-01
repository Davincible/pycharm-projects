# just too lazy to delete duplicate files myself

import os
import json
import re

def delete_files(path):
    regex = r'(\([1-9]\))'
    compiled = re.compile(regex)

    dicts = list(os.walk(path))
    for dict in dicts:
        path_ = os.path.join(path, dict[0])
        files = dict[2]
        for file in files:
            if compiled.findall(file):
                os.remove(os.path.join(path_, file))
                print("removed '{}'".format(file))

delete_files('F:\\Mega\\GG - 2')