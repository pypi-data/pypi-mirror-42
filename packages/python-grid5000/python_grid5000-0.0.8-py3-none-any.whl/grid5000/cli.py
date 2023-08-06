import os

from grid5000 import Grid5000

import IPython


def main():
    
    conf_file = os.path.join(os.environ.get("HOME"), ".python-grid5000.yaml")
    gk = Grid5000.from_yaml(conf_file)

    IPython.embed()
