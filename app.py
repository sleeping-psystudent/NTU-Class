import gradio as gr
import process
import datetime
import lib

# source: https://www.cnblogs.com/tian777/p/17371619.html
def store(progress = gr.Progress()):
    progress(0, desc="Starting")
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = [{'cr_cono': time,
    'cr_clas': '',
    'cr_cnam': '',
    'cr_tenam': '',
    'cr_no': '',
    'cr_time': ''}]

    sem = lib.latest_semester()
    clrooms = lib.class_rooms()
    for clroom in progress.tqdm(clrooms, desc="Reversing"):
        url = "https://gra206.aca.ntu.edu.tw/classrm/acarm/webcr-use-new?SYearDDL="+sem+"&BuildingDDL=%25&RoomDDL="+clroom+"&SelectButton=%E6%9F%A5%E8%A9%A2"
        data += lib.crawler(url)
    process.SQL_storage(data)

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