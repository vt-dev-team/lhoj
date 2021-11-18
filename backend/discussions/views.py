from django.db.models.fields import DateField
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.core.paginator import Page, Paginator
from django.db.models import Q
import re
from .models import Section, Post, Comment
from django.utils import timezone

# Create your views here.


def SectionList(request):
    Sections = [u.get_all() for u in Section.objects.all()]
    return JsonResponse({
        "data": Sections
    })


def PostList(request):
    section_id = request.GET.get("section", "all")
    author_id = request.GET.get("user", "")
    ProblemSearch = re.search('^P(\d+)$', section_id)
    Posts = []
    if section_id == "all":
        if author_id != "":
            Posts = [k.get_simple() for k in Post.objects.filter(
                author=author_id).order_by("-toplevel", "-date")]
        else:
            Posts = [k.get_simple()
                     for k in Post.objects.order_by("-toplevel", "-date")]
    else:
        if ProblemSearch is None:
            sid = get_object_or_404(Section, pk=section_id)
        else:
            section_id = int(ProblemSearch.group(1)) + 1000
        if author_id != "":
            Posts = [k.get_simple() for k in Post.objects.filter(
                (Q(section=section_id) | Q(toplevel=3)) & Q(author=author_id)).order_by("-toplevel", "-date")]
        else:
            Posts = [k.get_simple() for k in Post.objects.filter(
                Q(section=section_id) | Q(toplevel=3)).order_by("-toplevel", "-date")]
    pageId = 1
    try:
        pageId = int(request.GET.get('page'))
    except Exception as e:
        pageId = 1
    P = Paginator(Posts, 10)
    if pageId < 1 or pageId > P.num_pages:
        pageId = 1
    return JsonResponse({
        "data": list(P.page(pageId)),
        "totalPage": P.num_pages,
        "currentPage": pageId
    })


def PostShow(request, post_id):
    mode = request.GET.get('mode', 'post')
    if mode == 'post':
        PostGet = get_object_or_404(Post, pk=post_id)
        return JsonResponse({
            "post": PostGet.get_all()
        })
    else:
        PostComment = [u.get_all()
                       for u in Comment.objects.filter(post=post_id).order_by("id")]
        pageId = 1
        try:
            pageId = int(request.GET.get('page'))
        except Exception as e:
            pageId = 1
        P = Paginator(PostComment, 10)
        if pageId < 1 or pageId > P.num_pages:
            pageId = 1
        return JsonResponse({
            "comments": list(P.page(pageId)),
            "totalPage": P.num_pages,
            "currentPage": pageId
        })


def newPost(request):
    privilege = request.session.get("loginPrivilege", default=5)
    section_id = request.POST.get('section')
    ProblemSearch = re.search('^P(\d+)$', section_id)
    if ProblemSearch is None:
        S = get_object_or_404(Section, pk=section_id)
        if privilege & S.privilege == 0:
            return JsonResponse({
                "code": 1,
                "mes": "没有权限"
            })
    else:
        section_id = int(ProblemSearch.group(1)) + 1000
        if privilege & 128 == 0:
            return JsonResponse({
                "code": 1,
                "mes": "没有权限"
            })
    uname = request.session.get("loginUser", default="未登录")
    title = request.POST.get('title')
    if len(title) <= 0:
        return JsonResponse({
            "code": 1,
            "mes": "请输入标题"
        })
    content = request.POST.get('content')
    if len(title) <= 0:
        return JsonResponse({
            "code": 1,
            "mes": "请输入内容"
        })
    toplevel = 1
    try:
        nc = Post(author=uname, title=title,
                  content=content, section=section_id, toplevel=toplevel, date=timezone.now())
        nc.save()
        return JsonResponse({
            "code": 0,
            "mes": "发表成功",
            "post": nc.id
        })
    except Exception as e:
        return JsonResponse({
            "code": 1,
            "mes": "服务器错误"
        })


def editPost(request, post_id):
    privilege = request.session.get("loginPrivilege", default=5)
    uname = request.session.get("loginUser", default="未登录")
    ns = get_object_or_404(Post, pk=post_id)
    if (ns.author == uname) or (privilege & 8192 > 0):
        title = request.POST.get('title')
        if len(title) <= 0:
            return JsonResponse({
                "code": 1,
                "mes": "请输入标题"
            })
        content = request.POST.get('content')
        if len(title) <= 0:
            return JsonResponse({
                "code": 1,
                "mes": "请输入内容"
            })
        ns.title = title
        ns.content = content
        if (privilege & 8192 > 0):
            try:
                toplevel = int(request.POST.get('toplevel'))
                ns.toplevel = toplevel
                ns.date = timezone.now()
            except Exception as e:
                pass
        try:
            ns.save()
            return JsonResponse({
                "code": 0,
                "mes": "编辑成功",
            })
        except Exception as e:
            return JsonResponse({
                "code": 1,
                "mes": "服务器错误"
            })
    else:
        return JsonResponse({
            "code": 1,
            "mes": "没有权限"
        })


def DeletePost(request, post_id):
    privilege = request.session.get("loginPrivilege", default=5)
    uname = request.session.get("loginUser", default="未登录")
    ns = get_object_or_404(Post, pk=post_id)
    if (ns.author == uname) or (privilege & 8192 > 0):
        try:
            ns.delete()
            Comment.objects.filter(post=post_id).delete()
            return JsonResponse({
                "code": 0,
                "mes": "删除成功",
            })
        except Exception as e:
            return JsonResponse({
                "code": 1,
                "mes": "服务器错误"
            })
    else:
        return JsonResponse({
            "code": 1,
            "mes": "没有权限"
        })


def newComment(request):
    privilege = request.session.get("loginPrivilege", default=5)
    if privilege & 128 == 0:
        return JsonResponse({
            "code": 1,
            "mes": "没有权限"
        })
    uname = request.session.get("loginUser", default="未登录")
    post_id = request.POST.get('post_id')
    content = request.POST.get('content', '')
    if len(content) <= 0:
        return JsonResponse({
            "code": 1,
            "mes": "请输入内容"
        })
    nc = Comment(author=uname, post=post_id,
                 content=content, date=timezone.now())
    nc.save()
    return JsonResponse({
        "code": 0,
        "mes": "评论成功"
    })


def DeleteComment(request, comment_id):
    privilege = request.session.get("loginPrivilege", default=5)
    uname = request.session.get("loginUser", default="未登录")
    ns = get_object_or_404(Comment, pk=comment_id)
    if (ns.author == uname) or (privilege & 8192 > 0):
        try:
            ns.delete()
            return JsonResponse({
                "code": 0,
                "mes": "删除成功",
            })
        except Exception as e:
            return JsonResponse({
                "code": 1,
                "mes": "服务器错误"
            })
    else:
        return JsonResponse({
            "code": 1,
            "mes": "没有权限"
        })