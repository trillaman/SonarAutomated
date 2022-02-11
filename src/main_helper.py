import os
import platform
import sys
import sqlite3


def close_db_connection():
    con = get_db_connection()
    con.close()
    return True


def get_db_connection():
    try:
        con = sqlite3.connect('scan.db')
        print("Connected to db")
    except Exception:
        con = False
        print("Can't connect to db")
    return con


def get_last_id():
    con = get_db_connection()
    if con is not False:
        cursor = con.execute("SELECT MAX(ID) FROM scans")
        for row in cursor:
            max_id = row[0]

    return max_id


def insert_log_file(proj_name, report_path, scanning_tool):
    con = get_db_connection()
    if con is not False:
        max_id = get_last_id()
        sql_insert = "INSERT INTO scans (ID,PROJECT_NAME,REPORT_PATH,SCAN_TOOL) VALUES (" + max_id + "," + str(proj_name) + "," + str(report_path) + "," + str(scanning_tool) + ")"
        con.execute(sql_insert)
        con.commit()
        print("Records created successfully")

    return True


def get_proper_slashes():
    if platform.system() == 'Windows':
        return "\\"
    elif platform.system() == 'Linux':
        return "/"


def check_output_exists(path):
    try:
        report_path = open(path, "w")
    except Exception:
        print("Can't open output file for reporting: " + path)
        sys.exit()

    return report_path


def get_filename(filepath):
    filep = set_slashes(filepath)
    split_tup = filep.split(get_proper_slashes())
    filename = split_tup[-1]
    filename = filename.split(".")

    return filename[0]


def set_slashes(path):
    if platform.system() == 'Windows':
        path = path.replace("/", "\\")
    elif platform.system() == 'Linux':
        path = path
    else:
        print("Unknown platform")
        return path
    return str(path)


def get_file_extension(filepath):
    filep = set_slashes(filepath)
    if platform.system() == 'Windows':
        split_tup = filep.split("\\")
    else:
        split_tup = filep.split("/")

    filename = split_tup[-1]
    ext = filename.split(".")
    return ext[1]


# CANT BE TESTED YET ON WINDOWS
def unzip_file(self, project_folder, file_to_unzip):
    unzip_cmd = "unzip -d " + project_folder + " " + file_to_unzip
    try:
        os.system(unzip_cmd)
    except Exception:
        print("Couldn't unzip file" + file_to_unzip + " to " + project_folder)
    finally:
        print("File " + file_to_unzip + " unzipped")

    return True
