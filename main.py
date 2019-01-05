""" Entry file
"""
import moodledb
import config


def main():

    db = moodledb.MoodleDB(config.MYSQL_USER, config.MYSQL_PASSWORD,
                           config.MYSQL_HOST, config.MYSQL_DB, port=config.MYSQL_PORT)
    defid = db.get_assignment_definitionid(25)
    cr = db.get_criteria_names(defid)
    cids = [a['id'] for a in cr]
    assign_info = db.get_grading_info(cids)
    userid = db.instanceid_to_userid(49)
    db.close_no_save()


if __name__ == "__main__":
    main()
