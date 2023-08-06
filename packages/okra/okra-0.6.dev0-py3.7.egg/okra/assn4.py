""" Compute Truck Factor

The truck factor assignment includes several factors. We're just
going to focus on the actual truck factor computation from a database
in this file.

References:
  http://janvitek.org/events/NEU/6050/a4.html
"""
from sqlalchemy import func
from okra.models import CommitMeta

def get_truck_factor_by_project(proj_name, dal):
    """ Get the 'truck factor' by project.

    1. For each project, and each file, compute how many lines were 
       added by each unique user.
    2. For each project, and each file, find which user created the file.
    3. Given the above two results compute the ownership of each file.
    4. For each project, and each file pick an owner.
    5. For each project, rank the users by the number of files they own.
    6. Given all of the above compute the Truck Factor as the smallest set 
       of users such that they own more than half of the files in the project.

    :param proj_name: name of GitHub project
    :param dal: okra.models.DataAccessLayer() with connection string param
    :return: Truck factor score for a GitHub project
    :rtype: float
    """
    query = dal.session.query(func.count(CommitMeta.commit_hash)). \
        group_by(CommitMeta.owner_name)

    return query
