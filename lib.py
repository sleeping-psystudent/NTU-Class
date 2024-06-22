import requests
from bs4 import BeautifulSoup

def crawler(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    js = soup.select('script[type="text/javascript"]')
    dtxt = eval(js[6].text.split('\n\n')[1].strip('var timeDT = ').strip(';'))

    dl = []
    for item in dtxt:
        for element in item.values():
            if type(element[0])==dict:
                dl.append(element[0])

    # source: https://blog.csdn.net/fengqianlang/article/details/130080073
    # data = list(
    #     {
    #         dictionary['cr_cono']: dictionary
    #         for dictionary in dl
    #     }.values()
    # )
    
    return dl

def latest_semester():
    url = "https://gra206.aca.ntu.edu.tw/classrm/acarm/webcr-use-new"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    op = soup.select('option')
    sem = op[0].text
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