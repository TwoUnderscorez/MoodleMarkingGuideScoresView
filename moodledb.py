""" Connection to the Moodle database
"""
import pymysql
from pymysql.connections import Connection as PySQLCon


class MoodleDB():
    """ Connection to the Moodle database
    """

    def __init__(self, user: str,
                 password: str,
                 host: str,
                 **kwargs: dict):
        """ Initialize a connection to the moodle database

        Arguments:
            user {str} -- MySQL username
            password {str} -- MySQL password
            host {str} -- MySQL server ip/domain

        Keyword Arguments:
            port {int} -- MySQL server port
            database {str} -- database name
        """
        self.conn: PySQLCon = pymysql.connect(
            user=user, host=host, password=password, **kwargs)
        self.cur = self.conn.cursor()

    def get_instanceid_to_username_map(self):
        pass
