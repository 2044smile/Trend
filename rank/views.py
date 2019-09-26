from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import NaverRank, DaumRank, GoogleRank
import rank_crawling


def index(request):
    nr = NaverRank.objects.all()
    dr = DaumRank.objects.all()
    gr = GoogleRank.objects.all()
    return render(request, 'rank/index.html', {'nr': nr, 'dr': dr, 'gr': gr})


def refresh(request):
    if request.method == 'POST':
        rank_crawling.naver_trend()
        rank_crawling.daum_trend()
        rank_crawling.google_trend()
    return redirect('index')