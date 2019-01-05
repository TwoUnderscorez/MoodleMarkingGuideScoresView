""" Connection to the Moodle database
"""
import warnings
from typing import Dict, List
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

    def close(self):
        self.conn.commit()
        self.close_no_save()

    def close_no_save(self):
        self.cur.close()
        self.conn.close()

    def get_course_list(self) -> List[dict]:
        """ Get list of courses

        Returns:
            List[dict] -- A list of dictionaries with `id`, `fullname`, 
                          `shortname` and `summary` of the course
        """
        return self._get_fileds_from_table('mdl_course', None, None, 'id',
                                           'fullname', 'shortname', 'summary')

    def get_assignments_list(self, courseid: int) -> List[dict]:
        """ Get the list of assignments in a course

        Arguments:
            courseid {int} -- The ID of the course

        Returns:
            List[dict] -- a list of dicts containing `id` and `name` of the assignment
        """
        return self._get_fileds_from_table('mdl_assign', 'course', courseid, 'id', 'name')

    def get_user_info(self, userid: int) -> dict:
        """ Get the user's info, name, surname and email

        Arguments:
            userid {int} -- The user's ID in to moodle database

        Raises:
            KeyError -- If there is no such user with the given id

        Returns:
            dict -- a dictionary containing `id`, `name`, `surname`
                    and `email` fields
        """
        res = self._get_fileds_from_table(
            'mdl_user', 'id', userid, 'id', 'firstname', 'lastname', 'email')
        if len(res) == 0:
            raise KeyError(
                f'No such user with id of {id} in {self.db}.mdl_user')
        return res[0]

    def _get_fileds_from_table(self, from_: str, where: str = None, by: str = None, *args) -> List[dict]:
        """ Get data from a table

        Arguments:
            from_ {str} -- From which table

        Keyword Arguments:
            where {str} -- Column name of where clause (default: {None})
            by {str} -- Value of where clause (default: {None})

        Variable Positional Arguments:
            args {[str,]} -- the culumns to select

        Returns:
            List[dict] -- A list of dicts containing the result `column`:`value`
        """
        sqlq: str = (
            (f"SELECT {str.join('',(f'{f},' for f in args))[:-1]} FROM {self.db}.{from_} ") +
            (f"WHERE {where}={by};" if where else ';')
        )
        self.cur.execute(sqlq)
        res = self.cur.fetchall()
        return [dict(zip(args, r)) for r in res]

    def get_assignment_definitionid(self, areaid: int) -> int:
        """ Get the definitionid of an assignment for the mdl_gradingform_guide_criteria table

        Arguments:
            areaid {int} -- The id of the assignment in mdl_assign

        Raises:
            KeyError -- If there is no such assignment with the given id

        Returns:
            int -- The definitionid of the assignment
        """
        res = self._get_fileds_from_table(
            'mdl_grading_definitions', 'areaid', areaid, 'id')
        if len(res) == 0:
            raise KeyError(
                f'No such assignment with id of {id} in {self.db}.mdl_grading_definitions')
        elif len(res) > 1:
            warnings.warn(
                f'There should be only one assignment with id of {id} in {self.db}.mdl_grading_definitions but {len(res)} matches were found. Using the first one.',
                RuntimeWarning,
                stacklevel=2
            )
        return int(res[0]['id'])

    def get_criteria_names(self, definitionid: int) -> List[dict]:
        """ Get the criteria text of an assignment

        Arguments:
            definitionid {int} -- The definitionid of the assignment

        Returns:
            List[dict] -- A list of dicts containing `id`, `definitionid`, 
                          `shortname` and `maxscore` fields of a criterion

        Note:
            Always use `MoodleDB.get_assignment_definitionid` to get the definitionid
        """
        return self._get_fileds_from_table('mdl_gradingform_guide_criteria', 'definitionid',
                                           definitionid, 'id', 'definitionid', 'shortname', 'maxscore')

    def get_grading_info(self, criteria_ids: List[int]) -> List[List[Dict[str, str]]]:
        """ Get each student's score for all the criteria

        Arguments:
            criteria_ids {List[int]} -- The criteria IDs that represent
                                        the assignment

        Returns:
            List[List[Dict[str, str]]] -- List[criterion][students][instanceid, str]
                                          where the str there represents the `remark`
                                          and `score` of a students data on a spesific
                                          criterion
        """

        retdata = {}
        for cid in criteria_ids:
            retdata[cid] = self._get_fileds_from_table('mdl_gradingform_guide_fillings',
                                                       'criterionid', cid, 'id', 'instanceid', 'criterionid', 'remark', 'score')
        return retdata

    def get_instanceid_to_username_map(self):
        pass
