""" Entry file
"""
import moodledb
import config


def main():
    db = moodledb.MoodleDB(config.MYSQL_USER, config.MYSQL_PASSWORD,
                           config.MYSQL_HOST, config.MYSQL_DB, port=config.MYSQL_PORT)
    defid = db.get_assignment_definitionid(25)
    crs = db.get_criteria_names(defid)
    cids = [cr['id'] for cr in crs]
    assign_info = db.get_grading_info(cids)
    userid = db.instanceid_to_userid(49)
    db.close_no_save()


def get_data_from_moodledb():
    db = moodledb.MoodleDB(config.MYSQL_USER, config.MYSQL_PASSWORD,
                           config.MYSQL_HOST, config.MYSQL_DB, port=config.MYSQL_PORT)
    courses = db.get_course_list()
    courseid = 0  # TODO: Add GUI and get input
    assigns = db.get_assignments_list(courseid)
    assignid = 0  # TODO: Add GUI and get input
    defid = db.get_assignment_definitionid(assignid)
    crs = db.get_criteria_names(defid)
    cids = [cr['id'] for cr in crs]
    assign_info = db.get_grading_info(cids)
    userid = db.instanceid_to_userid(49)
    db.close_no_save()


if __name__ == "__main__":
    main()
