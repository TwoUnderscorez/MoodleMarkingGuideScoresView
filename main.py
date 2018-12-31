""" Entry file
"""
import moodledb
import config


def main():

    db = moodledb.MoodleDB(config.MYSQL_USER, config.MYSQL_PASSWORD,
                           config.MYSQL_HOST, db=config.MYSQL_DB, port=config.MYSQL_PORT)
    print(db)


if __name__ == "__main__":
    main()
