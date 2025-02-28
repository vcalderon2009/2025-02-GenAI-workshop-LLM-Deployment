#!/usr/bin/env python

import os
import shutil


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def remove_dir(filepath):
    shutil.rmtree(os.path.join(PROJECT_DIRECTORY, filepath))


def copy_file(original_filepath, new_filepath):
    shutil.copyfile(
        os.path.join(PROJECT_DIRECTORY, original_filepath),
        os.path.join(PROJECT_DIRECTORY, new_filepath),
    )


PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)

license_files = {
    "Apache Software Licence 2.0": "apache-v2.0.md",
    "BSD 2-Clause": "bsd-2.md",
    "MIT": "mit.md",
    "General": "general.md",
}


def process_licence(licence_name):
    """
    Processes the License file for the document.

    Parameters
    ----------
    licence_name : str
        Name of the License to use.
    """
    if licence_name in license_files:
        shutil.copyfile(
            os.path.join(PROJECT_DIRECTORY, "licenses", license_files[licence_name]),
            os.path.join(PROJECT_DIRECTORY, "LICENSE.rst"),
        )

    #  Remove `licenses` folder
    shutil.rmtree(os.path.join(PROJECT_DIRECTORY, "licenses"))


if __name__ == "__main__":

    process_licence("{{ cookiecutter.open_source_license }}")

    try:
        from git import Repo

        new_repo = Repo.init(PROJECT_DIRECTORY)
        new_repo.git.add(".")
        new_repo.index.commit(
            "Creation of {{ cookiecutter.repo_name }} "
            "from AWS/Terraform/FastAPI template"
        )
    except ImportError:
        print(
            "'gitpython' is not initialized so the repository "
            "will not be initialized!"
        )
