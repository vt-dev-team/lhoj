import json
import requests
import random
import shutil
import time
import os
import subprocess
import psutil
import zipfile

backendUrl = "http://127.0.0.1"   # 后端地址
defaultChecker = r"diff -b -B --text {outputFile} {answerFile}"  # 默认检查器
judgerUser = {  # 评测用户设置
    "uname": "LH_AK_IOI",  # 用户名
    "pword": "bda7e9b27d43ab06748",  # 密码
    "nick": "李华一号"  # 评测机
}
savedCookie = {}
privilege = 247
judgeWait = 5  # 间隔时间(s)


# 随机字符串，用来作为文件夹名称
def ranstr(num):
    H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    salt = ''
    for i in range(num):
        salt += random.choice(H)
    return salt

# 题目


class Problem:
    id = 1            # 题目编号
    time = 1000       # 时间限制
    memory = 262144   # 内存限制
    templateFile = ''  # 模板文件
    checker = defaultChecker
    data = []         # 测试点

    def __init__(self, id, time=1000, memory=262144, data=[]):  # 初始化
        self.id = id
        self.time = time
        self.memory = memory
        self.data = data

    def fetch_dir(self):
        try:
            with open('./data/{}/config.lh'.format(self.id), 'r', encoding='utf8') as f:  # 读取配置文件
                problem_data = json.load(f)
                # print(problem_data)
                if 'time' in problem_data:
                    self.time = problem_data['time']
                if 'memory' in problem_data:
                    self.memory = problem_data['memory']
                if 'datas' in problem_data:
                    self.data = problem_data['datas']
                if 'template' in problem_data:
                    self.templateFile = problem_data['template']
                if 'checker' in problem_data:
                    self.checker = problem_data['checker']
        except Exception as e:
            pass

    def download(self):  # 下载数据文件
        if os.path.exists('./data/{}'.format(self.id)):
            return
        try:
            r = requests.post("{}/api/problem/{}/download/".format(backendUrl, self.id),
                              cookies=savedCookie, stream=True)
            with open("./data/{}.zip".format(self.id), 'wb') as fp:
                for chunk in r.iter_content(512):
                    fp.write(chunk)
            f = zipfile.ZipFile("./data/{}.zip".format(self.id))
            f.extractall('./data/{}'.format(self.id))
            # print(f.namelist())
        except Exception as e:
            print(e)


# 评测记录
class Submission:
    id = 1        # 编号
    user_id = ""
    code = ""
    time = 0
    memory = 0
    score = 0
    result = 0
    problem = ""
    cases = ""
    judger = ""
    date = ""
    onlyKey = ""

    def __init__(self, id=0):
        global backendUrl, judgerUser
        if id != 0:   # 指定了id，直接获取
            self.id = id
            r = requests.get(
                "{}/api/submission/{}/".format(backendUrl, self.id))
            res = r.json()
            self.user_id = res["user_id"]
            self.code = res["code"]
            self.problem = res["problem"]
            self.date = res["date"]
            self.judger = judgerUser["nick"]
            self.cases = judgerUser["cases"]
        else:
            r = requests.get(
                "{}/api/submission/latest/".format(backendUrl))  # 获取最新的未评测的记录
            try:
                res = r.json()
                if res["id"] == 0:  # 没有最新的
                    self.id = 0
                else:
                    res = res["submission"]
                    self.id = res["id"]
                    self.user_id = res["user_id"]
                    self.code = res["code"]
                    self.problem = res["problem"]
                    self.date = res["date"]
                    self.judger = judgerUser["nick"]
                    self.cases = judgerUser["cases"]
            except Exception as e:
                pass

    def makeUp(self, tp, cker):   # 建立临时文件夹
        self.onlyKey = ranstr(8)
        onlyKey = self.onlyKey
        rawCode = self.code
        if tp != "":
            try:
                deperatedCode = self.code.splitlines()
                # print(deperatedCode)
                with open('./data/{}/{}'.format(self.problem, tp), 'r') as f:
                    self.code = f.read()
                for i in deperatedCode:
                    self.code = self.code.replace("__BLANK__", i, 1)
            except Exception as e:
                self.result = 10
                self.case = "{ \"mes\":\"Error: {}\", \"datas\":[] }".format(e)
        try:
            if os.path.exists('tmp/{}'.format(onlyKey)):
                shutil.rmtree('tmp/{}'.format(onlyKey))
            os.mkdir('tmp/{}'.format(onlyKey))
            with open('tmp/{}/code.py'.format(onlyKey), "w") as f:
                #f.write(self.code)
                f.write("\n".join([p for p in self.code.splitlines() if p]))
            with open('tmp/{}/raw_code.py'.format(onlyKey), "w") as f:
                #f.write(rawCode)
                f.write("\n".join([p for p in rawCode.splitlines() if p]))
            if cker != defaultChecker:
                shutil.copyfile('./data/{}/{}'.format(self.problem,
                                cker), 'tmp/{}/{}'.format(onlyKey, cker))
        except Exception as e:
            self.result = 10
            self.case = "{ \"mes\":\"Error: {}\", \"datas\":[] }".format(e)

    def DeleteSelf(self):   # 删除临时文件夹
        onlyKey = self.onlyKey
        shutil.rmtree('tmp/{}'.format(onlyKey))

    def judge(self):
        P = Problem(self.problem)
        try:
            P.download()  # 下载数据
            P.fetch_dir()  # 配置数据
            resultVal = []
            self.score = 0
            self.time = 0
            self.memory = 0
            self.result = 2  # 结果改为评测中
            # print(self.code)
            self.makeUp(P.templateFile, P.checker)  # 建立临时文件夹
            if self.result != 2:
                raise ValueError("建立文件夹时遇到错误")
            rescnt = [0 for i in range(10)]  # 记录各种测试结果数量
            failed = 0  # 失败的测试点数目
            maxRes = 0  # 出现次数最多的测试结果
            if (len(P.data) <= 0):
                raise ValueError("找不到测试数据")
            casesJson = {}  # 若以前有评测了一部分，解析这个结果
            try:
                casesJson = json.loads(self.cases)
            except Exception as e:
                pass
            if ("datas" in casesJson) and (len(casesJson["datas"]) > 0):
                resultVal = casesJson["datas"]
            else:
                for DataSet in P.data:  # 初始化评测结果
                    resultVal.append({
                        "res": 0,
                        "time": 0,
                        "memory": 0,
                        "mes": ""
                    })
            self.cases = json.dumps({
                "datas": resultVal
            })
            self.save(hasCases=True)  # 先提交给服务器
            for i in range(len(P.data)):  # 测试每个测试点
                R = resultVal[i]
                if R["res"] > 2:  # 已经评测过了就不评测了
                    continue
                DataSet = P.data[i]
                q = self.judgeOne('./data/{}/{}'.format(P.id, DataSet["in"]), './data/{}/{}'.format(
                    P.id, DataSet["out"]), P.time, P.memory, P.checker)  # 测试一个测试点
                # print(q)
                R["res"] = q["code"]
                R["mes"] = q["mes"]
                if q["code"] == 3:
                    self.score += DataSet["score"]
                rescnt[R["res"]] += 1
                if (rescnt[R["res"]] > rescnt[maxRes]) and (R["res"] != 3):  # 更新出现次数最多的测试结果
                    maxRes = R["res"]
                if R["res"] != 3:               # 不正确，有测试点未通过
                    failed = 1
                R["time"] = (int)(q["time"] * 1000)  # 记录时间和内存
                self.time += R["time"]  # 更新总时间和内存
                R["memory"] = (int)(q["memory"])
                self.memory += R["memory"]
                self.cases = json.dumps({   # 更新评测数据
                    "datas": resultVal
                })
                self.save_one_case(i, R)
            if failed == 0:        # 没有测试点未通过，那么正确
                self.result = 3
            else:
                self.result = maxRes
            self.save()
            self.DeleteSelf()
        except Exception as e:
            print(e)
            self.result = 10
            self.cases = json.dumps({
                "mes": "Error: {}".format(e)
            })
            self.save(hasCases=True)

    def judgeOne(self, inp, outp, tim, memory, checker):
        onlyKey = self.onlyKey
        if os.path.exists('tmp/{}/data.in'.format(onlyKey)):  # 先清空临时文件夹
            os.remove('tmp/{}/data.in'.format(onlyKey))
        if os.path.exists('tmp/{}/data.out'.format(onlyKey)):
            os.remove('tmp/{}/data.out'.format(onlyKey))
        if os.path.exists('tmp/{}/data.ans'.format(onlyKey)):
            os.remove('tmp/{}/data.ans'.format(onlyKey))
        if not os.path.exists(inp):
            return {
                "code": 10,
                "time": 0,
                "memory": 0,
                "returnCode": 0,
                "diffVal": 0,
                "score": 0,
                "mes": "找不到测试输入文件"
            }
        if not os.path.exists(outp):
            return {
                "code": 10,
                "time": 0,
                "memory": 0,
                "returnCode": 0,
                "diffVal": 0,
                "score": 0,
                "mes": "找不到测试输出文件"
            }
        shutil.copyfile(inp, 'tmp/{}/data.in'.format(onlyKey))  # 复制输入文件
        inputFileReader = open('tmp/{}/data.in'.format(onlyKey), 'r')
        outputFileWrite = open('tmp/{}/data.out'.format(onlyKey), 'w')
        errorFileWrite = open('tmp/{}/err.out'.format(onlyKey), 'w')
        startTime = time.time()  # 开始运行时间
        user_Run = subprocess.Popen('python {}'.format(
            'tmp/{}/code.py'.format(onlyKey)), shell=True, stdin=inputFileReader, stdout=outputFileWrite, stderr=errorFileWrite)  # 运行文件
        endTime = 0  # 结束运行时间
        judged = 0
        MemoryUse = 0  # 内存使用
        TimeUse = 0   # 时间使用
        while True:
            is_run = 0  # 用来记录程序是否还在运行
            endTime = time.time()  # 更新结束运行的时间
            TimeUse = endTime - startTime  # 更新运行的时间
            try:
                pRun = psutil.Process(user_Run.pid)  # 获取内存
                muse = (pRun.memory_info().rss + pRun.memory_info().vms) / 1024
            except Exception as e:
                break
            else:
                if muse > MemoryUse:  # 内存取最大值
                    MemoryUse = muse
            if user_Run.poll() is None:
                is_run = 1
            if MemoryUse > memory:  # 超出内存限制，kill，下同
                os.system("taskkill /F /PID {} /T".format(user_Run.pid))
                return {
                    "code": 6,
                    "time": TimeUse,
                    "memory": MemoryUse,
                    "returnCode": 1,
                    "diffVal": 0,
                    "score": 0,
                    "mes": ""
                }
            if endTime - startTime >= (tim / 1000) + 0.2:
                os.system("taskkill /F /PID {} /T".format(user_Run.pid))
                break
        user_Run.wait()  # 等待执行完毕
        if endTime - startTime >= (tim / 1000):
            return {
                "code": 5,
                "time": TimeUse,
                "memory": MemoryUse,
                "returnCode": 1,
                "diffVal": 0,
                "score": 0,
                "mes": ""
            }
        rcode = user_Run.returncode  # 获取返回值
        shutil.copyfile(outp, 'tmp/{}/data.ans'.format(onlyKey))  # 复制答案文件
        if rcode == 0:  # 正常运行，那么比较文件
            if checker != defaultChecker:
                checker = 'tmp/{}/{}'.format(
                    onlyKey, checker)
                if checker.find('.py') != 0:
                    checker = 'python {}'.format(checker)
                checker += r' {inputFile} {outputFile} {answerFile} {codeFile}'
            checker += ">diff.txt"
            fileFormatter = {
                'inputFile': 'tmp/{0}/data.in'.format(onlyKey),
                'outputFile': 'tmp/{0}/data.ans'.format(onlyKey),
                'answerFile': 'tmp/{0}/data.out'.format(onlyKey),
                'codeFile': 'tmp/{0}/raw_code.py'.format(onlyKey),
            }
            diff_val = os.system(checker.format(**fileFormatter))
            with open("diff.txt", 'r') as diffReader:
                diff_text = diffReader.read(128)
            if diff_val != 0:
                return {
                    "code": 4,
                    "time": TimeUse,
                    "memory": MemoryUse,
                    "returnCode": rcode,
                    "diffVal": diff_val,
                    "score": 0,
                    "mes": diff_text
                }
            else:
                diff_val = 0
                return {
                    "code": 3,
                    "time": TimeUse,
                    "memory": MemoryUse,
                    "returnCode": rcode,
                    "diffVal": diff_val,
                    "score": 0,
                    "mes": diff_text
                }
        else:
            with open('tmp/{}/err.out'.format(onlyKey), 'r') as errReader:
                err_text = errReader.read(128)
            return {
                "code": 8,
                "time": TimeUse,
                "memory": MemoryUse,
                "returnCode": rcode,
                "diffVal": 0,
                "mes": err_text
            }

    def get_all(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "code": self.code,
            "time": self.time,
            "memory": self.memory,
            "score": self.score,
            "result": self.result,
            "cases": self.cases,
            "judger": self.judger,
            "problem": self.problem,
            "date": self.date,
        }

    def save(self, hasCases=False):
        global backendUrl, savedCookie
        reqParams = {
            "time": self.time,
            "memory": self.memory,
            "score": self.score,
            "result": self.result,
            "judger": self.judger
        }
        if hasCases:
            reqParams["cases"] = self.cases
        r = requests.post("{}/api/submission/{}/edit/".format(backendUrl,
                          self.id), reqParams, cookies=savedCookie)
        # print(r.text)
        # return r.json()

    def save_one_case(self, case_id, case_res):
        global backendUrl, savedCookie
        r = requests.post("{}/api/submission/{}/edit/case/".format(backendUrl, self.id), {
            "id": case_id,
            "result": case_res["res"],
            "memory": case_res["memory"],
            "time": case_res["time"],
            "mes": case_res["mes"],
            "score": self.score
        }, cookies=savedCookie)


def getCookie():
    global backendUrl, judgerUser, savedCookie, privilege
    try:
        r = requests.post("{}/api/user/login/".format(backendUrl), judgerUser)
        privilege = r.json()["user"]["privilege"]
        savedCookie = requests.utils.dict_from_cookiejar(r.cookies)
    except Exception as e:
        print("Cannot login or save cookies")
        return 1
    return 0


def logout():
    global backendUrl, savedCookie
    r = requests.post("{}/api/user/logout/".format(backendUrl),
                      cookies=savedCookie)


print("LHJudger v1.0.1")
print("By yemaster")
print("---------------")

while (privilege & 65536 == 0) and (privilege & 32768 == 0):  # 65536和32768是下载数据和更改提交记录的权限
    print("Try to login the user:{}".format(judgerUser["uname"]))
    getCookie()
    # time.sleep(5)
print("Login Successfully")

# print(savedCookie)
while True:
    print("Start to find unjudged submissions")
    q = Submission()
    if q.id == 0:
        print("Up to date")
    else:
        print("Start to judge #{}".format(q.id))
        q.judge()
        print("Submit change")
        # q.save()
    time.sleep(judgeWait)

print("Try to logout")
logout()
