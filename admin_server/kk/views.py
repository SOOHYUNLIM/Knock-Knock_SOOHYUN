from django.core.paginator import Paginator
from django.db.models import Count, Sum, F
import json
import kk.models as models
from django.db.models.functions import ExtractWeekDay, ExtractHour, ExtractMonth
from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponse

from datetime import date, timedelta


def index(request):
    return render(request, 'index.html')


def charts(request):
    return render(request, 'charts.html')


def members(request):
    member_query = models.TblMember.objects.all()
    paginator = Paginator(member_query, 10)
    return render(request, 'members.html', {"members": paginator.get_page(1)})


def visitant(request):
    return HttpResponse(models.TblExecuteHistory.objects.filter(regdate__contains=date.today()).count())


def member(request):
    return HttpResponse(models.TblMember.objects.count())


def pick(request):
    counts = map(lambda row: row['count'], list(models.TblPick.objects.values('state').annotate(count=Count('pno')).values('count')))
    success = next(counts)
    total = success + next(counts)
    return HttpResponse(round(success/total*100))


def specialPrice(request):
    return HttpResponse(models.TblCommunityCrawling.objects.filter(regdate__contains=date.today()).count())


def category(request):
    result = list(models.TblClickHistory.objects.values('community_crawling_no__category_code__code').annotate(category=F('community_crawling_no__category_code__keyword'), count=Count('no')).values('category', 'count'))
    return JsonResponse(result, safe=False)


def traffic(request):
    type = request.GET['type']
    result = None
    if type == 'D':
        startDay = date.today()
        endDay = startDay + timedelta(days=-7)
        result = list(models.TblExecuteHistory.objects.filter(regdate__range=[endDay, startDay]).annotate(date=ExtractWeekDay('regdate')).values('date').annotate(count=Count('no'), sex=F('member_mid__sex'))) + [{'type': type}]
    elif type == 'H':
        result = list(models.TblExecuteHistory.objects.filter(regdate__contains=date.today() + timedelta(days=-1)).annotate(date=ExtractHour('regdate')).values('date').annotate(count=Count('no'), sex=F('member_mid__sex'))) + [{'type': type}]
    elif type == 'M':
        result = list(models.TblExecuteHistory.objects.filter(regdate__contains=date.today().year).annotate(date=ExtractMonth('regdate')).values('date').annotate(count=Count('no'), sex=F('member_mid__sex'))) + [{'type': type}]

    return JsonResponse(result, safe=False)