import sqlite3
import pandas as pd

def SQL_storage(data):
    # 連接SQLite數據庫
    conn = sqlite3.connect('classrooms.db')
    cursor = conn.cursor()

    # 清空檔案
    cursor.execute('truncate table history')

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

def generate(course_name, teacher_name, selected_day):
    result = load()
    time = result.at[0, 'cr_cono']
    if course_name != "":
        result = result[result['cr_cnam'].str.contains(course_name, na=False)]
    if teacher_name != "":
        result = result[result['cr_tenam'].str.contains(teacher_name, na=False)]

    day_mapping = {
        "不限": "無",
        "星期一": "一",
        "星期二": "二",
        "星期三": "三",
        "星期四": "四",
        "星期五": "五"
    }
    day = day_mapping[selected_day]
    if day != "無":
        result = result[result['cr_time'].str.contains(day, na=False)]

    result['cr_cnam'] = result.apply(
        lambda row: f'<a href="https://coursemap.aca.ntu.edu.tw/course_map_all/course.php?code={row["cr_cono"].replace(" ", "+")}" target="_blank">{row["cr_cnam"]}</a>',
        axis=1
    )
    
    result = result.drop(columns=['cr_cono'])
    result = result.rename(columns={
        'cr_clas': '班次',
        'cr_cnam': '課程名稱',
        'cr_tenam': '授課教師',
        'cr_no': '教室',
        'cr_time': '時間'
    })
    
    return time, result.to_html(index=False, escape=False)