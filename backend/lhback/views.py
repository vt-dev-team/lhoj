from django.shortcuts import get_object_or_404, render
# Create your views here.
from django.http import JsonResponse
from .models import Announcement


def AnnoucementList(request):
    AnnouncementList = [a.get_item()
                        for a in Announcement.objects.order_by('-pub_date')]
    return JsonResponse({"data": AnnouncementList})


def AnnouncementDetail(request, announcement_id):
    AnnouncementView = get_object_or_404(Announcement, pk=announcement_id)
    return JsonResponse(AnnouncementView.get_all())
