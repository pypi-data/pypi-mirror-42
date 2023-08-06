""" GitHub Repo Managment

Related to downloading and updating GitHub repos. See
the 'assn1' script in bin/assn1 to handle get and update
features.
"""
import logging
import os
import subprocess

logger = logging.getLogger(__name__)

def read_repos(fpath: str) -> list:
    """ Read list of repos from disk """
    try:
        with open(fpath, "r") as infile:
            data = infile.readlines()

        data = [i.strip() for i in data]
        return data

    except FileNotFoundError:
        logger.error("File not found: {}".format(fpath))
        return []

def create_parent_dir(repo_name: str, dirpath: str) -> bool:
    """ Create parent directory before cloning repo.

    https://github.com/tbonza/EDS19/issues/8
    """
    parent_dir = repo_name.split("/")[0]
    ppath = dirpath + parent_dir
    
    if os.path.exists(ppath):
        return True

    res = subprocess.run(["mkdir", ppath], capture_output=True)

    if res.returncode == 0 and os.path.exists(ppath):
        return True
    else:
        return False

def clone_repo(repo_name: str, dirpath: str) -> bool:
    """ Clone GitHub repo. """
    repo_path = "https://github.com/{}.git".format(repo_name)
    rpath = dirpath + repo_name

    res = subprocess.run(["git", "clone", repo_path, rpath],
                         capture_output=True)

    if res.returncode == 0 and os.path.exists(rpath):
        return True
    else:
        return False

def update_repo(repo_name: str, dirpath: str) -> bool:
    """ Update repo with new code. """
    c1 = ["git", "fetch"]
    rpath = dirpath + repo_name
    res = subprocess.run(c1, cwd=rpath, capture_output=True)

    if res.returncode == 0:
        return True
    else:
        return False

def repo_clone_main(fpath: str, dirpath: str):
    """ Clone all git repositories from repos list. """
    repos = read_repos(fpath)
    total_repos = len(repos)
    repo_count = 0
    tries = 0
    logger.info("Started cloning {} GitHub repositories".format(total_repos))
    while repo_count < total_repos:

        repo_name = repos[repo_count]
        rpath = dirpath + repo_name

        logger.info("Cloning '{}', attempt {}".\
                    format(repo_name, tries))

        if os.path.exists(rpath):
            logger.info("Repository '{}' already exists".\
                        format(repos[repo_count]))
            repo_count += 1

        else:
            yes_parent = create_parent_dir(repo_name, dirpath)
            attempt = clone_repo(repos[repo_count], dirpath)
            if attempt and yes_parent:
                logger.info("Successful clone: {}".format(repos[repo_count]))
                repo_count += 1                
            else:
                
                if tries < 3:
                    logger.warning("Retrying {}".format(repos[repo_count]))
                    tries += 1

                else:
                    logger.error("Unable to clone '{}'".\
                                 format(repos[repo_count]))
                    repo_count += 1
                    tries = 0
    logger.info("Finished cloning {} GitHub repositories".\
                format(total_repos))

def repo_update_main(fpath: str, dirpath: str):
    """ Update code for existing github repositories """
    repos = read_repos(fpath)
    total_repos = len(repos)
    repo_count = 0
    tries = 0
    logger.info("Started updating {} GitHub repositories".\
                format(total_repos))
    while repo_count < total_repos:

        repo_name = repos[repo_count]
        rpath = dirpath + repo_name

        logger.info("Updating '{}', attempt {}".\
                    format(repo_name, tries))

        attempt = update_repo(repos[repo_count], dirpath)
        if attempt:
            logger.info("Successful update: {}".format(repos[repo_count]))
            repo_count += 1                
        else:
            if tries < 3:
                logger.warning("Retrying {}".format(repos[repo_count]))
                tries += 1

            else:
                logger.error("Unable to update '{}'".\
                             format(repos[repo_count]))
                repo_count += 1
                tries = 0
    logger.info("Finished updating {} GitHub repositories".\
                format(total_repos))

