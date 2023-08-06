""" Parses and implements playbook commands. Similar to Ansible

References:
  https://docs.ansible.com/
"""
import logging

from yaml import load, Loader

from okra.playbooks.assn2 import run_assn2

logger = logging.getLogger(__name__)

def load_playbook(filepath: str):
    """ Parse Okra Playbook in YAML format. """
    try:
        with open(filepath, "r") as infile:
            data = load(infile, Loader=Loader)
        return data

    except FileNotFoundError as exc:
        logger.error("Unable to find file")
        logger.exception(exc)
        raise exc

    except Exception as exc:
        logger.exception(exc)
        raise exc

def parse_playbook(playbook: list):

    for item in playbook:

        for task in item['tasks']:

            if task['task_id'] == 'assn2':

                logger.info("TASK IDENTIFIED: {}".\
                            format(task['task_id']))
                task_args = task['run']
                run_assn2(task_args)
                
                
