import gradio as gr
import pandas as pd
import process

def main():
    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column(scale = 1):
                course_name_input = gr.Textbox(label="課程名稱", placeholder="輸入關鍵字即可")
                teacher_name_input = gr.Textbox(label="教師姓名", placeholder="輸入關鍵字即可")
                day_input = gr.Dropdown(choices=["不限", "星期一", "星期二", "星期三", "星期四", "星期五"], label="時間", value="不限")
                submit_button = gr.Button("Submit")
                time_output = gr.Textbox(label="資料集更新時間")
            with gr.Column(scale = 2):
                dataframe_output = gr.HTML(label="搜尋結果")

        submit_button.click(process.generate, inputs=[course_name_input, teacher_name_input, day_input], outputs=[time_output, dataframe_output])
    demo.launch(share=True, debug=True)

if __name__=='__main__':
    main()