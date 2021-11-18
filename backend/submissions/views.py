from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, StreamingHttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
import requests
from .models import Submission
from contests.models import Contest
from django.utils import timezone
import json
import time
# Create your views here.


def SubmissionList(request):
    ContestId = 0
    hideResult = False
    onlyAC = False
    try:
        ContestId = int(request.GET.get('contest', '0'))
        Con = get_object_or_404(Contest, pk=ContestId)
        if (Con.tp == 1) and (timezone.now() < Con.end_time):
            hideResult = True
        elif (Con.tp == 0) and (timezone.now() < Con.end_time):
            onlyAC = True
    except Exception as e:
        ContestId = 0
    QueryQ = Q(contest=ContestId)
    if not request.GET.get('user_id') is None:
        QueryQ = QueryQ & Q(user_id=request.GET.get('user_id'))
    if not request.GET.get('problem') is None:
        QueryQ = QueryQ & Q(problem=request.GET.get('problem'))
    if not request.GET.get('result') is None:
        QueryQ = QueryQ & Q(result=int(request.GET.get('result')))
    SubmissionList = [a.get_simple()
                      for a in Submission.objects.filter(QueryQ).order_by('-id')]
    if hideResult:
        for k in SubmissionList:
            k["result"] = 0
            k["score"] = 0
            k["time"] = 0
            k["memory"] = 0
    if onlyAC:
        for k in SubmissionList:
            if k["result"] >= 4:
                k["result"] = 11
                k["score"] = 0
            elif k["result"] <= 2:
                k["score"] = 0
    pageId = 1
    try:
        pageId = int(request.GET.get('page'))
    except Exception as e:
        pageId = 1
    P = Paginator(SubmissionList, 20)
    if pageId < 1 or pageId > P.num_pages:
        pageId = 1
    return JsonResponse({
        "data": list(P.page(pageId)),
        "totalPage": P.num_pages,
        "currentPage": pageId
    })


def SubmissionDetail(request, submission_id):
    SubmissionView = get_object_or_404(Submission, pk=submission_id).get_all()
    hideResult = False
    onlyAC = False
    privilege = request.session.get("loginPrivilege", default=5)
    uname = request.session.get("loginUser", default="未登录")
    if SubmissionView["contest"] != 0:
        try:
            Con = get_object_or_404(Contest, pk=SubmissionView["contest"])
            if (Con.tp == 1) and (timezone.now() < Con.end_time):
                hideResult = True
            elif (Con.tp == 0) and (timezone.now() < Con.end_time):
                onlyAC = True
        except Exception:
            pass
    if hideResult:
        SubmissionView["result"] = 0
        SubmissionView["score"] = 0
        SubmissionView["cases"] = "{}"
        SubmissionView["time"] = 0
        SubmissionView["memory"] = 0
    if onlyAC:
        if SubmissionView["result"] >= 4:
            SubmissionView["result"] = 11
            SubmissionView["score"] = 0
            SubmissionView["cases"] = "{}"
        elif SubmissionView["result"] <= 2:
            SubmissionView["score"] = 0
        SubmissionView["cases"] = "{}"
    if privilege & 8 == 0 and SubmissionView["user_id"] != uname:
        SubmissionView["code"] = ""
    return JsonResponse(SubmissionView)


def newSubmission(request):
    if request.method == 'POST':
        privilege = request.session.get("loginPrivilege", default=5)
        if privilege & 2 == 0:
            return JsonResponse({
                "code": 1,
                "mes": "没有权限"
            })
        problem = int(request.POST.get('problem'))
        code = request.POST.get('code')
        contest = 0
        try:
            contest = int(request.POST.get('contest', ''))
        except Exception as e:
            contest = 0
        if contest > 0:
            ContestD = Contest.objects.filter(id=contest)
            if len(ContestD) <= 0:
                return JsonResponse({
                    "code": 1,
                    "mes": "没有该比赛"
                })
            if timezone.now() > ContestD[0].end_time:
                return JsonResponse({
                    "code": 1,
                    "mes": "比赛已经结束"
                })
            if timezone.now() < ContestD[0].start_time:
                return JsonResponse({
                    "code": 1,
                    "mes": "没有该比赛"
                })
        user_id = request.session.get("loginUser", default="未登录")
        cases = ""
        judger = ""
        subm = Submission(user_id=user_id, code=code, problem=problem,
                          judger=judger, cases=cases, contest=contest, date=timezone.now())
        try:
            subm.save()
            return JsonResponse({
                "code": 0,
                "mes": "OK, 提交成功",
                "submission": {
                    "id": subm.id
                }
            })
        except Exception as e:
            return JsonResponse({
                "code": 1,
                "mes": "Error: {}".format(e)
            })


def SubmissionEdit(request, submission_id):
    if request.method == 'POST':
        privilege = request.session.get("loginPrivilege", default=5)
        if privilege & 32768 == 0:
            return JsonResponse({
                "code": 1,
                "mes": "失败:没有权限!"
            })
        try:
            SubmissionView = get_object_or_404(Submission, pk=submission_id)
            SubmissionView.time = int(request.POST.get('time', 0))
            SubmissionView.memory = int(request.POST.get('memory', 0))
            SubmissionView.score = int(request.POST.get('score', 0))
            getCases = request.POST.get('cases', '')
            if getCases != '':
                SubmissionView.cases = getCases
            SubmissionView.result = int(request.POST.get('result', 0))
            SubmissionView.judger = request.POST.get('judger', '')
            SubmissionView.save()
            return JsonResponse({
                "code": 0,
                "mes": "成功!"
            })
        except Exception as e:
            return JsonResponse({
                "code": 1,
                "mes": "失败:{}!".format(e)
            })


def UpdateOneCase(request, submission_id):
    if request.method == 'POST':
        privilege = request.session.get("loginPrivilege", default=5)
        if privilege & 32768 == 0:
            return JsonResponse({
                "code": 1,
                "mes": "失败:没有权限!"
            })
        try:
            SubmissionView = get_object_or_404(Submission, pk=submission_id)
            case_id = int(request.POST.get('id'))
            case_result = request.POST.get('result')
            case_time = request.POST.get('time')
            case_memory = request.POST.get('memory')
            case_mes = request.POST.get('mes', '')
            score = int(request.POST.get('score'))
            cases = json.loads(SubmissionView.cases)
            if not ("datas" in cases):
                return JsonResponse({
                    "code": 1,
                    "mes": "不存在datas"
                })
            if len(cases["datas"]) < case_id:
                return JsonResponse({
                    "code": 1,
                    "mes": "没有对应的case"
                })
            cases["datas"][case_id] = {
                "res": int(case_result),
                "time": int(case_time),
                "memory": int(case_memory),
                "mes": case_mes
            }
            SubmissionView.cases = json.dumps(cases)
            SubmissionView.score = score
            SubmissionView.save()
            return JsonResponse({
                "code": 0,
                "mes": "成功"
            })
        except Exception as e:
            return JsonResponse({
                "code": 1,
                "mes": "失败:{}!".format(e)
            })


def FindSubmission(request):
    q = Submission.objects.filter(result__lte=1).order_by("id")[:1]
    if len(q) <= 0:
        return JsonResponse({
            "id": 0,
            "mes": "没有未评测的记录!"
        })
    else:
        return JsonResponse({
            "id": q[0].id,
            "submission": q[0].get_all()
        })
