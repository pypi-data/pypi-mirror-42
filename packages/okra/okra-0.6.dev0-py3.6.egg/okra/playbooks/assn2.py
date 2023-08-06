""" Complete Assignment 2

http://janvitek.org/events/NEU/6050/a2.html
"""
import logging

from okra.assn2_db import (config_assn2_schema, metadata_tosql, erm_diagram)

logger = logging.getLogger(__name__)

def run_assn2(task_args: dict):
    """ Run assignment 2 """
    schema_dest = task_args.get("schema_dest", "")
    diagram_dest = task_args.get("diagram_dest", "")
    db_url = task_args.get("db_url", "")

    logger.info("INITIALIZED task_id: assn2")
    logger.info("""Task args:
    schema_dest: {},
    diagram_dest: {},
    db_url: {}
    """.format(schema_dest, diagram_dest, db_url))

    metadata = config_assn2_schema()
    logger.info("Retrieved metadata")

    logger.info("Generating SQL")
    schema_sql = metadata_tosql(metadata, db_url)
    with open(schema_dest, "w") as outfile:
        outfile.write(schema_sql)

    logger.info("Generating diagram")
    dgram = erm_diagram(metadata, diagram_dest)

    logger.info("COMPLETED task_id: assn2")

    
