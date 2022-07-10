import datetime
import os

# setting config
import shutil
from pathlib import Path

PATH_BACKUP_FILE = '../db.sqlite3'
PATH_BACKUP_FOLDER = './saved'
ROTATE = 30


# second
# TIME = 60


def create_backup():
    date = datetime.datetime.now().__str__()
    mk_path = os.path.join(PATH_BACKUP_FOLDER, date)
    os.mkdir(mk_path)
    # copy backup
    shutil.copy(PATH_BACKUP_FILE, mk_path)
    logfile.write(f'add dir : {mk_path}\n')


if __name__ == "__main__":
    logfile = open('log.txt', 'a')

    # check exist backup file
    if not (os.path.exists(PATH_BACKUP_FILE)):
        raise "BACKUP FILE IS NOT EXIST"

    # check exist backup folder if not created
    Path(PATH_BACKUP_FOLDER).mkdir(parents=True, exist_ok=True)

    backup_folders = sorted(os.listdir(PATH_BACKUP_FOLDER))
    len_backup_folders = len(backup_folders)

    if len_backup_folders >= ROTATE:
        # del folders
        for index in range(len_backup_folders - ROTATE + 1):
            del_path = os.path.join(PATH_BACKUP_FOLDER, backup_folders[index])
            # os.rmdir(del_path)
            shutil.rmtree(del_path)
            logfile.write(f'del dir : {del_path}\n')

        create_backup()
    else:
        create_backup()

    logfile.close()
