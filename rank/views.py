from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import NaverRank, DaumRank, GoogleRank


def index(request):
    nr = NaverRank.objects.all()
    dr = DaumRank.objects.all()
    gr = GoogleRank.objects.all()
    return render(request, 'rank/index.html', {'nr': nr, 'dr': dr, 'gr': gr})


def refresh(request):
    if request.method == 'POST':
        import rank_crawling
    return redirect('index')