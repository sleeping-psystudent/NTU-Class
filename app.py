import gradio as gr
import process
from datetime import datetime, timedelta
import lib
import collections

def adjust_time(time_str):
    start_time, end_time = time_str.split('~')
    end_time = end_time.strip()
    end_time_dt = datetime.strptime(end_time, "%H:%M")
    adjusted_end_time_dt = end_time_dt + timedelta(minutes=50)
    adjusted_end_time = adjusted_end_time_dt.strftime("%H:%M")
    return f"{start_time}~{adjusted_end_time}"

def store(progress = gr.Progress()):
    progress(0, desc="Starting")
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = [{'cr_cono': time,
    'cr_clas': '',
    'cr_cnam': '',
    'cr_tenam': '',
    'cr_no': '',
    'cr_time': ''}]

    sem = lib.latest_semester()
    clrooms = lib.class_rooms()
    
    # source: https://www.cnblogs.com/tian777/p/17371619.html
    for clroom in progress.tqdm(clrooms, desc="Reversing"):
        url = "https://gra206.aca.ntu.edu.tw/classrm/acarm/webcr-use-new?SYearDDL="+sem+"&BuildingDDL=%25&RoomDDL="+clroom+"&SelectButton=%E6%9F%A5%E8%A9%A2"
        data += lib.crawler(url)
    
    # 同課程識別碼、同課名、同老師但不同教室、時間的課程合併
    courses = collections.defaultdict(lambda: {
        'cr_cono': '',
        'cr_clas': '',
        'cr_cnam': '',
        'cr_tenam': '',
        'cr_no': '',
        'cr_time': ''
    })

    for course in data:
        if course['cr_time'] != '':
            adj_time = adjust_time(course['cr_time'])
        else:
            adj_time = ''

        key = (course['cr_cono'], course['cr_clas'], course['cr_cnam'], course['cr_tenam'])
        if not courses[key]['cr_cono']:
            courses[key]['cr_cono'] = course['cr_cono']
            courses[key]['cr_clas'] = course['cr_clas']
            courses[key]['cr_cnam'] = course['cr_cnam']
            courses[key]['cr_tenam'] = course['cr_tenam']
            courses[key]['cr_no'] = course['cr_no']
            courses[key]['cr_time'] = adj_time
        else:
            if course['cr_no'] not in courses[key]['cr_no']:
                courses[key]['cr_no']+=f"<br>{course['cr_no']}"
            if adj_time not in courses[key]['cr_time']:
                courses[key]['cr_time']+=f"<br>{adj_time}"

    data_re = []
    for course in courses.values():
        data_re.append(course)

    process.SQL_storage(data_re)

def main():
    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column(scale = 1):
                course_name_input = gr.Textbox(label="課程名稱", placeholder="輸入關鍵字即可")
                teacher_name_input = gr.Textbox(label="教師姓名", placeholder="輸入關鍵字即可")
                day_input = gr.Dropdown(choices=["不限", "星期一", "星期二", "星期三", "星期四", "星期五"], label="時間", value="不限")
                submit_button = gr.Button("Submit")
                time_output = gr.Textbox(label="資料集更新時間")
                update_button = gr.Button("Update")
                progress_output = gr.Textbox(label="資料集更新進度")
            with gr.Column(scale = 2):
                dataframe_output = gr.HTML(label="搜尋結果")

        submit_button.click(process.generate, inputs=[course_name_input, teacher_name_input, day_input], outputs=[time_output, dataframe_output])
        update_button.click(store, inputs=[], outputs=[progress_output])
    demo.launch(share=True, debug=True)

if __name__=='__main__':
    main()