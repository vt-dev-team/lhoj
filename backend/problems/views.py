from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from wsgiref.util import FileWrapper
from .models import Problem
import os
import tempfile
import zipfile
import shutil
from submissions.models import Submission
import json

# Create your views here.


def ProblemsList(request):
    searchWord = request.GET.get('search', '')
    if searchWord == '':
        rawProblemSet = Problem.objects.all()
    else:
        rawProblemSet = Problem.objects.filter(
            Q(title__icontains=searchWord) | Q(content__icontains=searchWord) | Q(tags__icontains=searchWord))
    ProblemList = [a.get_simple() for a in rawProblemSet.order_by('id')]
    uname = request.session.get("loginUser", default="未登录")
    if uname != "未登录":
        for k in ProblemList:
            z = Submission.objects.filter(
                user_id=uname, problem=k["id"], contest=0)
            aclist = z.filter(result=3)
            if len(aclist) > 0:
                k["result"] = {
                    "res": 3,
                    "sid": aclist.last().id
                }
            elif len(z) > 0:
                zlast = z.last()
                k["result"] = {
                    "res": zlast.result,
                    "sid": zlast.id
                }
            else:
                k["result"] = {
                    "res": 0,
                    "sid": 0
                }
    pageId = 1
    try:
        pageId = int(request.GET.get('page'))
    except Exception as e:
        pageId = 1
    P = Paginator(ProblemList, 50)
    if pageId < 1 or pageId > P.num_pages:
        pageId = 1
    return JsonResponse({
        "data": list(P.page(pageId)),
        "totalPage": P.num_pages,
        "currentPage": pageId
    })


def ProblemDetail(request, problem_id):
    ProblemView = get_object_or_404(Problem, pk=problem_id)
    return JsonResponse(ProblemView.get_all())


def ProblemLatest(request):
    latest = [u.get_simple()
              for u in Problem.objects.order_by('-pub_date')[:5]]
    return JsonResponse({
        "data": latest
    })


def ProblemNew(request):
    privilege = request.session.get("loginPrivilege", default=5)
    uname = request.session.get("loginUser", default="未登录")
    if privilege & 256 != 0:
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
            time = int(request.POST.get('time_limit', '1000'))
        except Exception as e:
            time = 1000
        try:
            memory = int(request.POST.get('memory_limit', '262144'))
        except Exception as e:
            memory = 262144
        try:
            judgeType = int(request.POST.get('judge_type', '0'))
        except Exception as e:
            judgeType = 0
        tags = request.POST.get('tags', '')
        algorithm = request.POST.get('algorithm', '')
        p = Problem(title=title, content=content,
                    time_limit=time, memory_limit=memory, judge_type=judgeType, tags=tags, difficulty=0, algorithms=algorithm, author=uname, pub_date=timezone.now())
        p.save()
        return JsonResponse({
            "code": 0,
            "mes": "成功添加",
            "id": p.id,
        })
    else:
        return JsonResponse({
            "code": 1,
            "mes": "权限不足"
        })


def ProblemEdit(request, problem_id):
    privilege = request.session.get("loginPrivilege", default=5)
    uname = request.session.get("loginUser", default="未登录")
    if privilege & 2048 != 0:
        p = get_object_or_404(Problem, pk=problem_id)
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
            time = int(request.POST.get('time_limit', '1000'))
        except Exception as e:
            time = 1000
        try:
            memory = int(request.POST.get('memory_limit', '262144'))
        except Exception as e:
            memory = 262144
        try:
            judgeType = int(request.POST.get('judge_type', '0'))
        except Exception as e:
            judgeType = 0
        tags = request.POST.get('tags', '')
        algorithm = request.POST.get('algorithm', '')
        p.title = title
        p.content = content
        p.time_limit = time
        p.memory_limit = memory
        p.judge_type = judgeType
        p.tags = tags
        p.difficulty = 0
        p.algorithms = algorithm
        p.author = uname
        p.pub_date = timezone.now()
        p.save()
        return JsonResponse({
            "code": 0,
            "mes": "成功",
            "id": p.id,
        })
    else:
        return JsonResponse({
            "code": 1,
            "mes": "权限不足"
        })


def GetData(request, problem_id):
    privilege = request.session.get("loginPrivilege", default=5)
    if privilege & 2048 != 0:
        try:
            if not os.path.exists("problems/data/{}/config.lh".format(problem_id)):
                return JsonResponse({
                    "code": 0,
                    "data": {},
                })
            with open("problems/data/{}/config.lh".format(problem_id)) as f:
                k = json.load(f)
            return JsonResponse({
                "code": 0,
                "data": k,
            })
        except Exception as e:
            return JsonResponse({
                "code": 1,
                "mes": "出现错误" + str(e),
            })
    else:
        return JsonResponse({
            "code": 1,
            "mes": "权限不足"
        })


def UploadData(request, problem_id):
    privilege = request.session.get("loginPrivilege", default=5)
    if privilege & 2048 != 0:
        p = request.FILES.get('dataFile')
        if p:
            try:
                """with open("problems/data/{}.zip".format(problem_id), "wb") as f:
                    for chk in p.chunks():
                        f.write(chk)"""
                if os.path.exists("problems/data/{}".format(problem_id)):
                    shutil.rmtree("problems/data/{}".format(problem_id))
                zip_data_file = zipfile.ZipFile(p)
                zip_data_file.extractall(
                    path="problems/data/{}".format(problem_id))
                return JsonResponse({
                    "code": 0,
                    "mes": "成功",
                })
            except Exception as e:
                return JsonResponse({
                    "code": 1,
                    "mes": "出现错误" + str(e),
                })
        else:
            return JsonResponse({
                "code": 1,
                "mes": "未收到任何文件",
            })
    else:
        return JsonResponse({
            "code": 1,
            "mes": "权限不足"
        })


def ConfigData(request, problem_id):
    pass


def DataDownload(request, problem_id):
    privilege = request.session.get("loginPrivilege", default=5)
    if privilege & 65536 != 0:
        # if True:
        temp = tempfile.TemporaryFile()
        archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
        file_list = os.listdir("problems/data/{}".format(problem_id))
        for fl in file_list:
            archive.write("problems/data/{}/{}".format(problem_id, fl), fl)
        archive.close()
        length = temp.tell()
        temp.seek(0)
        wrapper = FileWrapper(temp)
        response = HttpResponse(wrapper, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=data{}.zip'.format(
            problem_id)
        response['Content-Length'] = length  # temp.tell()
        return response
    else:
        return JsonResponse({
            "code": 1,
            "mes": "没有权限下载数据"
        })


def AttachementsDownload(request, problem_id):
    privilege = request.session.get("loginPrivilege", default=5)
    if privilege & 2 != 0:
        # if True:
        if not os.path.exists("problems/attachments/{}".format(problem_id)):
            return JsonResponse({
                "code": 1,
                "mes": "找不到附件"
            })
        temp = tempfile.TemporaryFile()
        archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
        file_list = os.listdir("problems/attachments/{}".format(problem_id))
        for fl in file_list:
            archive.write(
                "problems/attachments/{}/{}".format(problem_id, fl), fl)
        archive.close()
        length = temp.tell()
        temp.seek(0)
        wrapper = FileWrapper(temp)
        response = HttpResponse(wrapper, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=attachments{}.zip'.format(
            problem_id)
        response['Content-Length'] = length  # temp.tell()
        return response
    else:
        print("YES")
        return JsonResponse({
            "code": 1,
            "mes": "没有权限下载附件(需要登录)"
        })
