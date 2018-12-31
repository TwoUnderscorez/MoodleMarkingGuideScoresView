""" Connection to the Moodle database
"""
import pymysql as sql
from pymysql.connections import Connection
from pymysql.cursors import Cursor


class MoodleDB():
    """ Connection to the Moodle database
    """

    def __init__(self, user: str, password: str, host: str, **kwargs):
        """ Initialize a connection to the moodle database

        Arguments:
            user {str} -- MySQL username
            password {str} -- MySQL password
            host {str} -- MySQL server ip/domain

        Keyword Arguments:
            port {int} -- MySQL server port
            database {str} -- database name
        """
        self.conn: Connection = sql.connect(
            user=user, host=host, password=password, **kwargs)
        self.cur: Cursor = self.conn.cursor()

    def get_course_list(self):
        pass

    def get_assignments_list(self, courseid: int):
        pass

    def get_user_info(self, userid: int) -> dict:
        """ Get the user's info, name, surname and email

        Arguments:
            userid {int} -- The user's ID in to moodle database

        Returns:
            dict -- a dictionary containing `id`, `name`, `surname` 
                    and `email` fields
        """
        return {}

    def get_instanceid_to_username_map(self):
        pass
