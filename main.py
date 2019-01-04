""" Entry file
"""
import moodledb
import config


def main():

    db = moodledb.MoodleDB(config.MYSQL_USER, config.MYSQL_PASSWORD,
                           config.MYSQL_HOST, config.MYSQL_DB, port=config.MYSQL_PORT)
    ron = db.get_user_info(3)
    areaid = db.get_assignment_areaid(14)
    cr = db.get_criteria_names(areaid)
    db.close_no_save()


if __name__ == "__main__":
    main()
