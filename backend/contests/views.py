from genericpath import exists
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, StreamingHttpResponse
from django.core.paginator import Paginator
from django.utils import timezone
# Create your views here.
import time
import datetime
from .models import Contest
from problems.models import Problem
from submissions.models import Submission


def ContestList(request):
    ContestList = [a.get_simple()
                   for a in Contest.objects.order_by('-start_time')]
    pageId = 1
    try:
        pageId = int(request.GET.get('page'))
    except Exception as e:
        pageId = 1
    P = Paginator(ContestList, 20)
    if pageId < 1 or pageId > P.num_pages:
        pageId = 1
    return JsonResponse({
        "data": list(P.page(pageId)),
        "totalPage": P.num_pages,
        "currentPage": pageId
    })


def ContestDetail(request, contest_id):
    ContestD = get_object_or_404(Contest, pk=contest_id).get_all()
    hideResult = False
    onlyAC = False
    if (ContestD["tp"] == 1) and (timezone.now() < ContestD["end_time"]):
        hideResult = True
    elif (ContestD["tp"] == 0) and (timezone.now() < ContestD["end_time"]):
        onlyAC = True
    if request.GET.get('notShowProblem', '') != 'yes':
        Problems = ContestD["problems"].split(",")
        ContestD["problems"] = []
        for i in Problems:
            Pro = Problem.objects.filter(id=int(i))
            for j in Pro:
                ContestD["problems"].append(j.get_simple())
            uname = request.session.get("loginUser", default="未登录")
        if uname != "未登录":
            for k in ContestD["problems"]:
                z = Submission.objects.filter(
                    user_id=uname, problem=k["id"], contest=contest_id)
                aclist = z.filter(result=3)
                if (not hideResult) and len(aclist) > 0:
                    k["result"] = {
                        "res": 3,
                        "sid": aclist.last().id
                    }
                elif len(z) > 0:
                    zlast = z.last()
                    if hideResult:
                        k["result"] = {
                            "res": 2,
                            "sid": zlast.id
                        }
                    elif onlyAC:
                        k["result"] = {
                            "res": 11,
                            "sid": zlast.id
                        }
                    else:
                        k["result"] = {
                            "res": zlast.result,
                            "sid": zlast.id
                        }
                else:
                    k["result"] = {
                        "res": 0,
                        "sid": 0
                    }
    return JsonResponse({
        "data": ContestD
    })

def ContestLatest(request):
    latest = [u.get_simple()
              for u in Contest.objects.order_by('-start_time')[:5]]
    return JsonResponse({
        "data": latest
    })

def ContestRank(request, contest_id):
    ContestD = get_object_or_404(Contest, pk=contest_id)
    hideResult = False
    if (ContestD.tp == 1) and (timezone.now() < ContestD.end_time):
        hideResult = True
    if ContestD.tp == 1:
        ContestSubmissions = Submission.objects.filter(
            contest=contest_id).order_by("date")
    else:
        ContestSubmissions = Submission.objects.filter(
            contest=contest_id).order_by("-score", "date")
    OneUser = {
        "rank": 0,
        "user_id": "",
        "solved": 0,
        "score": 0
    }
    RecordUsers = {}
    ps = ContestD.problems.split(",")
    Solved = [0 for i in range(len(ps))]
    BlankProblem = {
        "title": "",
        "score": 0,
        "time": 0,
        "first_blood": False,
        "recorded": False,
        "result": 0,
        "submission_id": 0,
    }
    for k in ContestSubmissions:
        azx = k.get_simple()
        if hideResult:
            azx["result"] = 2
            azx["time"] = 0
            azx["memory"] = 0
            azx["score"] = 0
        if not azx["user_id"] in RecordUsers:
            p = OneUser.copy()
            p["user_id"] = azx["user_id"]
            p["problems"] = []
            for j in range(len(ps)):
                bt = BlankProblem.copy()
                bt["title"] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[j]
                p["problems"].append(bt)
            RecordUsers[azx["user_id"]] = p
        strpid = str(azx["problem"])
        if strpid in ps:
            pindex = ps.index(strpid)
            g = RecordUsers[azx["user_id"]]["problems"][pindex]
            if ContestD.tp != 1 and g["recorded"]:
                continue
            g["score"] = azx["score"]
            g["time"] = azx["date"]
            g["submission_id"] = azx["id"]
            g["result"] = azx["result"]
            if k.result == 3:
                if Solved[pindex] == 0:
                    g["first_blood"] = True
                Solved[pindex] = 1
            if not g["recorded"]:
                if azx["result"] == 3:
                    RecordUsers[azx["user_id"]]["solved"] += 1
            g["recorded"] = True
    RU = []
    for i in RecordUsers:
        RU.append(RecordUsers[i])
    for i in RU:
        for j in i["problems"]:
            i["score"] += j["score"]
    if ContestD.tp == 1:
        RU.sort(key=lambda c: -c["score"])
    else:
        RU.sort(key=lambda c: -c["solved"])
    cnt = 0
    for i in RU:
        cnt += 1
        i["rank"] = cnt
    return JsonResponse({
        "data": RU,
        "contest": ContestD.get_all()
    })


def ContestNew(request):
    privilege = request.session.get("loginPrivilege", default=5)
    uname = request.session.get("loginUser", default="未登录")
    if privilege & 512 != 0:
        title = request.POST.get('title', '')
        if len(title) <= 0:
            return JsonResponse({
                "code": 1,
                "mes": "标题不能为空"
            })
        content = request.POST.get('content', '')
        if len(content) <= 0:
            return JsonResponse({
                "code": 1,
                "mes": "内容不能为空"
            })
        try:
            start_time = request.POST.get('start_time')
            start_time = time.strptime(start_time,  '%Y-%m-%d %H:%M')
            y, m, d, h, M = start_time[:5]
            start_time = datetime.datetime(y, m, d, h, M)
        except Exception as e:
            return JsonResponse({
                "code": 1,
                "mes": "开始时间不合法"
            })
        try:
            end_time = request.POST.get('end_time')
            end_time = time.strptime(end_time,  '%Y-%m-%d %H:%M')
            y, m, d, h, M = end_time[:5]
            end_time = datetime.datetime(y, m, d, h, M)
        except Exception as e:
            return JsonResponse({
                "code": 1,
                "mes": "结束时间不合法"
            })
        try:
            memory = int(request.POST.get('memory_limit', '262144'))
        except Exception as e:
            memory = 262144
        try:
            tp = int(request.POST.get('tp', '0'))
        except Exception as e:
            judgeType = 0
        problems = request.POST.get('problems', '')
        try:
            p = Contest(title=title, description=content,
                        start_time=start_time, end_time=end_time, tp=tp, problems=problems)
            p.save()
            return JsonResponse({
                "code": 0,
                "mes": "成功添加",
                "id": p.id,
            })
        except Exception as e:
            return JsonResponse({
                "code": 1,
                "mes": "服务器错误",
            })
    else:
        return JsonResponse({
            "code": 1,
            "mes": "权限不足"
        })


def ContestEdit(request, contest_id):
    privilege = request.session.get("loginPrivilege", default=5)
    uname = request.session.get("loginUser", default="未登录")
    p = get_object_or_404(Contest, pk=contest_id)
    if privilege & 4096 != 0:
        title = request.POST.get('title', '')
        if len(title) <= 0:
            return JsonResponse({
                "code": 1,
                "mes": "标题不能为空"
            })
        content = request.POST.get('content', '')
        if len(content) <= 0:
            return JsonResponse({
                "code": 1,
                "mes": "内容不能为空"
            })
        try:
            start_time = request.POST.get('start_time')
            start_time = time.strptime(start_time,  '%Y-%m-%d %H:%M')
            y, m, d, h, M = start_time[:5]
            start_time = datetime.datetime(y, m, d, h, M)
        except Exception as e:
            return JsonResponse({
                "code": 1,
                "mes": "开始时间不合法"
            })
        try:
            end_time = request.POST.get('end_time')
            end_time = time.strptime(end_time,  '%Y-%m-%d %H:%M')
            y, m, d, h, M = end_time[:5]
            end_time = datetime.datetime(y, m, d, h, M)
        except Exception as e:
            return JsonResponse({
                "code": 1,
                "mes": "结束时间不合法"
            })
        try:
            memory = int(request.POST.get('memory_limit', '262144'))
        except Exception as e:
            memory = 262144
        try:
            tp = int(request.POST.get('tp', '0'))
        except Exception as e:
            judgeType = 0
        problems = request.POST.get('problems', '')
        try:
            p.title = title
            p.description = content
            p.start_time = start_time
            p.end_time = end_time
            p.tp = tp
            p.problems = problems
            p.save()
            return JsonResponse({
                "code": 0,
                "mes": "成功添加",
                "id": p.id,
            })
        except Exception as e:
            return JsonResponse({
                "code": 1,
                "mes": "服务器错误",
            })
    else:
        return JsonResponse({
            "code": 1,
            "mes": "权限不足"
        })


def ContestDelete(request, contest_id):
    privilege = request.session.get("loginPrivilege", default=5)
    p = get_object_or_404(Contest, pk=contest_id)
    if privilege & 4096 != 0:
        try:
            p.delete()
            s = Submission.objects.filter(contest=contest_id)
            s.delete()
            return JsonResponse({
                "code": 0,
                "mes": "成功删除",
            })
        except Exception as e:
            return JsonResponse({
                "code": 1,
                "mes": "服务器错误",
            })
    else:
        return JsonResponse({
            "code": 1,
            "mes": "权限不足"
        })
