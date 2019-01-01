""" Connection to the Moodle database
"""
import pymysql as sql
from pymysql.connections import Connection
from pymysql.cursors import Cursor


class MoodleDB():
    """ Connection to the Moodle database
    """

    def __init__(self, user: str, password: str, host: str, db: str, **kwargs):
        """ Initialize a connection to the moodle database

        Arguments:
            user {str} -- MySQL username
            password {str} -- MySQL password
            host {str} -- MySQL server ip/domain
            db {str} -- database name

        Optional Keyword Arguments:
            port {int} -- MySQL server port
        """
        self.db = db
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
        return self._get_fileds_from_table('mdl_user', 'id', userid, 'id', 'firstname', 'lastname', 'email')

    def get_instanceid_to_username_map(self):
        pass

    def close(self):
        self.conn.commit()
        self.close_no_save()

    def close_no_save(self):
        self.cur.close()
        self.conn.close()

    def _get_fileds_from_table(self, from_: str, where: str = None, by: str = None, *args) -> dict:
        self.cur.execute(
            f"SELECT {str.join('',(f'{f},' for f in args))[:-1]} FROM {self.db}.{from_} "
            f"WHERE {where}={by};" if where else ';'
        )
        res = self.cur.fetchall()
        if where:
            return dict(zip(args, res[0]))
        else:
            raise NotImplementedError("Can't return a list of objects yet.")
