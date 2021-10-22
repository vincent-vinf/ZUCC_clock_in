# coding=utf-8
import requests
import json
import time
import random
from urllib import parse

auth_url = "http://ca.zucc.edu.cn/cas/login"
clock_in_url = "http://ca.zucc.edu.cn/cas/login?service=http://yqdj.zucc.edu.cn/feiyan_api/h5/html/daka/daka.html"
handle_clock_in_url = "http://yqdj.zucc.edu.cn/feiyan_api/examen/examenAnswerController/commitAnswer.do"
InitHeader = {"Connection": "keep-alive",
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}

# 登陆表单
post_data = {
    "authType": "0",
    "execution": "e1s1",
    "lt": "",
    "_eventId": "submit",
    "submit": "",
    "randomStr": "",
}


def clock_in(config):
    post_data["username"] = config["username"]
    post_data["password"] = config["password"]
    session = requests.Session()
    response = session.get(url=auth_url, headers=InitHeader)
    if not response.ok:
        return False
    print("##GET login page succeed!")

    response = session.post(url=auth_url, data=post_data)
    if not response.ok:
        return False
    print("##Post login page succeed!")

    response = session.get(url=clock_in_url, headers=InitHeader)
    if not response.ok:
        return False
    print("##get Daka page succeed!")

    param = {
        "Rnd": random.random(),
        # "_":""
    }
    final_url = handle_clock_in_url + "?" + parse.urlencode(param)
    print("post data: " + final_url)
    response = session.post(final_url, json=make_request())
    try:
        re = json.loads(response.text)
    except ValueError:
        return False
    if re["code"] == 14801 or re["code"] == 1000:
        return True
    return False


def make_request():
    today = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    return {'examenSchemeId': 2, 'examenTitle': '师生报平安',
            'answer': '{"填报日期(Date)":"' + today + '","自动定位(Automatic location)":"浙江省 杭州市 拱墅区","目前所在地":"校内 校内 校内",'
                                                  '"近14天是否有与疫情中、高风险地区人员的接触史？(Did you contact any person(s) from medium or high risk area of '
                                                  'the epidemic in the past 14 days?)":"否(NO)","近14天是否有与疑似、确诊人员的接触史?(In the past 14 days, '
                                                  'did you contact any COVID-19 suspected or confirmed person(s)?)":"否(NO)",'
                                                  '"近21天是否有中高风险地区旅居史，近14天是否有中高风险地区所在区旅居史？( In the past 21 days, have you been to medium or '
                                                  'high-risk area? In the past 14 days, have you been to any places close to medium or high '
                                                  'risk area?)":"否(NO)","现是否处于医学观察状态？(Are you under medical observation currently ?)":"否(NO)",'
                                                  '"若处于医学观察状态，请填写隔离地点和隔离起始时间？(If yes, please indicate the place and the starting date.)":"",'
                                                  '"现是否处于居家隔离状态？(Are you in home quarantine now?)":"否(NO)","若处于居家隔离状态，请填写隔离地点和隔离起始时间？(If yes, '
                                                  'please indicate the place and the starting date.)":"","现身体状况，是否存在发热体温、寒战、咳嗽、胸闷以及呼吸困难等症状？( '
                                                  'Do you have any symptoms such as fever, chills, cough, chest tightness, and difficulty '
                                                  'breathing?)":"否(NO)","同住家属近14天是否有与疫情中、高风险地区人员的接触史？(Did your family member (s) living '
                                                  'together contact any person(s) from medium or high risk area in the past 14 days?)":"否('
                                                  'NO)","同住家属近14天是否有与疑似、确诊人员的接触史？(Did your family members living together contact any COVID-19 '
                                                  'suspected or confirmed person(s) in the past 14 days?)":"否(NO)","同住家属近14天是否到过疫情中、高风险地区？('
                                                  'Have any family members living together been to medium or high risk area in the past 14 '
                                                  'days?)":"否(NO)","同住家属现是否处于医学观察状态?(Are the family members living together under medical '
                                                  'observation?)":"否(NO)","今日申领学校所在地健康码的颜色? What\'s the color of today\'s health code?":"绿码('
                                                  'Green code)","本人或家庭成员(包括其他亲密接触人员)是否有近28日入境或未来7日拟入境的情况?Have you or your family members('
                                                  'including other close contact persons) entered China over the past 28 days or plan to enter '
                                                  'China in 7 days?":"否 No"} '}


if __name__ == '__main__':
    with open("./config.json", 'r') as configs:
        configs = json.load(configs)
        if clock_in(configs):
            print(time.strftime("%Y-%m-%d", time.localtime(time.time())), " 打卡成功", )
        else:
            print(time.strftime("%Y-%m-%d", time.localtime(time.time())), " 打卡失败!")
