import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup

def crawler(url):
    # 設定重試機制
    session = requests.Session()
    retries = Retry(
        total=5,               # 總共嘗試次數
        backoff_factor=0.5,    # 每次重試間隔的基數
        status_forcelist=[500, 502, 503, 504]  # 在這些HTTP狀態碼出現時重試
    )
    session.mount('https://', HTTPAdapter(max_retries=retries))

    try:
        # 發送請求
        response = session.get(url, timeout=10)
        response.raise_for_status()  # 檢查HTTP請求是否成功
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return None

    # 解析HTML內容
    try:
        soup = BeautifulSoup(response.content, 'lxml')
        js = soup.select('script[type="text/javascript"]')
        dtxt = eval(js[6].text.split('\n\n')[1].strip('var timeDT = ').strip(';'))
    except Exception as e:
        print(f"Error parsing content: {e}")
        return None

    # 提取資料
    dl = []
    try:
        for item in dtxt:
            for element in item.values():
                if isinstance(element[0], dict):  # 檢查是否為字典型態
                    dl.append(element[0])
    except Exception as e:
        print(f"Error extracting data: {e}")
        return None

    return dl

# def crawler(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'lxml')
#     js = soup.select('script[type="text/javascript"]')
#     dtxt = eval(js[6].text.split('\n\n')[1].strip('var timeDT = ').strip(';'))

#     dl = []
#     for item in dtxt:
#         for element in item.values():
#             if type(element[0])==dict:
#                 dl.append(element[0])

    # source: https://blog.csdn.net/fengqianlang/article/details/130080073
    # data = list(
    #     {
    #         dictionary['cr_cono']: dictionary
    #         for dictionary in dl
    #     }.values()
    # )
    
# return dl

def latest_semester():
    url = "https://gra206.aca.ntu.edu.tw/classrm/acarm/webcr-use-new"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    op = soup.select('option')
    sem = op[0].text
    print(sem)
    return sem

def class_rooms():
    url = "https://gra206.aca.ntu.edu.tw/classrm/acarm/get-classroom-by-building"
    params = {
        "building": "%"
    }
    response = requests.get(url, params=params)
    data = response.json()
    room_ls = data['room_ls']

    clrooms = []
    for room in room_ls:
        clrooms.append(room["cr_no"])
    return clrooms