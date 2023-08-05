#!/usr/bin/env python
# update_sphinx_conf.py
# Copyright (c) 2018-2019 Pablo Acosta-Serafini
# See LICENSE for details
# pylint: disable=C0111,C0413,E1101,F0401,R0914,W0141

# Standard library imports
import datetime
import os
import re
import sys
PKG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(PKG_DIR, "pytest_pmisc"))
# Intra-package update
import version


###
# Functions
###
def update_conf():
    """Update Sphinx conf.py file."""
    # pylint: disable=W0122,W0612
    __version__ = version.__version__
    year = datetime.datetime.now().year
    fname = os.path.join(PKG_DIR, "docs", "conf.py")
    regexp = re.compile(".*2018-(\\d\\d\\d\\d), Pablo Acosta-Serafini")
    with open(fname, "r") as fobj:
        lines = [item.rstrip() for item in fobj.readlines()]
        ret = []
        for line in lines:
            rmatch = regexp.match(line)
            if rmatch:
                file_year = int(rmatch.group(1))
                template = "2018-{0}, Pablo Acosta-Serafini"
                line = line.replace(template.format(file_year), template.format(year))
                ret.append(line)
            elif line.startswith("version = "):
                tokens = ["a", "b", "rc"]
                index = max([__version__.find(item) for item in tokens])
                short_version = __version__
                if index > -1:
                    short_version = __version__[:index]
                ret.append("version = '{0}'".format(short_version))
            elif line.startswith("release = "):
                ret.append("release = '{0}'".format(__version__))
            else:
                ret.append(line)
        with open(fname, "w") as fobj:
            fobj.write("\n".join(ret))


if __name__ == "__main__":
    update_conf()
