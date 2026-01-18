import os
import shutil
from config import MAPPING_FILENAME


def load_mapping(folder):
    path = os.path.join(folder, MAPPING_FILENAME)
    rules = {}
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line:
                    src, out = line.strip().split("=", 1)
                    rules[src.strip()] = out.strip()
    except:
        return None
    return rules


def process_files(source, output, rules):
    count = 0
    for file in os.listdir(source):
        if file.lower().endswith(".png") and file in rules:
            src_file = os.path.join(source, file)
            out_file = os.path.join(output, rules[file])
            shutil.copy(src_file, out_file)
            count += 1
    return count