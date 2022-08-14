# coding=utf-8
import os
import requests
import json
import time
import random
from urllib import parse
from email_sender import EmailSender

auth_url = "http://ca.zucc.edu.cn/cas/login"
clock_in_url = "http://ca.zucc.edu.cn/cas/login?service=http://yqdj.zucc.edu.cn/feiyan_api/h5/html/daka/daka.html"
handle_clock_in_url = "http://yqdj.zucc.edu.cn/feiyan_api/examen/examenAnswerController/commitAnswer.do"
find_examen_schema_url = "http://yqdj.zucc.edu.cn/feiyan_api/examen/examenSchemeController/findExamenSchemeById.do"
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
# examen schema id
examen_schema_id = 2
examen_schema_validation = False
today = time.strftime("%Y-%m-%d", time.localtime(time.time()))

'''
自定义打卡失败异常类
1 打卡模版不一致错误
2 账号密码不正确错误
'''


class ClockInError(Exception):
    def __init__(self, code):
        self.code = code
        errs = {
            1: "问卷内容更新！请及时更新！",
            2: "账号或密码不正确！"
        }
        self.msg = errs.get(code)


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
    # 登陆失败
    if session.cookies.get("CASTGC") is None:
        raise ClockInError(2)
    print("##Post login page succeed!")

    response = session.get(url=clock_in_url, headers=InitHeader)
    if not response.ok:
        return False
    print("##get Daka page succeed!")

    param = {
        "Rnd": random.random(),
        # "_":""
    }

    # 验证表单内容是否更新
    global examen_schema_validation
    if not examen_schema_validation:
        find_schema_url = find_examen_schema_url + "?" + parse.urlencode(param)
        response = session.post(find_schema_url, data={"esId": examen_schema_id})
        re = json.loads(response.text)
        schema_local_path = "examen_schema.json"
        if os.path.exists(schema_local_path):
            f = open("examen_schema.json", 'r')
            scheme_local = json.loads(f.read())["scheme"]
            # update_time_local = json.loads(f.read())["updateTime"]
            # 判断 schema 更新时间是否相同
            if scheme_local != re["data"]["examen"]["scheme"]:
                # save_schema(re)
                raise ClockInError(1)
        else:
            save_schema(re)
        examen_schema_validation = True

    final_url = handle_clock_in_url + "?" + parse.urlencode(param)
    print("post data: " + final_url)
    response = session.post(final_url, json=make_request(
        config["vaccine"],
        config["address"] if "address" in config.keys() else "",
        config["inSchool"]
    ))
    try:
        re = json.loads(response.text)
        print(re)
    except ValueError:
        return False
    if re["code"] == 14801 or re["code"] == 1000:
        return True
    return False


def save_schema(re):
    schema_dic = {
        "scheme": re["data"]["examen"]["scheme"],
        "updateTime": re["data"]["examen"]["updateTime"]
    }
    f = open("examen_schema.json", "w")
    f.write(json.dumps(schema_dic, ensure_ascii=False))
    f.close()


def make_request(vaccine, address, in_school):
    # vaccine为编号
    vaccine_list = {"1": "已接种第一针 (first jab received) ",
                    "2": "已接种第二针（已满6个月）(second jab received, more than 6 months)",
                    "3": "已接种第二针（未满6个月）(second jab received, less than 6 months)",
                    "4": "已接种第三针( booster jab received)",
                    "5": "未接种(unvaccinated)"}

    return {'examenSchemeId': examen_schema_id, 'examenTitle': '师生报平安',
            'answer': '{"填报日期(Date)":"' + today + '","自动定位(Automatic location)":"' +
                      (address if address else '浙江省 杭州市 拱墅区') +
                      '",'
                      '"今日是否在校？(Are you on campus today?)":"' +
                      ('是(Yes)' if in_school else '否(NO)') +
                      '",'
                      '"近2天内是否曾经离杭？(Did you ever leave Hangzhou in past two days?)":"否(NO)",'
                      '"近7天是否有国内高中低风险地区旅居史?( In the past 7 days, have you ever been to any low, medium or high risk '
                      'areas?)":"否(NO)",'
                      '"近7天是否有（或被告知有）与疑似、确诊人员或密切接触者的接触史? (In the past 7 days，did you contact any COVID-19 suspected '
                      'or confirmed person(s) or close contacts ?)":"否(NO)",'
                      '"现是否处于健康管理（管控）期? 如是，请暂缓来校。(Are you under health management period currently ? If yes, '
                      'please do not come to school for the time being.) ":"否(NO)",'
                      '"现身体状况，是否存在发热体温、寒战、咳嗽、胸闷以及呼吸困难等症状? (Do you have any symptoms such as fever, chills, cough, '
                      'chest tightness and dyspnea?)":"否(NO)",'
                      '"同住家属（人员）是否有上述与疫情相关的情况？(Did your family members(s) living together have any situation '
                      'mentioned above ?)":"否(NO)",'
                      '"当前疫苗接种情况? (Vaccination status?)":"' +
                      vaccine_list[vaccine] +
                      '",'
                      '"本人或家庭成员(包括其他亲密接触人员)是否有近10日入境或未来7天内拟入境的情况? (Have you or your family members(including other '
                      'close contact persons) entered China over the past 10 days or plan to enter China in 7 '
                      'days?)":"否(NO)"}'}


if __name__ == '__main__':
    with open("./config.json", 'r', encoding='utf-8') as configs:
        configs = json.load(configs)
        email_config = None
        sender = None
        if "email" in configs.keys():
            email_config = configs["email"]
            try:
                sender = EmailSender(email_config["host"], email_config["username"], email_config["password"])
            except BaseException as e:
                print("获取邮箱发送实例失败，" + e.__str__() + "！\n")
                exit(0)

        log = ""
        for config in configs["user"]:
            u = config["username"]
            if len(u) == 0:
                continue
            if "tag" in config.keys():
                u += "(" + config["tag"] + ")"
            print(u)
            try:
                if clock_in(config):
                    u += ": 打卡成功！\n"
                else:
                    u += ": 打卡失败！\n"
            except ClockInError as e:
                print(e.msg)
                if e.code != 1:
                    u += "：打卡失败！" + e.msg + "\n"
                else:
                    log = e.msg
                    # 发送问卷内容更新消息给打卡人
                    if sender is not None:
                        for u in configs["user"]:
                            if "email" in config.keys() and config["email"] != "":
                                sender.send(config["email"], "ZUCC 打卡日志", today + ":\n打卡失败！问卷内容更新，请及时联系管理员！")
                    break
            except BaseException as e:
                print(e)
                u += ": 打卡失败！未处理的异常！\n"
            # 发送打卡信息给打卡人
            if sender is not None and "email" in config.keys():
                sender.send(config["email"], "ZUCC 打卡日志", today + ":\n" + u)
            log += u
            sleep_time = random.randint(500, 3000) / 1000
            time.sleep(sleep_time)

        print(log)
        if sender is not None:
            sender.send(email_config["receiver"], "ZUCC 打卡日志（总）", today + ":\n" + log)
            sender.quit()
