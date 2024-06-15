import sqlite3
import pandas as pd
import datetime
import lib

def SQL_storage(data):
    # 連接SQLite數據庫
    conn = sqlite3.connect('classrooms.db')
    cursor = conn.cursor()

    # 創建表格
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS classroom_info (
        cr_cono TEXT,
        cr_clas TEXT,
        cr_cnam TEXT,
        cr_tenam TEXT,
        cr_no TEXT,
        cr_time TEXT
    )
    ''')

    # 插入資料
    for info in data:
        cursor.execute('''
        INSERT INTO classroom_info (cr_cono, cr_clas, cr_cnam, cr_tenam, cr_no, cr_time)
        VALUES (:cr_cono, :cr_clas, :cr_cnam, :cr_tenam, :cr_no, :cr_time)
        ''', info)

    conn.commit()
    conn.close()

def load():
    query = '''
    select * from classroom_info; 
    '''
    db = sqlite3.connect("classrooms.db")
    data = pd.read_sql_query(query, db)
    return data

def store():
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = [{'cr_cono': time,
    'cr_clas': '',
    'cr_cnam': '',
    'cr_tenam': '',
    'cr_no': '',
    'cr_time': ''}]

    sem = lib.latest_semester()
    clrooms = lib.class_rooms()
    for clroom in clrooms:
        url = "https://gra206.aca.ntu.edu.tw/classrm/acarm/webcr-use-new?SYearDDL="+sem+"&BuildingDDL=%25&RoomDDL="+clroom+"&SelectButton=%E6%9F%A5%E8%A9%A2"
        data += lib.crawler(url)
    SQL_storage(data)