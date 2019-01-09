""" Entry file
"""
import moodledb
import config


def main():
    res = get_data_from_moodledb()
    usr = get_user_data(res)
    print('Done')


def get_data_from_moodledb():
    retdata = {}
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
    for crid, crdataarr in assign_info.items():
        retdata[crid] = {}
        for crdata in crdataarr:
            retdata[crid][db.instanceid_to_userid(
                crdata['instanceid'])] = crdata
    db.close_no_save()
    return retdata


def get_user_data(assign_info):
    retdata = {}
    db = moodledb.MoodleDB(config.MYSQL_USER, config.MYSQL_PASSWORD,
                           config.MYSQL_HOST, config.MYSQL_DB, port=config.MYSQL_PORT)
    for crid, crdata in assign_info.items():
        for userid in crdata:
            retdata[userid] = db.get_user_info(userid)
        break
    return retdata


if __name__ == "__main__":
    main()
