#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil


def proj_requirements():
    """
    Tries to import the necessary packages.

    Parameters
    -----------
    pkg : `str`
        Name of the package to install
    """
    #  Project directory
    PROJECT_DIRECTORY = os.path.relpath(os.path.curdir)

    #  Reading in list of packages
    reqfile = os.path.join(PROJECT_DIRECTORY, "requirements_pre.txt")

    #  Dictionary for necessary requirements
    req_arr = [
        "click",
        "coverage",
        "awscli",
        "flake8",
        "python-dotenv>=0.5.1",
        "gitpython",
        "sphinx>=1.6",
        "configparser",
        "pytest",
    ]

    #  Saving to file
    with open(reqfile, "w") as req_f:
        for item in req_arr:
            req_f.write("{0}\n".format(item))

    #  Checking that file exists
    if not (os.path.exists(reqfile)):
        msg = "`reqfile` ({0}) was not found!".format(reqfile)
        raise ValueError(msg)

    return reqfile


def main():
    """
    Making sure packages are installed before running cookiecutter.
    """
    #  Pip package
    try:
        import pip
    except ImportError:
        msg = "`pip` must be installed first. Please install this beforehand!"
        raise ImportError(msg)

    #  Reading in list of packages
    reqfile = proj_requirements()

    #  Running `install requirements.txt`
    try:
        os.system("pip -q install -r {0}".format(reqfile))
    except:
        msg = "Could not install requirements!!"
        raise ValueError(msg)


if __name__ == "__main__":
    main()
