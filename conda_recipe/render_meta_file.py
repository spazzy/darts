from pathlib import Path
import os

PACKAGE = 'darts'
DIR = os.path.join(Path(__file__).parent.absolute(), PACKAGE)
REQS_DIR = os.path.join(Path(__file__).parent.absolute(), '..', 'requirements')
REQ_FILES = ['core.txt', 'pmdarima.txt', 'torch.txt', 'prophet.txt']
IN_FILE = 'meta-template.yaml'
OUT_FILE = 'meta.yaml'


def read_requirements(fname):
    return list(Path(os.path.join(REQS_DIR, fname)).read_text().splitlines())


reqs_list = [read_requirements(fname) for fname in REQ_FILES]
all_reqs = [item for sublist in reqs_list for item in sublist]

reqs_string = '- ' + '\n    - '.join(all_reqs)
# replace packages by conda-forge equivalents
reqs_string = reqs_string.replace('torch', 'pytorch').replace('matplotlib', 'matplotlib-base')
# add space in front of >=
reqs_string = reqs_string.replace('>=', ' >=')


# read meta-template.yaml and write to meta.yaml, filling in our dependencies
with open(os.path.join(DIR, IN_FILE), 'r') as in_file:
    with open(os.path.join(DIR, OUT_FILE), 'w') as out_file:
        for in_line in in_file:
            out_file.write(in_line.replace('%%%', reqs_string))
