from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
import bcrypt
from .models import User, Message
from submissions.models import Submission
from discussions.models import Post


def LoginUser(request):
    return JsonResponse({
        "user": {
            "uid": request.session.get("loginUid", default=-1),
            "privilege": request.session.get("loginPrivilege", default=5),
            "uname": request.session.get("loginUser", default="未登录")
        }
    })


def Logout(request):
    if request.method == 'POST':
        try:
            del request.session["loginUser"]
            del request.session["loginUid"]
            del request.session["loginPrivilege"]
        except Exception as e:
            pass
    return JsonResponse({
        "user": {
            "uid": request.session.get("loginUid", default=-1),
            "privilege": request.session.get("loginPrivilege", default=5),
            "uname": request.session.get("loginUser", default="未登录")
        }
    })


def Login(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pword = request.POST.get('pword')
        try:
            u = User.objects.get(username=uname)
        except User.DoesNotExist:
            return JsonResponse({
                "code": 2,
                "mes": "用户不存在"
            })
        if bcrypt.checkpw(pword.encode('utf-8'), u.password.encode("utf-8")):
            request.session["loginUser"] = u.username
            request.session["loginUid"] = u.id
            request.session["loginPrivilege"] = u.privilege
            return JsonResponse({
                "code": 0,
                "mes": "登录成功",
                "user": {
                    "uid": u.id,
                    "privilege": u.privilege,
                    "uname": u.username
                }
            })
        else:
            return JsonResponse({
                "code": 3,
                "mes": "用户名或密码错误"
            })


def Register(request):
    if request.method == 'POST':
        print(request.POST)
        uname = request.POST.get('uname')
        invalidUserName = ["未登录", "LH", "lh"]
        for iun in invalidUserName:
            if iun in uname:
                return JsonResponse({
                    "code": 2,
                    "mes": "这种用户名见鬼去吧"
                })
        pword = request.POST.get('pword')
        email = request.POST.get('email')
        motto = request.POST.get('motto')
        salt = bcrypt.gensalt()
        hashed_pword = bcrypt.hashpw(
            pword.encode('utf-8'), salt).decode('utf-8')
        u = User.objects.filter(username=uname)
        if len(u) > 0:
            return JsonResponse({
                "code": 2,
                "mes": "用户已经存在"
            })
        u = User.objects.filter(email=email)
        if len(u) > 0:
            return JsonResponse({
                "code": 2,
                "mes": "邮箱已经存在"
            })
        u = User(username=uname, password=hashed_pword,
                 email=email, motto=motto, reg_time=timezone.now())
        try:
            u.save()
            request.session["loginUser"] = u.username
            request.session["loginUid"] = u.id
            request.session["loginPrivilege"] = u.privilege
            return JsonResponse({
                "code": 0,
                "mes": "OK, Your UserID is {}".format(u.id),
                "user": {
                    "uid": u.id,
                    "privilege": u.privilege,
                    "uname": u.username
                }
            })
        except Exception as e:
            return JsonResponse({
                "code": 1,
                "mes": "Error: {}".format(e)
            })


def UserSimpleList(request):
    user_id = request.session.get("loginUser", default="未登录")
    query = request.GET.get("find", "")
    uli = [q.username
           for q in User.objects.filter(username__icontains=query)]
    resList = []
    for k in uli:
        unreadMessages = len(Message.objects.filter(
            Q(from_user=k) & Q(to_user=user_id) & Q(isRead=False)))
        resList.append({
            "u": k,
            "n": unreadMessages
        })
    return JsonResponse({
        "data": resList
    })


def UserInfo(request, user_id):
    user = get_object_or_404(User, username=user_id).get_all()
    user["solved"] = len(list(set(
        [p.problem for p in Submission.objects.filter(user_id=user["username"], result=3)])))
    user["posts"] = len(Post.objects.filter(author=user["username"]))
    return JsonResponse(user)


def UserModify(request, user_id):
    uid = request.session.get("loginUid", default=-1)
    privilege = int(request.session.get("loginPrivilege", default=5))
    user = get_object_or_404(User, username=user_id)
    if (user.id != uid) and ((privilege & 16384) > 0):
        return JsonResponse({
            "code": 1,
            "mes": "权限不足"
        })
    try:
        email = request.POST.get('email')
        motto = request.POST.get('motto')
        privil = int(request.POST.get('privilege'))
        user.email = email
        user.motto = motto
        if ((privilege & 16384) > 0):
            user.privilege = privil
            if (user.id == uid):
                request.session["loginPrivilege"] = user.privilege
        user.save()
        return JsonResponse({
            "code": 0,
            "mes": "操作成功"
        })
    except Exception as e:
        return JsonResponse({
            "code": 1,
            "mes": "服务器错误" + str(e)
        })


def RankList(request):
    reqType = request.GET.get('xz', 'solve')
    try:
        pagePer = int(request.GET.get('size', '30'))
    except Exception as e:
        pagePer = 30
    pageId = 1
    if reqType == "solve":
        UserList = [u.get_simple() for u in User.objects.all()]
        cnt = 0
        for k in UserList:
            k["solve"] = len(list(set(
                [p.problem for p in Submission.objects.filter(user_id=k["username"], result=3)])))
        UserList.sort(key=lambda c: -c["solve"])
        for k in UserList:
            cnt += 1
            k["rank"] = cnt
    else:
        UserList = [u.get_simple() for u in User.objects.order_by("-rating")]
        cnt = 0
        for k in UserList:
            cnt += 1
            k["rank"] = cnt
            k["solve"] = len(list(set(
                [p.problem for p in Submission.objects.filter(user_id=k["username"], result=3)])))
    try:
        pageId = int(request.GET.get('page'))
    except Exception as e:
        pageId = 1
    P = Paginator(UserList, pagePer)
    if pageId < 1 or pageId > P.num_pages:
        pageId = 1
    return JsonResponse({
        "data": list(P.page(pageId)),
        "totalPage": P.num_pages,
        "currentPage": pageId
    })


def ContactList(request):
    user_id = request.session.get("loginUser", default="未登录")
    if user_id == "未登录":
        return JsonResponse({
            "code": 1,
            "mes": "请先登录"
        })
    receiverList = list(set(list(set(list(Message.objects.filter(Q(from_user=user_id) | Q(to_user=user_id)).order_by("-date").values_list("to_user", flat=True)))
                                 ) + list(set(list(Message.objects.filter(Q(from_user=user_id) | Q(to_user=user_id)).order_by("-date").values_list("from_user", flat=True))))))
    resList = []
    for k in receiverList:
        unreadMessages = len(Message.objects.filter(
            Q(from_user=k) & Q(to_user=user_id) & Q(isRead=False)))
        resList.append({
            "u": k,
            "n": unreadMessages
        })
    return JsonResponse({
        "code": 0,
        "data": resList,
    })


def MessageList(request):
    user_id = request.session.get("loginUser", default="未登录")
    if user_id == "未登录":
        return JsonResponse({
            "code": 1,
            "mes": "请先登录"
        })
    to_user = request.GET.get("to_user", "")
    tu = get_object_or_404(User, username=to_user)
    message = [m.get_all() for m in Message.objects.filter(
        (Q(from_user=user_id) & Q(to_user=to_user)) | (Q(from_user=to_user) & Q(to_user=user_id))).order_by("-date")]
    changeReadList = Message.objects.filter(
        Q(from_user=to_user) & Q(to_user=user_id))
    for k in changeReadList:
        k.isRead = True
    Message.objects.bulk_update(changeReadList, ['isRead'])
    pageId = 1
    try:
        pageId = int(request.GET.get('page'))
    except Exception as e:
        pageId = 1
    P = Paginator(message, 8)
    if pageId < 1 or pageId > P.num_pages:
        return JsonResponse({
            "code": 1,
            "mes": "页码错误"
        })
    return JsonResponse({
        "data": list(P.page(pageId)),
        "totalPage": P.num_pages,
        "currentPage": pageId
    })


def NewMessage(request):
    user_id = request.session.get("loginUser", default="未登录")
    privilege = int(request.session.get("loginPrivilege", default=5))
    if privilege & 64 == 0:
        return JsonResponse({
            "code": 1,
            "mes": "没有权限"
        })
    if user_id == "未登录":
        return JsonResponse({
            "code": 1,
            "mes": "请先登录"
        })
    to_user = request.POST.get("to_user", "")
    tu = get_object_or_404(User, username=to_user)
    content = request.POST.get('content', '')
    if len(content) == 0:
        return JsonResponse({
            "code": 1,
            "mes": "请输入内容"
        })
    m = Message(from_user=user_id, to_user=to_user,
                content=content, date=timezone.now())
    try:
        m.save()
        return JsonResponse({
            "code": 0,
            "mes": "发送成功"
        })
    except Exception as e:
        return JsonResponse({
            "code": 1,
            "mes": "出现错误"
        })
