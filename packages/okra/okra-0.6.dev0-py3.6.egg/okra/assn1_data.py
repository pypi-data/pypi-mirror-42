""" Handle the data requirements for Assignment 1 

References:
   Assignment 1: "http://janvitek.org/events/NEU/6050/a1.html"
   Git log formatting: "https://git-scm.com/docs/pretty-formats"
"""
import csv
import logging
import os
import subprocess

from okra.repo_mgmt import read_repos
from okra.protobuf.assn1_pb2 import Commit, Message, File

logger = logging.getLogger(__name__)


def parse_commits(rpath: str):
    """ Yields a protocol buffer of git commit information.

    commits.csv collects basic information about 
    commits and contains the following columns:

    hash
    author
    author email
    author timestamp
    committer
    committer email
    committer timestamp
    """
    c1 = ["git", "log",
          "--pretty=%H^|^%an^|^%ae^|^%ad^|^%cn^|^%ce^|^%ct"]
    res = subprocess.run(c1, cwd=rpath, capture_output=True)

    if res.returncode == 0:
        logger.info("SUCCESS -- extracted commits_csv info")

        rows = res.stdout.splitlines()

        for row_num, row in enumerate(rows):

            items = row.decode('utf-8', 'ignore').split("^|^")

            if len(items) == 7:
                commit = Commit()

                commit.hash_val = items[0]
                commit.author = items[1]
                commit.author_email = items[2]
                commit.author_timestamp = items[3]
                commit.committer = items[4]
                commit.committer_email = items[5]
                commit.committer_timestamp = items[6]
                
                yield commit

            else:
                logger.error("Issue with row {}, repo '{}'".\
                             format(row_num, rpath))            
    else:
        logger.error("FAIL -- unable to extract commits_csv")

def write_line_commits(parsed_commits):
    """ Generate a line for each git commit message. """
    for commit in parsed_commits:

        row = [
            commit.hash_val,
            commit.author,
            commit.author_email,
            commit.author_timestamp,
            commit.committer,
            commit.committer_email,
            commit.committer_timestamp,
        ]
        yield row

def parse_messages(rpath: str):
    """ Yields a protocol buffer of a git commit message.
    
    messages.csv collects commit messages and their 
    subject as follows:

    hash
    subject
    message
    """
    c1 = ["git", "log",
          "--pretty=^^!^^%H^|^%s^|^%b"]
    res = subprocess.run(c1, cwd=rpath, capture_output=True)

    if res.returncode == 0:
        logger.info("SUCCESS -- extracted messages_csv info")

        rows = res.stdout.decode('utf-8', 'ignore').split("^^!^^")

        for row_num, row in enumerate(rows):

            items = row.split("^|^")

            if len(items) == 3:

                message = Message()

                message.hash_val = items[0]
                message.subject = items[1]
                message.message_body = items[2]

                yield message
                
            else:
                logger.error("Issue with row {}, repo '{}'".\
                             format(row_num, rpath))
    else:
        logger.error("FAIL -- unable to extract messages_csv")

def write_line_messages(parsed_messages):
    """ Generate a line for each git commit message. """

    for message in parsed_messages:

        row = [
            message.hash_val,
            message.subject,
            message.message_body,
        ]
        yield row

def parse_files(rpath: str):
    """

    files.csv informs which files were modified by 
    commits. If a commit modifies multiple files, 
    files.csv will contain multiple lines referencing 
    that commit’s hash (one per modified file).

    hash
    file path
    """
    c1 = ["git", "log",
          '--pretty=^|^%n%H',
          '--numstat']
    res = subprocess.run(c1, cwd=rpath, capture_output=True)

    if res.returncode == 0:
        logger.info("SUCCESS -- extracted files_csv info")
        rows = res.stdout.decode('utf-8', 'ignore').split("^|^")

        for row_num, row in enumerate(rows):

            grp = row.splitlines()

            if len(grp) >= 3:
                
                hash_val = grp[1]

                for i in range(3, len(grp)):

                    possible_file = grp[i].split()

                    if len(possible_file) == 3:
                    
                        finfo = File()
                        
                        finfo.hash_val = hash_val
                        finfo.file_path = possible_file[-1]

                        yield finfo

            else:
                if len(grp) != 2:
                    logger.error("Issue with row {}, repo '{}'".\
                                 format(row_num, rpath))
    else:
        logger.error("FAIL -- unable to extract files_csv")

def write_line_files(parsed_files):
    """ Generate a line for each git filepath message. """

    for file_item in parsed_files:

        row = [
            file_item.hash_val,
            file_item.file_path,
        ]

        yield row

def extract_data_main(fpath: str, dirpath: str):
    """ Extract data as requested in Assignment 1. """
    logger.info("STARTED data extraction")
    
    commits = "commits.csv"
    messages = "messages.csv"
    files = "files.csv"
    
    outfiles = [{"parse"     : parse_commits,
                 "line"      : write_line_commits,
                 "file_name" : commits},
                {"parse"     : parse_messages,
                 "line"      : write_line_messages,
                 "file_name" : messages},
                {"parse"     : parse_files,
                 "line"      : write_line_files,
                 "file_name" : files}]

    repos = read_repos(fpath)
    logger.info("Extracting data for {} git repos".format(len(repos)))

    outs = {
        commits : open(dirpath + commits, "w"),
        messages: open(dirpath + messages, "w"),
        files: open(dirpath + files, "w"),
    }

    repo_count = 0
    for repo_name in repos:

        rpath = dirpath + repo_name

        logger.info("Extracting data in repo '{}'".format(rpath))

        for out_item in outfiles:

            lines = out_item["line"](out_item["parse"](rpath))

            logger.info("Adding to file '{}'".format(out_item["file_name"]))

            writer = csv.writer(outs[out_item["file_name"]],
                                delimiter=",",
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)

            for line in lines:

                writer.writerow(line)

    for key in outs.keys():

        outs[key].close()

    logger.info("Closed files")
    logger.info("FINISHED data extraction")

